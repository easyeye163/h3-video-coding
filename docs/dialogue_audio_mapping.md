# 对话音频映射方案

## 现有音频文件

| 文件名 | 大小 | 适用角色 |
|--------|------|----------|
| 20岁女生_清冷.flac | 112K | Audio1 神秘女子（清冷古风）|
| 20岁女生.flac | 437K | Audio2 现代女子（温暖甜美）|
| 03_活泼女生.flac | 295K | 备选Audio2 |

---

## 音频分配方案

### Audio1 - 神秘女子（古代）
**音色**：清冷、古风、高贵
**源文件**：`20岁女生_清冷.flac`

### Audio2 - 现代女子
**音色**：温暖、甜美、友善
**源文件**：`20岁女生.flac`

---

## 对话分段计划

### Shot 4 - 触摸倒影

| 时间 | 角色 | 台词 | 音频段 |
|------|------|------|--------|
| 30-33s | Audio1 | "这是……哪里？" | 清冷.flac 前3秒 |
| 33-36s | Audio2 | "这里是21世纪的上海。" | 女生.flac 前3秒 |
| 36-39s | Audio1 | "21世纪……我在做梦吗？" | 清冷.flac 中间3秒 |

### Shot 5 - 咖啡厅相遇

| 时间 | 角色 | 台词 | 音频段 |
|------|------|------|--------|
| 40-43s | Audio1 | "那……这是什么机器？" | 清冷.flac 后段 |
| 43-46s | Audio2 | "这是咖啡机，你要尝尝吗？" | 女生.flac 后段 |
| 46-49s | Audio1 | "咖啡……是什么味道？" | 清冷.flac 补充 |

### Shot 6 - 时空交汇

| 时间 | 角色 | 台词 | 音频段 |
|------|------|------|--------|
| 50-53s | Audio1 | "我想……回到我的时代。" | 清冷.flac 结尾 |
| 53-56s | Audio2 | "没关系，我们会再见的。" | 女生.flac 结尾 |
| 56-60s | Audio1 | "谢谢你……朋友。" | 清冷.flac 收尾 |

---

## FFmpeg 合并方案

```bash
# 步骤1：提取对话片段
ffmpeg -i 20岁女生_清冷.flac -ss 0 -t 3 output/s1_s4_a1.flac
ffmpeg -i 20岁女生.flac -ss 0 -t 3 output/s1_s4_a2.flac
# ... 更多片段

# 步骤2：合并对话轨道
ffmpeg -i a1.flac -i a2.flac -filter_complex "[0:a][1:a]amix=inputs=2:duration=first" output/dialogue_track.flac

# 步骤3：合并到视频
ffmpeg -i video.mp4 -i dialogue_track.flac -c:v copy -c:a aac output/video_with_dialogue.mp4
```

