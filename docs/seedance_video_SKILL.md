---
name: seedance-video
description: Text-to-video generation using Volcengine Ark Seedance (Doubao/Jimeng) models
triggers:
  - pattern: "生成视频|文生视频|视频生成|做个视频|做视频"
    description: "检测视频生成请求"
  - pattern: "seedance|豆包视频|火山视频|doubao-seedance"
    description: "检测Seedance模型相关请求"
  - pattern: "用豆包|豆包生成|豆包做"
    description: "用户指定用豆包生成视频"
  - pattern: "即梦|jimeng|用即梦|即梦生成"
    description: "用户指定用即梦生成视频"
auto_invoke: false
examples:
  - "生成一个日落海边的视频"
  - "用Seedance生成小猫钓鱼的视频"
  - "文生视频：一只猫在睡觉"
  - "用豆包生成一个嵩口古镇的视频"
  - "用即梦做一段御剑飞行的视频"
  - "豆包图生视频，用这张场景图作为首帧"
---

# Volcengine Ark Seedance - Text to Video

Generate videos from text prompts using ByteDance's Seedance models via Volcengine Ark API.

## Setup

Set environment variables:
- `VOLCENGINE_ARK_API_KEY` - Your Volcengine Ark API key

### Example (PowerShell)
```powershell
[Environment]::SetEnvironmentVariable("VOLCENGINE_ARK_API_KEY", "your-api-key", "User")
# Or for current session only:
$env:VOLCENGINE_ARK_API_KEY = "your-api-key"
```

### Example (Bash)
```bash
export VOLCENGINE_ARK_API_KEY="your-api-key"
```

## Quick Start

```bash
python scripts/seedance_video.py generate \
  --prompt "A beautiful sunset over the ocean" \
  --ratio 16:9 \
  --duration 5
```

## Usage

```
seedance_video.py <command> [options]

Commands:
  generate    Generate a video from text prompt
  status      Query task status
  list        List available Seedance models

Generate Options:
  --prompt TEXT          Text prompt for video generation (optional when images provided)
  --model MODEL         Model ID (default: doubao-seedance-1-5-pro-251215)
  --ratio RATIO         Aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive; default: 16:9)
  --duration SECONDS    Video duration in seconds (default: 5)
  --resolution RES      Resolution (480p, 720p, 1080p, 4k, default: 720p)
  --watermark           Add watermark (default: false)
  --first-frame URL     First frame image URL (image-to-video)
  --last-frame URL      Last frame image URL (requires --first-frame)
  --reference-image URL Reference image URL (repeatable, multi-modal reference)
  --reference-audio URL Reference audio URL, wav/mp3 (repeatable, Seedance 2.0+)
  --generate-audio      Generate synchronized audio
  --no-audio            Generate silent video

Status Options:
  --task-id ID          Task ID to query (required)

List Options:
  --all                 Show all models (not just Seedance)
```

## Available Models

**Seedance 2.0 (Latest)**
- `doubao-seedance-2-0-fast-260128` - Fast version
- `doubao-seedance-2-0-260128` - Standard version

**Seedance 1.5**
- `doubao-seedance-1-5-pro-251215` - Professional version (recommended)
- `doubao-seedance-1-0-pro-fast-251015` - Fast version
- `doubao-seedance-1-0-pro-250528` - Professional version
- `doubao-seedance-1-0-lite-t2v-250428` - Lite version

## Image-to-Video (First / Last Frame)

```bash
# First frame only (image-to-video)
python scripts/seedance_video.py generate \
  --first-frame "https://example.com/first.png" \
  --prompt "让画面动起来" \
  --ratio adaptive

# First + last frame (首尾帧)
python scripts/seedance_video.py generate \
  --first-frame "https://example.com/first.png" \
  --last-frame "https://example.com/last.png" \
  --ratio adaptive \
  --duration 5
```

> Note: `--last-frame` must be used together with `--first-frame`. With frames, use `--ratio adaptive` to follow the first frame's dimensions.

## Multi-Modal Reference (全能参考)

```bash
python scripts/seedance_video.py generate \
  --reference-image "https://example.com/ref1.png" \
  --reference-image "https://example.com/ref2.png" \
  --prompt "参考图1的主体做参考图2的动作" \
  --ratio 16:9
```

> Reference images must be publicly accessible HTTPS URLs (not Base64). In the prompt, refer to them as 「图片1」「图片2」 by their order in `--reference-image`.

## Reference Audio (参考音频)

```bash
python scripts/seedance_video.py generate \
  --model doubao-seedance-2-0-260128 \
  --first-frame "https://example.com/first.png" \
  --reference-audio "https://example.com/voice.wav" \
  --prompt "「角色」说：\"你好\"，音色参考「音频1」" \
  --generate-audio
```

> Reference audio requires a Seedance 2.0+ model (`doubao-seedance-2-0-260128`). Format wav/mp3, 2-15s each, <15MB, max 3 audios for 2.0. Cannot be used alone — needs visual input. Refer to audios as 「音频1」「音频2」 in the prompt.

## Example Session

```bash
# Generate a video
python scripts/seedance_video.py generate \
  --prompt "一只可爱的小猫在河边钓鱼" \
  --ratio 16:9 \
  --duration 5

# Output: cgt-20260330200405-29g92

# Check status
python scripts/seedance_video.py status --task-id cgt-20260330200405-29g92

# Output:
# {
#   "status": "succeeded",
#   "video_url": "https://...",
#   ...
# }
```

## Notes

- Video generation is asynchronous. Use the returned task_id to poll for results.
- Video URLs are temporary and expire after 24-48 hours.
- Default duration is 5 seconds, maximum depends on the model tier.
