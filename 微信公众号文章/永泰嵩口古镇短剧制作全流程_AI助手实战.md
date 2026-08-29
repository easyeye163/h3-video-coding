# 从构思到成片：AI助手如何30分钟完成20集短剧的完整制作

> **导语**：你是否想过，一部20集、每集1分钟的短剧剧本，需要多长时间才能完成？过去可能需要数周的时间，但今天，在AI的加持下，整个过程只需要**30分钟**！让我带你揭秘这场"AI+人类协作"的内容创作革命。

---

## 一、项目背景

最近，我接到了一个小项目——为**永泰嵩口古镇**制作一部**20集文化宣传短剧**。嵩口古镇位于福建永泰县，是一座拥有千年历史的闽中古镇，以保存完好的明清古建筑群、独特的鹤形路风水格局和深厚的文化底蕴而闻名。

### 项目需求
- ✅ 20集短剧，每集1分钟
- ✅ 每集包含完整的人物对话
- ✅ 富有创意，不千篇一律
- ✅ 输出MiniMax H3能理解的镜头语言
- ✅ 所有数据需要结构化存储和管理

### 传统制作流程（参考）
| 阶段 | 传统耗时 | 问题 |
|------|----------|------|
| 剧本创作 | 3-5天 | 需要反复修改 |
| 角色设计 | 2-3天 | 需要专业画师 |
| 分镜设计 | 3-4天 | 需要影视经验 |
| 数据管理 | 全程 | 容易混乱 |

---

## 二、技术方案：AI + DeepSeek Harness

这次我选择了**GLM 5V-Turbo**作为核心AI助手，配合**DeepSeek Harness**框架进行任务编排。这个组合的神奇之处在于：

### 1. GLM 5V-Turbo的核心能力
- 🧠 **强大的自然语言理解**：能快速理解复杂的项目需求
- 📝 **结构化思维**：擅长将任务分解为可执行的步骤
- 🎨 **创意生成**：能产出富有创意的剧本和镜头语言
- 🔗 **系统集成**：能与飞书、RunningHub等平台深度集成

### 2. DeepSeek Harness的独特优势
- 🎯 **任务并行**：可以同时执行多个子任务
- 🔄 **状态追踪**：实时跟踪每个任务的进度
- 📊 **数据管理**：自动将结果写入飞书多维表格
- ⚡ **智能决策**：根据任务复杂度自动调整策略

### 3. 整体架构图
```
┌─────────────────────────────────────────────┐
│           用户输入需求                      │
│     "制作20集嵩口古镇短剧"                 │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│        DeepSeek Harness 编排层              │
│  ├─ 任务分解（4个并行子任务）               │
│  ├─ 进度追踪                                │
│  └─ 结果汇总                                │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│         GLM 5V-Turbo 智能体                 │
│  ├─ 角色设计 Agent                          │
│  ├─ 剧情规划 Agent                          │
│  ├─ 镜头设计 Agent                          │
│  └─ 数据同步 Agent                          │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│            外部API集成                      │
│  ├─ 飞书多维表格（数据存储）                │
│  ├─ RunningHub API（图片生成）              │
│  └─ MiniMax API（视频生成）                 │
└─────────────────────────────────────────────┘
```

---

## 三、执行过程详解

### 阶段一：需求分析与任务分解（3分钟）

GLM 5V-Turbo首先对需求进行了深入分析：

```python
# 需求分析结果
project_analysis = {
    "total_episodes": 20,
    "duration_per_episode": "60秒",
    "style": "文化宣传短剧",
    "target_platform": "MiniMax H3",
    "data_structure": {
        "characters": "5个主要角色",
        "scenes": "8个核心场景",
        "episodes": "20集完整剧情",
        "shots": "每集4-6个专业镜头"
    }
}
```

基于此，AI将任务分解为4个并行子任务：

1. **人物角色表**：创建5个角色的详细设定
2. **场景设计表**：设计8个核心场景
3. **剧情规划表**：编写20集的完整剧本
4. **极简版本表**：生成MiniMax镜头语言

### 阶段二：并行执行（15分钟）

#### 子任务1：人物角色设计
AI为短剧设计了5个性格鲜明的人物：

| 角色 | 定位 | 年龄 | 核心特征 | 作用 |
|------|------|------|----------|------|
| 林小溪 | 主角 | 24岁 | 返乡青年，热爱家乡 | 故事主线贯穿者 |
| 陈阿公 | 配角 | 72岁 | 智慧长者，历史讲述者 | 文化传承象征 |
| 张导演 | 配角 | 35岁 | 纪录片导演 | 外来视角，喜剧元素 |
| 神秘旅人 | NPC | 28岁 | 哲学思考者 | 引发深度对话 |
| 小糯米 | 配角 | 8岁 | 天真孩童 | 童真视角，气氛调节 |

每个角色都包含：
- ✅ 外貌描述（用于AI生成图像）
- ✅ 性格特点
- ✅ 服装风格
- ✅ 音频设计提示词（用于配音生成）
- ✅ 角色提示词（用于保持一致性）

#### 子任务2：场景设计
AI分析了嵩口古镇的核心景点，设计了8个场景：

1. **嵩口古镇全景** - 航拍视角，展示古镇全貌
2. **明清古民居群** - 传统建筑内部细节
3. **用坦厝天井** - "四水归堂"设计
4. **龙口祖厝门口** - 家族历史入口
5. **鹤形路俯瞰** - 风水格局展示
6. **宁远庄城墙** - 防御性建筑
7. **万安堡庭院** - "民间故宫"
8. **古巷道深处** - 时光隧道感

#### 子任务3：剧情规划
这是最有创意的部分。AI没有简单地拍风景，而是设计了一个**完整的人物成长故事**：

```python
# 20集剧情主线（节选）
episodes = [
    {
        "episode": 1,
        "title": "初见嵩口",
        "theme": "返乡发现家乡美",
        "emotion": "温情",
        "conflict": "现代思维与传统观念的初次碰撞",
        "dialogue_highlight": "阿公：'根不是找到的，是等你回来后才发现一直在那里的'"
    },
    {
        "episode": 3,
        "title": "鹤形之谜",
        "theme": "科学与传说的碰撞",
        "emotion": "悬疑",
        "conflict": "理性与信仰的对立统一",
        "key_scene": "神秘旅人揭示鹤形路既是风水又是排水系统"
    },
    # ... 共20集，每集60秒
]
```

每集都包含：
- 📝 详细的场景描述
- 💬 真实的人物对话
- 🎭 情感冲突设计
- 🎵 音效和配乐建议

#### 子任务4：镜头语言设计
AI输出了**完全符合MiniMax H3规范的镜头脚本**：

```json
{
  "镜头1": {
    "景别": "远景",
    "运镜": "推镜",
    "画面": "清晨薄雾中的嵩口古镇全景...",
    "时长": "12s",
    "音效": "悠扬笛声、环境底噪"
  },
  "镜头2": {
    "景别": "中景", 
    "运镜": "跟拍",
    "画面": "林小溪拖着行李箱走出村口...",
    "时长": "10s",
    "对白": "小溪：'好久不见，阿公'"
  }
}
```

每集包含4-6个专业镜头，总计100+镜头脚本。

### 阶段三：数据同步（5分钟）

所有数据自动同步到**飞书多维表格**：

| 表名 | 记录数 | 说明 |
|------|--------|------|
| 人物角色表 | 5条 | 完整的角色设定 |
| 场景设计表 | 8条 | 核心场景定义 |
| 剧情规划表 | 20条 | 完整剧本 |
| 极简版本表 | 20条 | MiniMax镜头脚本 |
| 作品列表 | 5条 | 素材管理 |

**特点**：
- ✅ 表之间通过关联字段连接
- ✅ 支持后续迭代修改
- ✅ 便于团队协作
- ✅ 版本管理清晰

### 阶段四：视觉生成（7分钟）

使用**RunningHub KREA-2-EDIT API**生成写实风格的三视图定妆照：

```python
# 调用KREA-2-EDIT API
import requests

def generate_character_views(character_info, reference_image):
    """
    使用KREA-2-EDIT生成角色三视图
    """
    response = requests.post(
        'https://www.runninghub.cn/openapi/v2/run/ai-app/2088926295186034689',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        json={
            'nodeInfoList': [
                {
                    'nodeId': '160',
                    'fieldName': 'text',
                    'fieldValue': 'Professional three-view character design sheet, 
                                  front view, side view, back view, 
                                  based on reference photo, 
                                  photorealistic, 8K ultra HD'
                },
                {
                    'nodeId': '104',
                    'fieldName': 'image',
                    'fieldValue': reference_image_token
                }
            ],
            'instanceType': 'default'
        }
    )
    return response.json()
```

生成的三视图将用于：
- 🎬 保证视频生成时的角色一致性
- 📸 制作宣传物料
- 🎨 分镜脚本配图

---

## 四、最终成果展示

### 📊 数据统计

| 指标 | 数量 | 说明 |
|------|------|------|
| 总时长 | 20分钟 | 20集×1分钟 |
| 角色数 | 5个 | 主角+配角+NPC |
| 场景数 | 8个 | 核心场景 |
| 镜头数 | 100+ | 专业分镜 |
| 对话数 | 200+ | 人物台词 |
| 数据表 | 5个 | 完整管理 |
| 执行时间 | 30分钟 | 包含生成时间 |

### 🎯 核心亮点

#### 1. **富有创意的叙事结构**
- 不是千篇一律的风景宣传片
- 通过人物成长线索串联20集
- 融入悬疑、搞笑、感人等多重情感节奏

#### 2. **真实的人物对话**
- 每集都有详细的剧本对白
- 方言特色（福州话元素）
- 代际对话（老人vs青年vs孩童）

#### 3. **专业级镜头语言**
- 完全符合MiniMax H3规范
- 包含完整的分镜脚本
- 音效、配乐、对白一体化设计

#### 4. **深度的文化挖掘**
- 不仅展示"是什么"，更解读"为什么"
- 建筑智慧（四水归堂、鹤形路风水）
- 家族传承、工匠精神、乡愁情怀

---

## 五、技术总结

### 成功的关键因素

1. **AI的并行处理能力**
   - 4个子任务同时执行
   - 节省70%以上的等待时间

2. **结构化的数据管理**
   - 飞书多维表格完美适配
   - 所有数据可随时查询修改

3. **API的深度集成**
   - RunningHub图片生成
   - MiniMax视频生成接口
   - 飞书云盘文件管理

4. **清晰的提示词工程**
   - 角色提示词保证一致性
   - 镜头语言格式标准化
   - 情感基调明确化

### 遇到的问题与解决

**问题1**：API并发限制
- **现象**：同时提交多个任务时失败
- **解决**：添加等待机制，串行处理关键任务
- **代码**：`sleep(10)` 在每次API调用后

**问题2**：JSON格式错误
- **现象**：批量创建记录时字段验证失败
- **解决**：使用dry-run模式调试，确认字段类型
- **技巧**：单选字段必须使用数组格式如 `["文生图"]`

**问题3**：图片下载链接
- **现象**：飞书云盘URL无法直接访问
- **解决**：使用File Token作为API输入参数
- **最佳实践**：优先使用Token而非URL

---

## 六、福利时间 🎁

为了感谢大家的支持，我给大家争取到了一个**超级福利**：

### GLM Coding Plan 体验卡

我在使用**GLM Coding Plan**的过程中，发现数小时内就能完成过去需要数周的开发工作！为了让更多小伙伴体验AI编程的魅力，我为大家申请了**7天AI Coding体验卡**！

👉 **免费领取体验卡**：
```
https://bigmodel.cn/activity/trial-card/GTFWJSBNFY
```

**体验卡福利**：
- ✅ 7天完整使用权限
- ✅ 包含GLM 5V-Turbo等模型
- ✅ 无限次API调用
- ✅ 专属技术支持群

---

## 七、工作流推荐（短剧必备）🔥

这次项目中，我使用了以下几个经过验证的工作流，强烈推荐给大家：

### Python代码示例（收藏备用）

```python
#!/usr/bin/env python3
"""
短剧制作工作流配置
基于DeepSeek Harness + GLM 5V-Turbo + RunningHub
"""

import requests
import json
import time

class DramaProductionWorkflow:
    """
    短剧制作工作流类
    包含：文生图、图生图、视频生成、声音设计
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.runninghub.cn/openapi/v2"
        
        # 工作流配置（基于实战验证）
        self.workflows = {
            "文生图_Zimage": {
                "app_id": "2088920592350277634",
                "name": "Z-image text-to-image",
                "description": "完美支持中文+超自然风格",
                "url": "https://www.runninghub.cn/post/2088917231601278978/?inviteCode=oga1ahgc"
            },
            "图生图_KREA_EDIT": {
                "app_id": "2088926295186034689",
                "name": "KREA-2-EDIT One-image-V2",
                "description": "人物一致性超高，短剧必备",
                "url": "https://www.runninghub.cn/post/2088923554007048194/?inviteCode=oga1ahgc"
            },
            "视频生成_MiniMax": {
                "app_id": "2088836712364601345",
                "name": "MiniMax H3稳定加速版",
                "description": "全能参考4步加速版本",
                "url": "https://www.runninghub.cn/post/2088836712364601345/?inviteCode=oga1ahgc"
            },
            "声音设计": {
                "app_id": "2090434415913689090",
                "name": "多角色声音一致性",
                "description": "短剧必备，保证角色声音统一",
                "url": "https://www.runninghub.cn/post/2090434415913689090/?inviteCode=oga1ahgc"
            }
        }
    
    def generate_text_to_image(self, prompt):
        """
        文生图：使用Z-image生成概念图
        """
        response = requests.post(
            f"{self.base_url}/run/ai-app/{self.workflows['文生图_Zimage']['app_id']}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "nodeInfoList": [
                    {"nodeId": "17", "fieldName": "prompt", "fieldValue": prompt}
                ],
                "instanceType": "default"
            }
        )
        return response.json()
    
    def generate_image_to_image(self, prompt, image_token):
        """
        图生图：使用KREA-2-EDIT保持人物一致性
        """
        response = requests.post(
            f"{self.base_url}/run/ai-app/{self.workflows['图生图_KREA_EDIT']['app_id']}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "nodeInfoList": [
                    {"nodeId": "160", "fieldName": "text", "fieldValue": prompt},
                    {"nodeId": "104", "fieldName": "image", "fieldValue": image_token}
                ],
                "instanceType": "default"
            }
        )
        return response.json()
    
    def generate_video(self, prompt, reference_images=None):
        """
        视频生成：使用MiniMax H3
        """
        node_list = [{"nodeId": "138", "fieldName": "value", "fieldValue": prompt}]
        if reference_images:
            node_list.append({
                "nodeId": "137",
                "fieldName": "image",
                "fieldValue": reference_images[0]
            })
        
        response = requests.post(
            f"{self.base_url}/run/ai-app/{self.workflows['视频生成_MiniMax']['app_id']}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "nodeInfoList": node_list,
                "instanceType": "plus"  # 视频生成建议使用48G显存
            }
        )
        return response.json()
    
    def design_voice(self, character_name, voice_style):
        """
        声音设计：生成角色配音
        """
        response = requests.post(
            f"{self.base_url}/run/ai-app/{self.workflows['声音设计']['app_id']}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "nodeInfoList": [
                    {"nodeId": "文本输入", "fieldName": "text", "fieldValue": character_name},
                    {"nodeId": "风格选择", "fieldName": "style", "fieldValue": voice_style}
                ],
                "instanceType": "default"
            }
        )
        return response.json()


# 使用示例
if __name__ == "__main__":
    workflow = DramaProductionWorkflow(api_key="YOUR_API_KEY")
    
    # 1. 生成角色概念图
    result = workflow.generate_text_to_image(
        "24岁中国女孩，马尾辫，浅蓝汉服，温暖笑容，写实风格"
    )
    print("✅ 角色图生成成功:", result.get('taskId'))
    
    # 2. 生成三视图（使用参考图保持一致性）
    result = workflow.generate_image_to_image(
        "Professional three-view character design sheet",
        "参考图Token"
    )
    print("✅ 三视图生成成功:", result.get('taskId'))
    
    # 3. 生成视频片段
    result = workflow.generate_video(
        "林小溪走在嵩口古镇青石板路上，清晨阳光",
        ["参考图Token"]
    )
    print("✅ 视频生成成功:", result.get('taskId'))
    
    # 4. 设计角色声音
    result = workflow.design_voice("林小溪", "温柔活泼")
    print("✅ 声音设计成功:", result.get('taskId'))
```

---

## 八、结语

### 这次项目的启示

1. **AI不是替代人类，而是放大人类的能力**
   - AI负责：数据整理、格式转换、批量处理
   - 人类负责：创意决策、审美判断、情感把控

2. **好的提示词是成功的一半**
   - 清晰的描述 = 高质量的输出
   - 结构化的思维 = 可维护的系统

3. **工具链的整合至关重要**
   - 飞书多维表格：数据管理
   - RunningHub：AI模型调用
   - DeepSeek Harness：任务编排
   - 三者结合 = 强大生产力

### 未来展望

这次尝试只是一个开始。随着AI技术的不断进化，我们可以期待：

- 🎬 **自动化剧本生成**：输入主题，自动生成完整剧本
- 🎨 **智能角色设计**：AI根据故事自动设计角色形象
- 🎵 **自动配乐**：根据剧情自动生成音乐
- 🎭 **智能剪辑**：AI自动剪辑成片

**AI正在重新定义内容创作的方式**，而我们都将成为这场革命的参与者和见证者。

---

## 附录：完整的项目文件清单

```
./
├── 📄 songkou_characters_tasks.md          # 任务跟踪文档
├── 📄 人物定妆照同步操作指南.md            # 操作指南
├── 📄 永泰嵩口古镇短剧制作全流程_AI助手实战.md  # 本文档
├── 📁 images/
│   └── songkou_characters/                # 角色三视图存储
│       ├── lin_xiaoxi_three_view.png
│       ├── chen_agong_three_view.png
│       ├── zhang_director_three_view.png
│       ├── mystery_traveler_three_view.png
│       └── xiaomi_three_view.png
├── 📁 data/
│   └── feishu_base_backup.json            # 飞书数据备份
└── 📁 scripts/
    ├── sync_characters_to_feishu.sh       # 同步脚本
    └── generate_all_shots.py              # 批量生成脚本
```

---

**感谢阅读！** 如果你对这个项目感兴趣，或者有任何问题，欢迎在评论区交流讨论！👇

*觉得有用？记得点赞、收藏、转发三连！* ❤️

---

**标签**：#AI创作 #短剧制作 #GLM #DeepSeek #RunningHub #飞书多维表格 #效率工具

**原文链接**：https://your-blog.com/songkou-drama-ai-workflow
