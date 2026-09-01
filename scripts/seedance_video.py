#!/usr/bin/env python3
"""Volcengine Ark Seedance - Text to Video Generator

Generate videos from text prompts using ByteDance's Seedance models.
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, Any, List, Optional

import requests

# Disable SSL warnings for development
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API Configuration
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"


def get_api_key() -> str:
    """Get Volcengine Ark API key from environment."""
    key = os.environ.get("VOLCENGINE_ARK_API_KEY")
    if not key:
        print("Error: VOLCENGINE_ARK_API_KEY environment variable not set", file=sys.stderr)
        print("Get your API key at https://console.volcengine.com/ark", file=sys.stderr)
        sys.exit(1)
    return key


def create_headers(api_key: str) -> Dict[str, str]:
    """Create request headers."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def list_models(api_key: str, seedance_only: bool = True) -> None:
    """List available models."""
    response = requests.get(
        f"{BASE_URL}/models",
        headers=create_headers(api_key),
        timeout=15,
        verify=False
    )
    response.raise_for_status()
    data = response.json()

    models = data.get("data", [])
    if seedance_only:
        models = [m for m in models if "seedance" in m.get("id", "").lower()]

    print(f"\nAvailable models ({len(models)}):")
    for model in models:
        model_id = model.get("id", "N/A")
        name = model.get("name", "N/A")
        status = model.get("status", "unknown")
        print(f"  - {model_id} | {name} | status={status}")


def generate_video(
    api_key: str,
    prompt: str,
    model: str = "doubao-seedance-1-5-pro-251215",
    ratio: str = "16:9",
    duration: int = 5,
    resolution: str = "720p",
    watermark: bool = False,
    poll: bool = False,
    first_frame: str = "",
    last_frame: str = "",
    reference_images: Optional[List[str]] = None,
    reference_audios: Optional[List[str]] = None,
    generate_audio: Optional[bool] = None,
    return_last_frame: bool = False,
    download_dir: str = ""
) -> str:
    """Create a video generation task.

    Supports text-to-video, first/last-frame image-to-video and
    multi-modal reference images/audios, all via the `content` array.
    """
    # Build the multimodal content array. Order matters: text first,
    # then first_frame, last_frame, reference_image(s) and reference_audio(s).
    content: List[Dict[str, Any]] = []
    if prompt:
        content.append({"type": "text", "text": prompt})
    if first_frame:
        content.append({
            "type": "image_url",
            "image_url": {"url": first_frame},
            "role": "first_frame",
        })
    if last_frame:
        content.append({
            "type": "image_url",
            "image_url": {"url": last_frame},
            "role": "last_frame",
        })
    for ref in (reference_images or []):
        content.append({
            "type": "image_url",
            "image_url": {"url": ref},
            "role": "reference_image",
        })
    for aud in (reference_audios or []):
        content.append({
            "type": "audio_url",
            "audio_url": {"url": aud},
            "role": "reference_audio",
        })

    if not content:
        print("Error: no input provided (prompt or frame images required)", file=sys.stderr)
        sys.exit(1)

    body = {
        "model": model,
        "ratio": ratio,
        "content": content,
        "duration": duration,
        "resolution": resolution,
        "watermark": watermark
    }
    if generate_audio is not None:
        body["generate_audio"] = generate_audio
    if return_last_frame:
        body["return_last_frame"] = True

    response = requests.post(
        f"{BASE_URL}/contents/generations/tasks",
        headers=create_headers(api_key),
        json=body,
        timeout=15,
        verify=False
    )
    response.raise_for_status()
    data = response.json()

    task_id = data.get("id", "")
    if not task_id:
        print("Error: No task_id in response", file=sys.stderr)
        print(json.dumps(data, indent=2), file=sys.stderr)
        sys.exit(1)

    print(f"\nTask created successfully!")
    print(f"Task ID: {task_id}")
    print(f"Model: {model}")
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    if poll:
        print("\nPolling for results...")
        task = query_task(api_key, task_id, max_attempts=120, interval=3, output=True)
        if task and task.get("status") == "succeeded":
            print("\n✅ Video generated successfully!")
            video_url = task.get("content", {}).get("video_url", "")
            if video_url:
                print(f"\nVideo URL: {video_url}")
            # Download video if download_dir specified
            if download_dir:
                os.makedirs(download_dir, exist_ok=True)
                video_path = os.path.join(download_dir, f"{task_id}.mp4")
                print(f"\n💾 Downloading video to {video_path}...")
                download_file(video_url, video_path)
                print(f"✅ Video saved: {video_path}")
            # Download last frame if available
            last_frame_url = task.get("content", {}).get("last_frame_url", "")
            if last_frame_url and download_dir:
                last_frame_path = os.path.join(download_dir, f"{task_id}_last_frame.png")
                print(f"💾 Downloading last frame to {last_frame_path}...")
                download_file(last_frame_url, last_frame_path)
                print(f"✅ Last frame saved: {last_frame_path}")
            elif last_frame_url:
                print(f"\nLast frame URL: {last_frame_url}")
        return task_id

    return task_id


def download_file(url: str, save_path: str) -> None:
    """Download a file from URL to local path."""
    response = requests.get(url, stream=True, timeout=300, verify=False)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))
    downloaded = 0
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total and total > 0:
                    pct = downloaded / total * 100
                    print(f"\r  {downloaded/1024/1024:.1f}MB / {total/1024/1024:.1f}MB ({pct:.0f}%)", end="", flush=True)
    print()


def query_task(
    api_key: str,
    task_id: str,
    max_attempts: int = 30,
    interval: int = 2,
    output: bool = True
) -> Dict[str, Any]:
    """Query task status."""
    for attempt in range(max_attempts):
        response = requests.get(
            f"{BASE_URL}/contents/generations/tasks/{task_id}",
            headers=create_headers(api_key),
            timeout=10,
            verify=False
        )

        if response.status_code != 200:
            if output:
                print(f"Error querying task: {response.status_code}", file=sys.stderr)
            continue

        task = response.json()
        status = task.get("status", "unknown")

        if status == "succeeded":
            if output:
                print("\nTask succeeded!")
            return task
        elif status in ["pending", "processing", "running", "queued"]:
            if output and (attempt + 1) % 10 == 0:
                print(f"Status: {status} (still processing... attempt {attempt+1}/{max_attempts})")
            time.sleep(interval)
        else:
            if output:
                print(f"Task failed with status: {status}", file=sys.stderr)
                print(json.dumps(task, indent=2, ensure_ascii=False), file=sys.stderr)
            return task

    if output:
        print("Timeout: Task did not complete in time", file=sys.stderr)
    return {"status": "timeout"}


def main():
    parser = argparse.ArgumentParser(
        description="Volcengine Ark Seedance - Text to Video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate --prompt "A beautiful sunset" --ratio 16:9 --duration 5
  %(prog)s generate --prompt "Fight scene" --first-frame https://.../start.png --last-frame https://.../end.png --poll
  %(prog)s generate --prompt "Epic battle" --first-frame https://.../start.png --return-last-frame --poll --download-dir ./output
  %(prog)s status --task-id cgt-20260330200405-29g92
  %(prog)s list
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a video from text or images")
    gen_parser.add_argument("--prompt", default="", help="Text prompt for video (optional when images are provided)")
    gen_parser.add_argument("--model", default="doubao-seedance-1-5-pro-251215", help="Model ID")
    gen_parser.add_argument("--ratio", default="16:9", choices=["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "adaptive"], help="Aspect ratio (use 'adaptive' with first/last frame)")
    gen_parser.add_argument("--duration", type=int, default=5, help="Duration in seconds")
    gen_parser.add_argument("--resolution", default="720p", choices=["480p", "720p", "1080p", "4k"], help="Resolution")
    gen_parser.add_argument("--watermark", action="store_true", help="Add watermark")
    gen_parser.add_argument("--poll", action="store_true", help="Poll for results automatically")
    gen_parser.add_argument("--first-frame", default="", help="URL of the first frame image (image-to-video)")
    gen_parser.add_argument("--last-frame", default="", help="URL of the last frame image (requires --first-frame)")
    gen_parser.add_argument("--reference-image", action="append", default=None, help="URL of a reference image (repeatable, Seedance 2.0+)")
    gen_parser.add_argument("--reference-audio", action="append", default=None, help="URL of a reference audio, wav/mp3 (repeatable, Seedance 2.0+)")
    gen_parser.add_argument("--generate-audio", dest="generate_audio", action="store_true", default=None, help="Generate synchronized audio")
    gen_parser.add_argument("--no-audio", dest="generate_audio", action="store_false", help="Generate silent video")
    gen_parser.add_argument("--return-last-frame", action="store_true", help="Return the last frame of the generated video (PNG)")
    gen_parser.add_argument("--download-dir", default="", help="Directory to save downloaded video and last frame")

    # Status command
    status_parser = subparsers.add_parser("status", help="Query task status")
    status_parser.add_argument("--task-id", required=True, help="Task ID to query")
    status_parser.add_argument("--max-attempts", type=int, default=30, help="Max polling attempts")
    status_parser.add_argument("--interval", type=int, default=2, help="Polling interval (seconds)")

    # Download command
    dl_parser = subparsers.add_parser("download", help="Download video and last frame from a completed task")
    dl_parser.add_argument("--task-id", required=True, help="Task ID to download")
    dl_parser.add_argument("--output-dir", required=True, help="Directory to save files")
    dl_parser.add_argument("--filename", default="", help="Custom filename (without extension)")

    # List command
    list_parser = subparsers.add_parser("list", help="List available models")
    list_parser.add_argument("--all", action="store_true", help="Show all models, not just Seedance")

    args = parser.parse_args()
    api_key = get_api_key()

    try:
        if args.command == "generate":
            if args.last_frame and not args.first_frame:
                print("Error: --last-frame requires --first-frame", file=sys.stderr)
                sys.exit(1)
            generate_video(
                api_key,
                args.prompt,
                model=args.model,
                ratio=args.ratio,
                duration=args.duration,
                resolution=args.resolution,
                watermark=args.watermark,
                poll=args.poll,
                first_frame=args.first_frame,
                last_frame=args.last_frame,
                reference_images=args.reference_image,
                reference_audios=args.reference_audio,
                generate_audio=args.generate_audio,
                return_last_frame=args.return_last_frame,
                download_dir=args.download_dir
            )
        elif args.command == "status":
            query_task(
                api_key,
                args.task_id,
                max_attempts=args.max_attempts,
                interval=args.interval
            )
        elif args.command == "download":
            task = query_task(api_key, args.task_id, max_attempts=1, interval=0, output=False)
            if task.get("status") != "succeeded":
                print(f"Error: task not succeeded (status: {task.get('status')})", file=sys.stderr)
                sys.exit(1)
            os.makedirs(args.output_dir, exist_ok=True)
            base_name = args.filename or args.task_id
            video_url = task.get("content", {}).get("video_url", "")
            if video_url:
                video_path = os.path.join(args.output_dir, f"{base_name}.mp4")
                print(f"Downloading video to {video_path}...")
                download_file(video_url, video_path)
                print(f"✅ Video saved: {video_path}")
            last_frame_url = task.get("content", {}).get("last_frame_url", "")
            if last_frame_url:
                lf_path = os.path.join(args.output_dir, f"{base_name}_last_frame.png")
                print(f"Downloading last frame to {lf_path}...")
                download_file(last_frame_url, lf_path)
                print(f"✅ Last frame saved: {lf_path}")
        elif args.command == "list":
            list_models(api_key, seedance_only=not args.all)

    except requests.HTTPStatusError as e:
        print(f"HTTP Error: {e.response.status_code}", file=sys.stderr)
        print(e.response.text, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
