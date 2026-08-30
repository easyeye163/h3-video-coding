# AI短视频制作全攻略：如何用DeepSeek Harness保持角色一致性？

> 从策划到成片，全程使用DeepSeek Harness + Agnes-2.5-Flash Agent自动化完成

---

## 前言：当AI开始讲故事

最近我尝试用AI制作了一部短剧《马年新宠》，过程中最大的挑战不是生成素材，而是**如何让角色在不同场景中保持一致性**。

经过数十次迭代，我总结出了一套完整的工作流。今天就把这些经验分享给各位创作者。

---

## 一、角色一致性：视觉篇

### 1.1 为什么角色会"变脸"？

很多创作者会遇到这个问题：生成的视频里，角色的脸型、发型、服装总在变，甚至同一镜头内人物风格都不统一。

根本原因：**提示词中对角色的描述不够精确，AI自由发挥空间过大**。

### 1.2 解决方案：三级锁定机制

#### 第一级：角色三视图（核心）

我使用Z-image工作流生成角色定妆照：

```json
{
  "nodeId": "17",
  "fieldName": "prompt",
  "fieldValue": "Three-view character design sheet, young Asian woman, front view, side view, full body view, clean white background, fashion illustration style, detailed clothing design, professional character turnaround, 8K ultra detailed"
}
```

**关键要点：**
- 必须生成正面、侧面、全身三个角度
- 服装要详细描述（颜色、款式、材质）
- 使用"character turnaround"关键词确保一致性

#### 第二级：首帧图片锁定

在视频生成时，使用**精确的首帧图片**而非角色图作为起始：

```
❌ 错误做法：首帧用三视图
   → 模型困惑，服装场景混乱

✅ 正确做法：首帧用场景图
   → 角色从参考图中提取外观
   → 场景一致性有保障
```

节点配置：
```json
{
  "nodeId": "137",
  "fieldName": "image",
  "fieldValue": "场景图片URL"  // 图书馆/海滩等
}
```

#### 第三级：提示词中的"不变量"声明

在提示词中加入`retention_analysis`段落：

```text
retention_analysis:
人物不变量：图2女性的面部、黑发、服装、体型必须全程保持一致
  → 不出现换装、变形、多余手指或五官扭曲

场景不变量：图1的海滩布局、海水位置、椰子树保持稳定
  → 海浪持续涌动

风格不变量：真人实拍质感，热带度假风，阳光明媚
  → 冷调为主、冷暖交织
```

---

## 二、声音一致性：音频设计

### 2.1 为什么音频很重要？

声音是角色的"身份证"。同一个角色在不同场景中说话，音色、语调必须一致，否则观众会出戏。

### 2.2 音频设计流程

#### 第一步：生成参考音频

使用RunningHub的音频工作流生成角色声音：

```json
{
  "appId": "2090440149267210242",
  "nodeId": "3",
  "fieldName": "prompt",
  "fieldValue": "20-24岁清冷柔弱女声，音色温柔灵动，音量偏轻，情绪淡，易碎感。"
}
```

#### 第二步：保存音色特征

将音频链接记录到飞书多维表格：

| 角色 | 音频风格 | 文件路径 | 远程链接 |
|------|----------|----------|----------|
| 现代女生 | 清冷柔弱女声 | agent/audio/20岁女生_清冷.flac | [查看](...) |
| 东方少女 | 活泼俏皮女声 | agent/audio/03_活泼女生.flac | [查看](...) |

#### 第三步：视频生成时引用音频

```json
{
  "nodeId": "165",
  "fieldName": "audio",
  "fieldValue": "https://.../20岁女生_清冷.flac"
}
```

并在提示词中明确：
```text
<Audio 1> is a reference audio for voice timbre, vocal identity,
speaking tone, rhythm, intonation, and lip-sync pacing.
```

---

## 三、工作流选择：选对工具事半功倍

### 3.1 各工作流定位

| 工作流 | appId | 用途 | 关键节点 |
|--------|-------|------|----------|
| Z-image | 2088920592350277634 | 文生图 | nodeId=17, fieldName=prompt |
| KREA-2-EDIT | 2088926295186034689 | 图生图 | nodeId=1 |
| AnimateDiff | 2088844222551121921 | 视频生成 | 137/138/157/156 |
| 高级视频 | 2090774740146413570 | 高质量视频 | 137/138/165/166 |
| 音频生成 | 2090440149267210242 | TTS | nodeId=3/5 |

### 3.2 节点配置速查

#### Z-image文生图（正确姿势）
```json
{
  "nodeId": "17",
  "fieldName": "prompt",
  "fieldValue": "提示词内容"
}
```

#### 高级视频工作流（完整版）
```json
{
  "nodeId": "132", "fieldName": "value", "fieldValue": "10",      // 时长
  "nodeId": "115", "fieldName": "aspect_ratio", "fieldValue": "16:9 (Widescreen)",
  "nodeId": "115", "fieldName": "megapixels", "fieldValue": "0.7",
  "nodeId": "137", "fieldName": "image", "fieldValue": "场景图URL",
  "nodeId": "166", "fieldName": "image", "fieldValue": "角色图URL",
  "nodeId": "165", "fieldName": "audio", "fieldValue": "音频URL",
  "nodeId": "138", "fieldName": "value", "fieldValue": "完整提示词"
}
```

---

## 四、提示词工程：黄金公式

### 4.1 六段式提示词结构

```
1. subject_definitions     → 角色/场景职责分离
2. summary                 → 一句话概括情绪弧线
3. retention_analysis      → 不变量锁定
4. detailed_description    → 分镜时间轴+机位+动作
5. overall_soundscape      → 环境音设计
6. non_diegetic_music      → 配乐设计
```

### 4.2 完整示例

```text
subject_definitions:
<Picture 1> 严格负责场景环境：热带海滩，阳光明媚，碧绿海水...
<Picture 2> 严格负责女性角色：黑发披肩，明亮大眼睛，现代休闲装...

summary:
一段10秒度假vlog场景，年轻女性站在海滩上打招呼。

retention_analysis:
人物不变量：图2女性的面部、黑发、服装必须全程一致
场景不变量：图1的海滩布局、海水位置保持稳定
风格不变量：真人实拍质感，热带度假风

detailed_description:
[Shot 1]（0s-10s）
海滩中景，固定机位，摄像机正面拍摄。
她微笑着看向镜头，用清晰自然的普通话说道：
「今天天气真好，你也来这里度假吗？」
说完轻轻点头，露出友好微笑。

overall_soundscape:
海浪拍打沙滩，海风轻拂，鸟鸣声，对白清晰。

non_diegetic_music:
轻快钢琴配乐，像阳光洒在海面上的感觉。
```

---

## 五、DeepSeek Harness：自动化神器

### 5.1 什么是DeepSeek Harness？

DeepSeek Harness是一个强大的Agent平台，支持：
- 多步骤自动化执行
- 上下文记忆管理
- 外部API调用
- 文件操作能力

### 5.2 本次项目中的体现

```python
# 自动执行视频生成
task_id = run_runninghub_workflow(
    app_id="2090774740146413570",
    node_info=[...]
)

# 自动查询任务状态
while True:
    status = query_task(task_id)
    if status == "SUCCESS":
        download_video(status['url'])
        break
    sleep(60)

# 自动更新飞书多维表格
update_feishu_base(
    table_id="tbl9hKFVTAGrCzlA",
    record={
        "任务名称": "海边沙滩-视频生成",
        "远程链接": video_url,
        "本地目录": local_path
    }
)
```

### 5.3 Agnes-2.5-Flash的Agent能力

在本次项目中，Agnes作为Agent展现了以下能力：

| 能力 | 应用场景 |
|------|----------|
| **上下文记忆** | 记住数十次迭代的经验教训 |
| **工具调用** | 自动调用RunningHub API、飞书API |
| **文件管理** | 自动下载、分类、重命名素材 |
| **错误处理** | 自动识别错误码并尝试修复 |
| **知识沉淀** | 将经验写入长期记忆文档 |

---

## 六、实战案例：海边度假视频

### 6.1 输入素材

| 类型 | 文件 | 用途 |
|------|------|------|
| 场景图 | beach_vacation.png | 首帧锁定 |
| 角色图 | 三视图_现代女生.png | 人物锁定 |
| 音频 | 20岁女生_清冷.flac | 声音锁定 |

### 6.2 执行过程

```
1. 使用Z-image生成场景图（7币）
2. 使用音频工作流生成角色声音（8币）
3. 使用高级视频工作流生成视频（104币）
4. 自动下载到本地
5. 自动更新飞书多维表格
```

### 6.3 最终效果

- 首帧像素级对齐场景
- 角色服装、面部全程一致
- 口型与音频精确同步
- 环境音、配乐层次分明

---

## 七、经验总结

### 7.1 核心经验

1. **先定角色，再定场景**
   - 先生成角色三视图
   - 再生成场景图
   - 最后生成视频

2. **提示词要具体**
   - 不要说"一个女孩"
   - 要说"黑发披肩、明亮大眼睛、白色上衣"

3. **不变量声明是关键**
   - 在提示词中明确哪些元素不能变
   - 用`retention_analysis`段落锁定

4. **音频优先**
   - 先生成角色声音
   - 视频生成时引用音频
   - 确保口型同步

### 7.2 常见错误

| 错误 | 后果 | 解决方案 |
|------|------|----------|
| 首帧用角色图 | 场景混乱 | 首帧用场景图 |
| 提示词缺少约束 | 角色漂移 | 加入不变量声明 |
| 未引用音频 | 口型不同步 | 添加Audio 1引用 |
| 工作流选错 | API报错 | 查阅节点配置文档 |

---

## 八、完整工具链

```
策划阶段：
  DeepSeek Harness + Agnes Agent
  → 生成策划案、分镜表

素材阶段：
  Z-image → 角色图、场景图
  音频工作流 → 角色声音

生成阶段：
  高级视频工作流 → 最终视频

管理阶段：
  飞书多维表格 → 素材管理
  本地文件系统 → 文件存储
```

---

## 结语

AI视频制作的难度不在于生成单个镜头，而在于**保持角色和场景的一致性**。

通过正确的提示词结构、合适的工作流选择、以及完善的素材管理，我们可以让AI真正成为创作伙伴。

希望这篇文章能帮助你少走弯路，高效创作！

---

**关于作者**

本文使用DeepSeek Harness + Agnes-2.5-Flash Agent完成，全程自动化执行API调用、文件管理、表格更新等操作。

如需了解更多细节，欢迎留言交流！
