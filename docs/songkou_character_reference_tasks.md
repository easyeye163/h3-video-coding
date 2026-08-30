# 🎬 永泰嵩口古镇 - 主角三视图定妆照任务

## 📋 任务概述

使用**KREA-2-EDIT（图生图）API**，基于提供的写实风格照片生成专业三视图定妆照。

---

## 🎯 核心信息

| 项目 | 详情 |
|------|------|
| **角色名称** | 林小溪（主角）- 已更新为新形象 |
| **参考图** | 嵩口主角_写实定妆照参考图.jpg |
| **File Token** | IhdWbYIDOoNrZGxVQ5pcEJYPnne |
| **飞书云盘URL** | https://my.feishu.cn/file/IhdWbYIDOoNrZGxVQ5pcEJYPnne |
| **任务ID** | `2092979237681319938` |
| **使用API** | KREA-2-EDIT (App ID: 2088926295186034689) |
| **任务状态** | ✅ RUNNING（正在生成中） |

---

## 🎨 生成要求

### 输入参数

**节点1: 文本提示词 (nodeId: 160)**
```
Professional three-view character design sheet, 
front view, side view, back view, 
24-year-old Chinese man, based on reference photo, 
photorealistic, 8K ultra HD, cinematic lighting, 
clean white background, fashion illustration style, 
detailed clothing, pose reference sheet, 
professional character turnaround
```

**节点2: 参考图 (nodeId: 104)**
```
IhdWbYIDOoNrZGxVQ5pcEJYPnne (File Token)
```

### 期望输出

- ✅ 专业三视图构图（正面 + 侧面 + 背面）
- ✅ 保持原照片的人物特征和神态
- ✅ 写实摄影风格（非动漫）
- ✅ 8K超清画质
- ✅ 白色干净背景（便于抠图使用）

---

## ⏳ 执行状态

| 步骤 | 状态 | 说明 |
|------|------|------|
| 1️⃣ 上传图片到飞书云盘 | ✅ 完成 | Token: IhdWbYIDOoNrZGxVQ5pcEJYPnne |
| 2️⃣ 提交KREA-2-EDIT任务 | ✅ 完成 | Task ID: 2092979237681319938 |
| 3️⃣ 等待图片生成 | ⏳ 进行中 | 通常30-90秒 |
| 4️⃣ 下载生成结果 | ⏳ 待处理 | - |
| 5️⃣ 同步到作品列表 | ⏳ 待处理 | - |

---

## 🔗 重要链接

### RunningHub任务查询
```
https://www.runninghub.cn/console/task?taskId=2092979237681319938
```

### 飞书文件查看
```
https://my.feishu.cn/file/IhdWbYIDOoNrZGxVQ5pcEJYPnne
```

---

## 📥 下载生成结果

### 方法1: RunningHub网页（推荐）
1. 访问: https://www.runninghub.cn/console/task
2. 搜索任务ID: `2092979237681319938`
3. 下载生成的三视图图片

### 方法2: API查询
等待任务完成后，使用以下命令查询：
```bash
curl -s --location --request GET "https://www.runninghub.cn/openapi/v2/task/2092979237681319938" \
  --header "Authorization: Bearer [REDACTED_BEARER]"
```

---

## 💾 本地存储准备

### 创建目录
```bash
mkdir -p ./images/songkou_characters
```

### 建议文件名
```
lin_xiaoxi_reference_photo.jpg      # 原始参考图
lin_xiaoxi_three_view_gen.png       # 生成的三视图
```

---

## 🔄 后续操作

### 1. 验证生成结果
- [ ] 确认三视图包含正面、侧面、背面三个角度
- [ ] 检查人物特征是否与原照片一致
- [ ] 确认画质清晰度和风格符合要求

### 2. 下载并保存
- [ ] 从RunningHub下载生成的三视图
- [ ] 保存到本地目录
- [ ] 重命名为规范格式

### 3. 更新飞书作品列表
- [ ] 在作品列表中创建新记录
- [ ] 关联参考图和三视图
- [ ] 更新角色信息（使用新形象）

### 4. 应用到视频生成
- [ ] 将三视图关联到极简版本表的参考图字段
- [ ] 使用KREA-2-EDIT API生成各集视频片段
- [ ] 保持角色一致性

---

## 🎯 技术要点

### KREA-2-EDIT优势
- ✅ **人物一致性超高** - 最适合短剧制作
- ✅ **保留原照片特征** - 基于参考图生成
- ✅ **支持复杂场景** - 可添加背景、动作等
- ✅ **多节点输入** - 支持文本+图片双重控制

### 三视图标准格式
- **正面图**: 完整面部和身体正面展示
- **侧面图**: 通常为左侧面，展示轮廓
- **背面图**: 展示发型和服装背面设计
- **比例**: 全身比例准确，便于后续使用

---

## 📝 备注

- **参考图特点**: 这是一张非常优质的写实风格男性肖像照
- **生成预期**: 应该能保持人物的五官特征、气质和神态
- **用途**: 作为20集短剧主角的视觉基准，确保所有镜头中角色一致

---

**生成时间**: 2026-08-27  
**任务状态**: 处理中  
**预计完成**: 30-90秒内

---
*🎬 这是永泰嵩口古镇宣传短剧的核心资产之一！*
