# 欢迎使用 RunningHub API，轻松调用 RunningHub 云端的 ComfyUI 工作流

## 1. 开始使用

### 注册用户

注册 RunningHub 账号并充值钱包后，即可开始使用 AI 应用 API 和 ComfyUI 工作流 API。
请注意：若您使用 消费级-会员 API Key，需拥有 基础版及以上会员 才能调用上述接口。
使用 企业级-共享 或 企业级-独占 API Key 的用户不受此限制。

### 获取您的 API Key

RunningHub 为每位用户自动生成一个独特的 32 位 API KEY

请妥善保存您的 API KEY，不要外泄，后续步骤将依赖此密钥进行操作

### 提交请求

提交 API 请求。RunningHub API 已为您处理 API Key，您只需提交请求即可

```curl
curl --location --request POST 'https://www.runninghub.cn/openapi/v2/run/ai-app/2088920592350277634' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "nodeInfoList": [
    {
      "nodeId": "17",
      "fieldName": "prompt",
      "fieldValue": "电影级 8K 超清，写实氛围感，年轻精致东方少女，黑色长卷发，通透冰蓝色眼眸，柔和水光妆容，身穿半透薄荷绿色薄纱长裙，怀抱着软乎乎的马宝宝毛绒玩偶，马宝宝玩偶造型圆润可爱，马年新宠，水下幽暗环境，青绿色光束丁达尔光效，漂浮细碎发光粒子，地面摆放通透水晶球，柔和逆光，皮肤通透质感，发丝带微光，布料通透飘逸，景深虚化，高级电影打光，细腻材质，画面静谧梦幻，画面中间一行手写风格的艺术字，写着”马年新宠“",
      "description": "prompt"
    }
  ],
  "instanceType": "default",
  "usePersonalQueue": "false"
}'
```

#### 请求参数说明

| 参数说明 | 类型 | 必填/可选 | AI 应用程序生成的结果。 |
| --- | --- | --- | --- |
| `nodeInfoList` | List | 必填 | 节点参数映射列表，用于动态修改工作流参数 |
| `instanceType` | String | 可选 | 指定运行实例的类型<br>default (24G显存), plus (48G显存) |
| `usePersonalQueue` | Boolean | 可选 | 是否使用个人独占队列 |
| `retainSeconds` | Integer | 可选 | 实例保留时长（秒）。仅企业共享 API Key 生效；任务成功结束后会在指定时长内优先复用同用户同工作流实例，减少冷启动与排队。该保留时段会产生额外费用，按实际保留时长计费。可选范围：10~180 秒。 |
| `webhookUrl` | String | 可选 | Webhook 回调地址，任务完成时会向该地址发送 POST 请求 |

#### 响应示例

```json
{
  "taskId": "2013508786110730241",
  "status": "RUNNING",
  "errorCode": "",
  "errorMessage": "",
  "results": null,
  "clientId": "f828b9af25161bc066ef152db7b29ccc",
  "promptTips": "{\"result\": true, \"error\": null, \"outputs_to_execute\": [\"4\"], \"node_errors\": {}}"
}
```

#### 响应字段说明

| 参数说明 | 类型 | AI 应用程序生成的结果。 |
| --- | --- | --- |
| `taskId` | String | 任务ID，用于后续查询任务状态 |
| `status` | String | 当前任务状态，常见状态：QUEUED (排队中), RUNNING (运行中), SUCCESS (成功), FAILED (失败) |
| `errorCode` | String | 错误码，仅在失败时返回 |
| `errorMessage` | String | 错误具体信息 |
| `results` | List | 生成结果（提交时为 null） |
| ├ `url` | String | 重要提醒：该链接有效期仅为 24 小时。任务生成结束后，请务必在此时间窗口内将视频文件下载或转存至您的服务器。逾期后链接将永久失效且无法恢复。 |
| ├ `nodeId` | String | 生成该结果的工作流节点 ID |
| ├ `outputType` | String | 文件扩展名 (如 png, mp4, txt) |
| └ `text` | String | 如果输出是纯文本，内容将显示在此字段 |
| `clientId` | String | 客户端会话ID，用于标识本次连接 |
| `promptTips` | String (JSON) | ComfyUI 后端的校验信息，包含需执行的节点ID等调试信息 |

### 查询结果与 Webhook

如果在提交时添加了 "webhookUrl": "https://example.com/webhook" 请求体参数，RunningHub 会在任务完成时向您的URL发送POST请求

#### 请求示例

```curl
curl --location --request POST 'https://www.runninghub.cn/openapi/v2/query' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "taskId": "${RUNNINGHUB_TASKID}"
}'
```

#### 响应示例

```json
{
  "taskId": "2013508786110730241",
  "status": "SUCCESS",
  "errorCode": "",
  "errorMessage": "",
  "failedReason": {},
  "usage": {
    "consumeMoney": null,
    "consumeCoins": null,
    "taskCostTime": "0",
    "thirdPartyConsumeMoney": null
  },
  "results": [
    {
      "url": "https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/b04e28cad0ee39193921a30a2eb4dc00/output/ComfyUI_00001_plhjr_1768892915.png",
      "nodeId": "2",
      "outputType": "png",
      "text": null
    }
  ],
  "clientId": "",
  "promptTips": ""
}
```

#### 响应字段说明

| 参数说明 | 类型 | AI 应用程序生成的结果。 |
| --- | --- | --- |
| `taskId` | String | 任务 ID |
| `status` | String | 任务最终状态，SUCCESS 表示生成成功 |
| `results` | List | 生成结果列表，包含图片、视频或文本等输出 |
| ├ `url` | String | 重要提醒：该链接有效期仅为 24 小时。任务生成结束后，请务必在此时间窗口内将视频文件下载或转存至您的服务器。逾期后链接将永久失效且无法恢复。 |
| ├ `nodeId` | String | 生成该结果的工作流节点 ID |
| ├ `outputType` | String | 文件扩展名 (如 png, mp4, txt) |
| └ `text` | String | 如果输出是纯文本，内容将显示在此字段 |
| `errorCode` | String | 错误码 (如有) |
| `errorMessage` | String | 错误信息 (如有) |
| `failedReason` | Object | ComfyUI 相关的失败原因 |
| `usage` | Object | 任务消耗信息 |
| ├ `thirdPartyConsumeMoney` | String | 三方API消费金额 |
| ├ `consumeMoney` | String | 运行时长消耗金额 |
| ├ `consumeCoins` | String | 运行消耗的RH币 |
| └ `taskCostTime` | String | 运行耗时（ComfyUI 工作流运行时长） |
### 文件上传

资源文件（如 imageUrls）参数支持传入文件 URL  

 

### 素材传递方式：GitHub raw URL（推荐）

**所有素材均可直接用 GitHub 公开仓库的 raw URL 传递，无需上传到 RunningHub。**

#### 优势
1. **免上传**：素材已在 GitHub 仓库，直接构造 raw URL 即可
2. **长期有效**：GitHub raw URL 永久有效（不像 RunningHub COS 链接 24h 失效）
3. **版本管理**：素材更新后 push 到 GitHub，URL 自动更新
4. **协作友好**：其他智能体可复用同一套素材 URL

#### GitHub raw URL 格式
```
https://raw.githubusercontent.com/{用户名}/{仓库名}/{分支}/{文件路径}
```

#### 中文路径处理
GitHub raw URL 支持中文路径，但需 URL 编码：
- `嵩口真实场景图` → `%E5%B5%A9%E5%8F%A3%E7%9C%9F%E5%AE%9E%E5%9C%BA%E6%99%AF%E5%9B%BE`
- `嵩口全景.png` → `%E5%B5%A9%E5%8F%A3%E5%85%A8%E6%99%AF.png`

**建议**：为避免 URL 编码复杂性，文件夹和文件名尽量用英文。

#### 验证 URL 可访问性
提交任务前先验证所有素材 URL 可公开访问：
```bash
curl -sI "https://raw.githubusercontent.com/.../image.png" | head -5
# 期望: HTTP/2 200, content-type: image/png
```

### 调用示例（EP1段1）

```bash
curl --location --request POST "https://www.runninghub.cn/openapi/v2/run/ai-app/2088878767828717570" \
--header "Content-Type: application/json" \
--header "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
--data-raw '{
  "nodeInfoList": [
    {
      "nodeId": "137",
      "fieldName": "image",
      "fieldValue": "https://raw.githubusercontent.com/.../scene.png",
      "description": "首帧图片-场景"
    },
    {
      "nodeId": "156",
      "fieldName": "image",
      "fieldValue": "https://raw.githubusercontent.com/.../character.png",
      "description": "角色参考-定妆图"
    },
    {
      "nodeId": "157",
      "fieldName": "audio",
      "fieldValue": "https://raw.githubusercontent.com/.../voice.flac",
      "description": "音色参考"
    },
    {
      "nodeId": "138",
      "fieldName": "value",
      "fieldValue": "subject_definitions:\n...\nsummary:\n...\nretention_analysis:\n...\ndetailed_description:\n...\noverall_soundscape:\n...\nnon_diegetic_music:\n...",
      "description": "完整6段式提示词"
    }
  ],
  "instanceType": "plus",
  "usePersonalQueue": "false"
}'
```

### 提示词格式（6段式）
详见 [docs/长期记忆_节点配置总结.md](长期记忆_节点配置总结.md) 的"分镜提示词标准模板"。

### 并发限制
RunningHub 有并发限制（错误码 421），建议串行提交任务，等前一个完成后再提交下一个。

