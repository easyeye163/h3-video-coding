# RunningHub AI API 技能指南

## 概述
RunningHub 是一个 AI 应用平台，提供多种 AI 模型 API 服务，包括文生图、图生图、图片编辑、视频生成等。

## 核心能力
1. **线上API验证**：快速测试工作流效果
2. **智能体编排**：通过自然语言驱动复杂工作流（配合 DeepSeek Harness）
3. **本地部署**：导出工作流后无限免费运行

## 配套智能体框架

### DeepSeek Harness
- **发布**: 2026 年 8 月 13 日
- **协议**: MIT 开源
- **理念**: "一切皆插件"
- **核心公式**: `Model + Harness = Agent`
- **GitHub**: https://github.com/deepseek-ai/deepseek-harness
- **特点**: 插件化智能体框架，可自由组合模型、工具、技能

## API 基础信息

### 端点
```
POST https://www.runninghub.cn/openapi/v2/run/ai-app/{appId}
```

### 认证
- Header: `Authorization: Bearer {API_KEY}`
- API Key 存储在环境变量 `RUNNINGHUB_API_KEY` 中

### 请求格式
```json
{
  "nodeInfoList": [
    {
      "nodeId": "节点ID",
      "fieldName": "字段名称",
      "fieldValue": "字段值",
      "description": "字段描述"
    }
  ],
  "instanceType": "default",
  "usePersonalQueue": "false"
}
```

### 响应格式
```json
{
  "taskId": "任务ID",
  "status": "RUNNING",
  "clientId": "客户端ID",
  "errorCode": "",
  "errorMessage": ""
}
```

## 可用 API 列表

### 1. KREA-2-EDIT (图生图/图片编辑)
- **App ID**: `2088926295186034689`
- **类型**: Image-to-Image (图生图)
- **特点**: 人物一致性超高，适合短剧制作
- **输入节点**:
  | nodeId | fieldName | description |
  |--------|-----------|-------------|
  | 160 | text | 提示词 |
  | 104 | image | 参考图 |

### 2. Z-image (文生图)
- **App ID**: `2088920592350277634`
- **类型**: Text-to-Image (文生图)
- **特点**: 完美支持中文字符和超自然风格
- **输入节点**:
  | nodeId | fieldName | description |
  |--------|-----------|-------------|
  | 17 | prompt | 提示词 |

### 3. AnimateDiff (文生视频/图生视频)
- **App ID**: `2088844222551121921`
- **类型**: Video Generation (视频生成)
- **特点**: 支持口播配音、人物动态化
- **输入节点**:
  | nodeId | fieldName | description |
  |--------|-----------|-------------|
  | 138 | value | 详细英文提示词 |
  | 137 | image | 参考图URL |

> **注意**: 视频生成任务显存消耗大，建议使用 `instanceType: "plus"` (48G显存)

## 使用示例

### 执行 API 请求
```bash
curl --location --request POST 'https://www.runninghub.cn/openapi/v2/run/ai-app/{appId}' \
--header "Content-Type: application/json" \
--header "Authorization: Bearer {API_KEY}" \
--data-raw '{"nodeInfoList":[{"nodeId":"17","fieldName":"prompt","fieldValue":"提示词内容"}],"instanceType":"default","usePersonalQueue":"false"}'
```

### 注意事项
1. JSON 中的中文引号需要转义或使用英文引号
2. 确保 API Key 已正确设置
3. 返回的 taskId 可用于查询任务状态
