# RunningHub 视频生成 curl 命令模板（15秒 · GitHub直链版）

> App ID: `2090774740146413570`（MiniMax H3 全能参考视频生成）
> 时长：15 秒
> 比例：16:9
> ⚡ **重要：直接用 GitHub raw 完整链接作为 fieldValue，无需上传文件！**

---

## 一、提交任务（完整 curl 命令）

```bash
# ============================================================
#  素材直接使用 GitHub raw 完整链接（无需上传）
# ============================================================
# Picture 1: https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/images/xxx.png
# Picture 2: https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/images/xxx.png
# Picture 3: 未使用填 example.png
# Audio 1:   https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/audio/voices/xxx.flac
# Audio 2:   未使用则复用 Audio 1 的链接
#
# API Key 从环境变量获取：export RUNNINGHUB_API_KEY="你的key"
# ============================================================

curl --location --request POST 'https://www.runninghub.cn/openapi/v2/run/ai-app/2090774740146413570' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "nodeInfoList": [
    {
      "nodeId": "132",
      "fieldName": "value",
      "fieldValue": "15",
      "description": "时长（秒）"
    },
    {
      "nodeId": "115",
      "fieldName": "aspect_ratio",
      "fieldData": "[\"COMBO\", {\"default\": \"1:1 (Square)\", \"options\": [\"1:1 (Square)\", \"2:3 (Portrait Photo)\", \"3:2 (Photo)\", \"3:4 (Portrait Standard)\", \"4:3 (Standard)\", \"9:16 (Portrait Widescreen)\", \"16:9 (Widescreen)\", \"21:9 (Ultrawide)\"], \"tooltip\": \"The aspect ratio for the output dimensions.\", \"multiselect\": false}]",
      "fieldValue": "16:9 (Widescreen)",
      "description": "方向"
    },
    {
      "nodeId": "115",
      "fieldName": "megapixels",
      "fieldValue": "0.7000000000000001",
      "description": "分辨率"
    },
    {
      "nodeId": "137",
      "fieldName": "image",
      "fieldValue": "https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/images/songkou_characters/lin_xiaoxi_three_view.png",
      "description": "picture1（角色主图）"
    },
    {
      "nodeId": "138",
      "fieldName": "value",
      "fieldValue": "subject_definitions:\n<Picture 1> ...（6段式提示词）\n\nsummary:\n...",
      "description": "提示词（6段式 Full-Reference）"
    },
    {
      "nodeId": "166",
      "fieldName": "image",
      "fieldValue": "https://raw.githubusercontent.com/.../scene.png",
      "description": "picture2（场景参考图）"
    },
    {
      "nodeId": "165",
      "fieldName": "audio",
      "fieldValue": "https://raw.githubusercontent.com/.../voice.flac",
      "description": "audio1（音色参考）"
    },
    {
      "nodeId": "167",
      "fieldName": "image",
      "fieldValue": "example.png",
      "description": "picture3（未使用）"
    },
    {
      "nodeId": "168",
      "fieldName": "image",
      "fieldValue": "example.png",
      "description": "picture4（占位，不要改）"
    },
    {
      "nodeId": "169",
      "fieldName": "audio",
      "fieldValue": "https://raw.githubusercontent.com/.../voice.flac",
      "description": "audio2（未使用则复用audio1）"
    }
  ],
  "instanceType": "default",
  "usePersonalQueue": "false"
}'
```

---

## 二、查询任务结果

```bash
curl --location --request POST 'https://www.runninghub.cn/openapi/v2/query' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "taskId": "YOUR_TASK_ID"
}'
```

成功响应示例：
```json
{
  "taskId": "xxx",
  "status": "SUCCESS",
  "results": [
    {
      "url": "https://xxx.cos.ap-xxx.myqcloud.com/xxx.mp4",
      "outputType": "mp4"
    }
  ],
  "usage": {
    "consumeCoins": "75",
    "taskCostTime": "372"
  }
}
```

---

## 三、节点对应关系速查

| 节点 | nodeId | fieldName | 用途 | fieldValue 填法 |
|---|---|---|---|---|
| 时长 | 132 | value | 视频时长（秒） | "15" |
| 比例 | 115 | aspect_ratio | 画面比例 | "16:9 (Widescreen)" |
| 分辨率 | 115 | megapixels | 像素（保持默认） | "0.7000000000000001" |
| Picture 1 | 137 | image | 角色/主参考图 | GitHub raw 完整 URL |
| 提示词 | 138 | value | 6段式 Full-Reference 提示词 | 多行文本（\n 换行） |
| Picture 2 | 166 | image | 场景/副参考图 | GitHub raw 完整 URL |
| Audio 1 | 165 | audio | 音色参考1 | GitHub raw 完整 URL |
| Picture 3 | 167 | image | 第3张参考图 | 用则填URL，不用填"example.png" |
| Picture 4 | 168 | image | 占位（必须保留节点） | "example.png" |
| Audio 2 | 169 | audio | 音色参考2 | 用则填URL，不用则复用audio1的URL |

---

## 四、重要注意事项

1. **直接用 GitHub raw 链接**：image/audio 的 fieldValue 填完整的 GitHub raw URL，无需调用上传接口。
2. **中文路径需 URL 编码**：如 `嵩口全景.png` → `%E5%B5%A9%E5%8F%A3%E5%85%A8%E6%99%AF.png`。
3. **未使用节点必须保留**：picture3 / picture4 / audio2 节点不能删。
4. **图片占位保持 example.png**：picture3 / picture4 未使用时填 `"example.png"`。
5. **音频占位复用 audio1**：audio2 未使用时直接填 audio1 的链接（避免占位文件导致 errorCode 805）。
6. **COS 链接 24 小时失效**：生成成功后必须及时下载到本地 `videos/songkou_drama/` 目录。
7. **并发限制**：同时只能有有限个任务运行，超限返回 `errorCode: 421`。
8. **提示词换行**：JSON 中换行用 `\n` 转义。

---

## 五、标准制作链路

```
设置 RUNNINGHUB_API_KEY 环境变量
    ↓
复制对应段落的 curl 命令（GitHub 链接已填好）
    ↓
执行 curl 提交任务
    ↓
等待约 5-6 分钟，查询结果
    ↓
下载成片到 videos/songkou_drama/ 目录
```
