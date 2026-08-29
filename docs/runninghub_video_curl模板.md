# RunningHub 视频生成 curl 命令模板（15秒）

> App ID: `2090774740146413570`（MiniMax H3 全能参考视频生成）
> 时长：15 秒
> 比例：16:9

---

## 一、提交任务（完整 curl 命令）

```bash
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
      "fieldValue": "PICTURE1_UPLOADED_FILENAME.png",
      "description": "picture1（角色主图）"
    },
    {
      "nodeId": "138",
      "fieldName": "value",
      "fieldValue": "subject_definitions:\n<Picture 1> 严格负责女性角色的身份与造型：林小溪，24岁返乡青年，黑长低马尾，空气刘海，浅蓝交领汉服上衣配白边，蓝色牛仔阔腿裤，白色帆布鞋，温柔微笑。全片不得漂移。\n<Picture 2> 仅负责场景空间环境与机位参照：大樟溪穿镇而过，白墙黑瓦明清古民居群依山傍水，航拍俯瞰全貌。以图2为准确定建筑群纵深、溪流走向与晨雾氛围，不参与人物造型。\n<Audio 1> 为 <Subject 1>（S1）的音色参考：温柔活泼的年轻女声。\n\nsummary:\n15秒嵩口古镇文化宣传质感镜头。清晨薄雾笼罩下的嵩口古镇全貌（场景参照<Picture 2>嵩口全景），航拍俯瞰到地面跟拍，S1在场，暖光初现，乡愁与期待交织。\n\nretention_analysis:\n<Picture 1>（角色锚点）：完全保留 - 林小溪的身份、发型、服装保持一致。\n<Subject 1>（全程出镜）：完全保留 - 身份与服装保持一致。\n<Audio 1>：参考 - 目标说话人遵循参考音色，不复制信号。\n\ndetailed_description:\n目标视频采用电影感、文学化文化宣传风格，柔和暖光，嵩口薄雾永恒氛围，白墙黛瓦徽派建筑，大樟溪晨雾，轻度去饱和SLOG质感。\n[Shot 1]（0s-7s）中景跟拍，<Picture 1> 参照的 <Subject 1>（S1）林小溪拖着行李箱走在青石板巷道上，薄雾飘过白墙黛瓦屋顶，她四下张望，轻声感叹<d>嵩口……我回来了。</d>[Shot 2]（7s-15s）中近景，她停下脚步仰望古镇屋檐，薄雾捕捉到第一缕暖光，眼眶微红，嘴角带着释然微笑。\n\noverall_soundscape:\n远处鸟鸣与柔和的河雾环境声。\n\nnon_diegetic_music:\n古筝独奏，温柔而苏醒。",
      "description": "提示词（6段式 Full-Reference）"
    },
    {
      "nodeId": "166",
      "fieldName": "image",
      "fieldValue": "PICTURE2_UPLOADED_FILENAME.png",
      "description": "picture2（场景参考图）"
    },
    {
      "nodeId": "165",
      "fieldName": "audio",
      "fieldValue": "AUDIO1_UPLOADED_FILENAME.flac",
      "description": "audio1（音色参考）"
    },
    {
      "nodeId": "167",
      "fieldName": "image",
      "fieldValue": "example.png",
      "description": "picture3（占位，不要改）"
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
      "fieldValue": "AUDIO1_UPLOADED_FILENAME.flac",
      "description": "audio2（未使用则复用audio1文件，避免占位文件报错）"
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
  ]
}
```

---

## 三、上传文件（获取 fieldValue 用的文件名）

```bash
# 上传图片
curl --location --request POST 'https://www.runninghub.cn/openapi/v2/media/upload/binary' \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--form 'file=@/path/to/your/image.png'

# 上传音频
curl --location --request POST 'https://www.runninghub.cn/openapi/v2/media/upload/binary' \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--form 'file=@/path/to/your/audio.flac'
```

成功响应示例：
```json
{
  "data": {
    "download_url": "d34ca5c9e4e711e7ec71b514fbaaf3b59e3ecf18286545ab6ec05de42c186ef2.png"
  }
}
```

> ⚠️ 取 `download_url` 的**文件名部分**（即最后一个 `/` 后面的内容）作为 `fieldValue`。如果 `download_url` 本身就没有路径，直接用整个值。

---

## 四、节点对应关系速查

| 节点 | nodeId | fieldName | 用途 | 示例值 |
|---|---|---|---|---|
| 时长 | 132 | value | 视频时长（秒） | "15" |
| 比例 | 115 | aspect_ratio | 画面比例 | "16:9 (Widescreen)" |
| 分辨率 | 115 | megapixels | 像素（保持默认） | "0.7000000000000001" |
| Picture 1 | 137 | image | 角色/主参考图 | 上传后的文件名.png |
| 提示词 | 138 | value | 6段式 Full-Reference 提示词 | 多行文本（\n 换行） |
| Picture 2 | 166 | image | 场景/副参考图 | 上传后的文件名.png |
| Audio 1 | 165 | audio | 音色参考1 | 上传后的文件名.flac |
| Picture 3 | 167 | image | 占位（保持example.png） | "example.png" |
| Picture 4 | 168 | image | 占位（保持example.png） | "example.png" |
| Audio 2 | 169 | audio | 未使用时复用audio1文件 | 同audio1的文件名 |

---

## 五、重要注意事项

1. **未使用的节点必须保留**：picture3 / picture4 / audio2 即使不用，也不能删除节点。
2. **图片占位保持 example.png**：picture3 / picture4 未使用时保持 `"example.png"`。
3. **音频占位复用 audio1**：audio2 未使用时直接填 audio1 的文件名（避免默认占位文件导致 errorCode 805）。
4. **COS 链接 24 小时失效**：生成成功后必须及时下载到本地 `videos/songkou_drama/` 目录。
5. **并发限制**：同时只能有有限个任务运行，超限返回 `errorCode: 421`，关键任务串行处理，每次调用间隔 `sleep(10)`。
6. **提示词换行**：JSON 中换行用 `\n` 转义。
7. **GET 查询接口已知问题**：部分情况下可能返回 `PARAMS_INVALID`，需从控制台手动取回结果。

---

## 六、标准制作链路

```
上传 Picture1（角色图） ──┐
上传 Picture2（场景图） ──┤
上传 Audio1（音色）   ──┴──→ 提交视频生成任务 → 轮询查询结果 → 下载成片
```
