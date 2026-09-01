# Volcengine Ark Seedance - Text to Video

使用字节跳动火山引擎的 Seedance 模型进行文生视频。

## 安装

1. 设置环境变量：

```bash
# Windows
set VOLCENGINE_ARK_API_KEY=your_api_key_here

# Linux/macOS
export VOLCENGINE_ARK_API_KEY=your_api_key_here
```

2. 安装依赖：

```bash
pip install requests
```

## 使用方法

### 生成视频

```bash
python scripts/seedance_video.py generate \
  --prompt "一只可爱的小猫在河边钓鱼" \
  --ratio 16:9 \
  --duration 5
```

### 查询任务状态

```bash
python scripts/seedance_video.py status --task-id cgt-20260330200405-29g92
```

### 列出可用模型

```bash
python scripts/seedance_video.py list
```

### 首尾帧图生视频

```bash
# 仅首帧
python scripts/seedance_video.py generate \
  --first-frame "https://example.com/first.png" \
  --prompt "让画面动起来" \
  --ratio adaptive

# 首帧 + 尾帧
python scripts/seedance_video.py generate \
  --first-frame "https://example.com/first.png" \
  --last-frame "https://example.com/last.png" \
  --ratio adaptive \
  --duration 5
```

> `--last-frame` 必须与 `--first-frame` 一起使用；传帧时建议 `--ratio adaptive` 以跟随首帧尺寸。

### 参考图（全能参考）

```bash
python scripts/seedance_video.py generate \
  --reference-image "https://example.com/ref1.png" \
  --reference-image "https://example.com/ref2.png" \
  --prompt "参考图1的主体做参考图2的动作" \
  --ratio 16:9
```

> 参考图需为公开 HTTPS URL（不支持 Base64），提示词中用「图片1」「图片2」按顺序引用。

### 参考音频

```bash
python scripts/seedance_video.py generate \
  --model doubao-seedance-2-0-260128 \
  --first-frame "https://example.com/first.png" \
  --reference-audio "https://example.com/voice.wav" \
  --prompt "「角色」说：\"你好\"，音色参考「音频1」" \
  --generate-audio
```

> 参考音频需 Seedance 2.0+ 模型；格式 wav/mp3，单个 2–15 秒、<15MB，2.0 最多 3 个；不能单独使用，需配合视觉素材；提示词中用「音频1」「音频2」按顺序引用。

## 可用模型

| 模型 ID | 说明 |
|---------|------|
| doubao-seedance-2-0-fast-260128 | 2.0 快速版 |
| doubao-seedance-2-0-260128 | 2.0 标准版 |
| doubao-seedance-1-5-pro-251215 | 1.5 专业版 (推荐) |
| doubao-seedance-1-0-pro-fast-251015 | 1.0 快速版 |

## 参数说明

- `--prompt`: 视频描述文本 (传图时可省略)
- `--model`: 模型ID (默认: doubao-seedance-1-5-pro-251215)
- `--ratio`: 宽高比 (16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive; 默认: 16:9)
- `--duration`: 视频时长(秒) (默认: 5)
- `--resolution`: 分辨率 (480p, 720p, 1080p, 4k; 默认: 720p)
- `--watermark`: 添加水印 (默认: false)
- `--poll`: 自动轮询结果 (默认: false)
- `--first-frame`: 首帧图片 URL (图生视频)
- `--last-frame`: 尾帧图片 URL (需配合 `--first-frame`)
- `--reference-image`: 参考图 URL (可重复传入，多模态参考)
- `--reference-audio`: 参考音频 URL，wav/mp3 (可重复传入，需 Seedance 2.0+)
- `--generate-audio`: 生成同步音频
- `--no-audio`: 生成无声视频

## 注意事项

- 视频生成是异步的，返回 task_id 后需要轮询查询结果
- 视频链接有时效性，通常24-48小时后失效
- 不同模型支持的时长和分辨率可能不同
