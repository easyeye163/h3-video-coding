# RunningHub AI 音乐与语音识别工作流

> 创建时间：2026-09-01
> 平台：RunningHub OpenAPI v2
> API Key 环境变量：`RUNNINGHUB_API_KEY`

---

## 一、AI 应用清单

| 应用 | App ID | 类型 | 用途 | 消耗 |
|------|--------|------|------|------|
| 语音转字幕 (ASR) | `2094729697874763777` | ai-app | 音频转 SRT 字幕 | 约 7-8 coins/次 |
| H3 全能参考视频生成 | `2090774740146413570` | ai-app | 图生视频 | 约 75 coins/15秒 |
| MiniMax Music3 音乐生成 | *(待确认)* | ai-app | 文本生成音乐 | - |

---

## 二、语音转字幕 (ASR) — 完整工作流

### 2.1 应用信息

- **App ID**: `2094729697874763777`
- **输入**: 音频文件（mp3 / flac / wav 等）
- **输出**: SRT 格式字幕文件 (.txt)
- **节点**: `nodeId: 25`, `fieldName: audio`
- **耗时**: 约 30-60 秒（2 分钟音频约 40 秒）
- **消耗**: 约 7-8 coins

### 2.2 调用方式

**前置条件**：音频文件需先上传到可公开访问的 URL（推荐 GitHub raw 链接）。

```bash
export RUNNINGHUB_API_KEY="你的API Key"

# 提交任务
curl --request POST 'https://www.runninghub.cn/openapi/v2/run/ai-app/2094729697874763777' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "nodeInfoList": [
    {
      "nodeId": "25",
      "fieldName": "audio",
      "fieldValue": "https://raw.githubusercontent.com/your-repo/path/to/audio.mp3",
      "description": "audio"
    }
  ],
  "instanceType": "default",
  "usePersonalQueue": "false"
}'
```

### 2.3 查询结果

```bash
curl --request POST 'https://www.runninghub.cn/openapi/v2/query' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "taskId": "你的任务ID"
}'
```

**成功响应示例：**
```json
{
  "taskId": "2094811181486395393",
  "status": "SUCCESS",
  "results": [
    {
      "url": "https://rh-images-xxx.cos.ap-beijing.myqcloud.com/.../subtitle_xxx.txt",
      "nodeId": "7",
      "outputType": "txt"
    }
  ],
  "usage": {
    "consumeCoins": "8",
    "taskCostTime": "39"
  }
}
```

### 2.4 输出格式 (SRT)

```
1
00:00:00,000 --> 00:00:05,000
第一句歌词

2
00:00:05,000 --> 00:00:10,000
第二句歌词
```

### 2.5 使用场景

| 场景 | 说明 |
|------|------|
| 歌曲歌词识别 | AI 生成音乐后，自动提取歌词文本 |
| 对话字幕生成 | 角色配音音频自动打时间轴字幕 |
| 视频字幕对齐 | 为成片自动生成 SRT 字幕文件 |

### 2.6 注意事项

1. **前奏/间奏部分**：无人声时可能识别出乱码或时间轴为 0，属于正常现象
2. **长音频**：目前测试 2 分 40 秒无压力，更长音频需自行测试
3. **COS 链接时效**：输出文件是临时 COS 链接，生成后需及时下载保存
4. **音频格式**：mp3 / flac / wav 均可，建议使用 GitHub raw 链接直接调用，无需上传

---

## 三、标准制作链路：AI 音乐 + 字幕

```
编写音乐描述（风格/情绪/歌词主题）
    ↓
调用 AI 音乐生成应用（MiniMax Music3 等）
    ↓
获取 mp3 文件 → 上传到 GitHub audio/music/ 目录
    ↓
调用 ASR 字幕应用识别歌词
    ↓
获取 SRT 字幕 → 校对润色歌词
    ↓
用于视频 BGM + 字幕展示
```

---

## 四、相关文件

| 文件 | 说明 |
|------|------|
| `audio/music/` | AI 生成音乐存放目录 |
| `docs/runninghub_video_curl模板.md` | H3 视频生成调用模板 |
| `docs/长期记忆_工作流节点配置.md` | 所有工作流节点总览 |
| `scripts/seedance_video.py` | 豆包 Seedance 视频生成脚本 |
