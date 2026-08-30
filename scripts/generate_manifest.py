#!/usr/bin/env python3
"""扫描 audio/images/videos 目录，生成 manifest.json 供动态看板使用"""
import os, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT_MAP = {
    '.png': 'images', '.jpg': 'images', '.jpeg': 'images', '.gif': 'images', '.webp': 'images', '.svg': 'images',
    '.mp4': 'videos', '.webm': 'videos', '.mov': 'videos',
    '.flac': 'audio', '.mp3': 'audio', '.wav': 'audio', '.aac': 'audio', '.ogg': 'audio',
}

def scan():
    result = {'images': [], 'videos': [], 'audio': []}
    for dir_name in ['audio', 'images', 'videos']:
        dir_path = os.path.join(ROOT, dir_name)
        if not os.path.isdir(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in EXT_MAP:
                    continue
                full = os.path.join(root, f)
                rel = os.path.relpath(full, ROOT)
                size = os.path.getsize(full)
                result[EXT_MAP[ext]].append({'path': rel, 'name': f, 'size': size})
    # sort by name desc
    for k in result:
        result[k].sort(key=lambda x: x['name'], reverse=True)
    result['updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result['total'] = sum(len(v) for v in [result['images'], result['videos'], result['audio']])
    return result

if __name__ == '__main__':
    manifest = scan()
    out = os.path.join(ROOT, 'manifest.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f'manifest.json 已生成: {out}')
    print(f'  图片: {len(manifest["images"])} 个')
    print(f'  视频: {len(manifest["videos"])} 个')
    print(f'  音频: {len(manifest["audio"])} 个')
    print(f'  总计: {manifest["total"]} 个')
