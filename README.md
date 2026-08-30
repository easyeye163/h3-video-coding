# h3-video-coding · AI 短剧制作工作流

> 基于 **MiniMax H3 六段式提示词 + RunningHub API + 飞书多维表格** 的 AI 文化宣传短剧自动化制作体系。

📊 **[嵩口项目可视化看板](./songkou-dashboard.html)** — 素材进度、分集状态、角色场景一览

---

## 短剧必备工作流（自用）

1、 Z-image text-to-image-文生图（完美支持中文字+超自然）【Agent必备】 
工作流地址： `https://www.runninghub.cn/post/2088917231601278978/?inviteCode=oga1ahgc` 

2、KREA-2-EDIT-One-image-V2 单图编辑工作流【短剧必备】 
工作流地址： `https://www.runninghub.cn/post/2088923554007048194/?inviteCode=oga1ahgc` 

3、MiniMax H3稳定加速版（全能参考4步加速版本） 
工作流地址： `https://www.runninghub.cn/post/2088836712364601345/?inviteCode=oga1ahgc` 

4、声音设计（用于短剧多角色声音一致性） 
工作流地址： `https://www.runninghub.cn/post/2090434415913689090/?inviteCode=oga1ahgc`

---

## ⚠️ 必读文档

**所有项目制作都基于上述 4 个 RunningHub 工作流。开始任何制作前，必须先阅读技能文档：**

**[docs/长期记忆_节点配置总结.md](docs/长期记忆_节点配置总结.md)**

该文档包含：
- **API 使用说明**（提交任务端点、查询结果端点、文件上传端点、并发限制）
- **4 个工作流的节点配置**（appId + nodeId + fieldName，已验证正确）
- **6 段式提示词标准模板**（MiniMax H3 Full-Reference 格式）
- **场景设计表**与分镜提示词模板

> 不会调用这些工作流 = 无法制作任何内容。所有智能体协作前必读。

---

## 项目简介

本项目是"永泰嵩口古镇 20 集 AI 文化宣传短剧"的制作工程，通过 AI 工作流完成从剧本、分镜、角色定妆、视频生成到成片的全链路自动化。

- **目标平台**：MiniMax H3（镜头语言＝6 段式 Full-Reference 英文提示词）
- **规格**：20 集 × 1 分钟（每集 4 段 × 15 秒）
- **角色**：5 人 ｜ **场景**：8 处 ｜ **镜头**：80 段

## 技术栈

| 层级 | 组件 | 用途 |
|---|---|---|
| 编排 | DeepSeek Harness | 任务分解/并行/追踪 |
| 智能体 | GLM 5V-Turbo | 角色/剧情/镜头/数据同步 |
| 图像 | RunningHub Z-image（文生图）/ KREA-2-EDIT（图生图） | 场景图/角色三视图（人物一致性） |
| 视频 | RunningHub AnimateDiff / MiniMax H3 | 6 段式提示词成片 |
| 音频 | RunningHub 多角色声音一致性 | 角色配音 |
| 数据 | 飞书多维表格 | 5 张表结构化存储 |

## 目录结构与功能约束

| 路径 | 功能 | 约束 / 说明 |
|---|---|---|
| `1、【实施中】嵩口宣传项目.md` | **项目主文档（入口）** | 单一权威源，进度/资产状态/瑕疵/版本记录以此为准 |
| `scripts/` | Python / Shell 脚本 | 自动化任务，内部用绝对路径引用资产 |
| `data/` | JSON 数据 | 结构化制作数据（剧本/分镜/批量创建载荷） |
| `docs/` | 项目文档 | 制作单/提示词模板/工作流配置/对话脚本/长期记忆 |
| `audio/` | 音频资产 | `voices/` 存嵩口角色音色；根目录存其他音色库 |
| `images/` | 图片资产 | `songkou_characters/` 存嵩口角色三视图；`character-sheet/` 存其他角色设计稿 |
| `videos/` | 视频成片 | `songkou_drama/` 存嵩口短剧成片；`downloaded/` 存素材 |
| `微信公众号文章/` | 营销文章 | 微信推文草稿与实战心得 |
| `知识库素材/` | 文化资料 | 嵩口历史/赶集文化/古建筑等背景资料 |
| `.workbuddy/` | 工作记忆 | **已 gitignore**：含 API 状态/taskId 等敏感信息，不入库 |

## .gitignore 规则

- `.workbuddy/` 全部排除（含敏感信息：API key 记录、taskId、lark-cli 凭据）
- 其余文件均可提交（含音视频/图片等二进制资源，单文件 < 50MB）

## 协作约定

1. **主文档优先**：所有进度/状态/瑕疵更新先写入 [1、【实施中】嵩口宣传项目.md](./1、【实施中】嵩口宣传项目.md)，它是单一权威源
2. **绝对路径**：脚本和文档内引用资产用绝对路径 `./...`，避免移动后失效
3. **RunningHub 注意**：
   - COS 云端链接 24h 失效，成片需及时下载到本地目录
   - GET 查询接口坏（`PARAMS_INVALID`），成片需从[控制台](https://www.runninghub.cn/console/task)手动取回
   - 有并发限制，关键任务串行处理，每次调用后 `sleep(10)`
4. **节点配置**：以 [docs/长期记忆_工作流节点配置.md](./docs/长期记忆_工作流节点配置.md) 为准（已实测验证）
5. **提示词规范**：6 段式 Full-Reference
   - `subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`
6. **文件命名约定**：
   - 成片：`嵩口短剧_第N集_标题_vX.mp4`
   - 三视图：`xxx_three_view.png`（如 `lin_xiaoxi_three_view.png`）
   - 音色：`songkou_xxx.flac`
7. **素材清单更新（重要）**：每次新增/删除 audio/images/videos 文件后，必须运行以下命令更新 `manifest.json`，否则动态看板无法显示最新素材：
   ```bash
   python3 scripts/generate_manifest.py
   git add manifest.json && git commit -m "Update manifest"
   ```
   - 动态看板 `songkou-dashboard-dynamic.html` 从 CDN 读取 `manifest.json` 自动渲染素材
   - 不更新 manifest.json = 看板看不到新素材

## 动态看板使用流程

动态看板 [`songkou-dashboard-dynamic.html`](./songkou-dashboard-dynamic.html) 用于实时浏览仓库内最新素材（图片/视频/音频），无需启动服务器，浏览器双击打开即可。

### 1. 访问方式

- **本地**：直接双击 `songkou-dashboard-dynamic.html` 用浏览器打开
- **在线**：可通过 GitHub Pages 或 jsdelivr CDN 直接访问该 HTML
- 打开后自动加载最新素材，右上角「刷新」按钮可手动重载

### 2. 数据源机制（双保险）

看板按以下顺序尝试读取素材清单，任一成功即渲染：

| 顺序 | 数据源 | URL | 说明 |
|---|---|---|---|
| 主 | CDN manifest.json | `https://cdn.jsdelivr.net/gh/easyeye163/h3-video-coding@main/manifest.json` | 最可靠，由 `generate_manifest.py` 生成 |
| 备 | GitHub Trees API | `https://api.github.com/repos/easyeye163/h3-video-coding/git/trees/main?recursive=1` | 当 CDN 失败时回退，但有时不可访问 |

> CDN 不可访问时自动回退到 GitHub API；两者皆失败则提示「加载失败」。

### 3. 素材访问

所有素材（图片/视频/音频）均通过 jsdelivr CDN 加载，URL 格式：

```
https://cdn.jsdelivr.net/gh/easyeye163/h3-video-coding@main/{相对路径}
```

例如：`https://cdn.jsdelivr.net/gh/easyeye163/h3-video-coding@main/images/songkou_characters/lin_xiaoxi_three_view.png`

看板中每张卡片的链接即为该 CDN 地址，可点击直接打开原始文件。

### 4. 新增素材后如何让看板看到

```
[1] 把素材文件放入 audio/ images/ videos/ 对应目录
        ↓
[2] 运行：python3 scripts/generate_manifest.py   # 重新扫描生成 manifest.json
        ↓
[3] git add manifest.json && git commit -m "Update manifest" && git push
        ↓
[4] 等待 jsdelivr CDN 缓存刷新（约 10 分钟 ~ 12 小时）
        ↓
[5] 打开/刷新看板，自动读取最新 manifest.json 渲染
```

> ⚠️ 不更新 `manifest.json` = 看板只能依赖 GitHub API 回退，且新素材不会出现在主数据源中。

### 5. CDN 缓存刷新说明

- jsdelivr 对 GitHub 仓库有缓存延迟（通常 10 分钟 ~ 12 小时）
- 急需立即刷新可访问：`https://purge.jsdelivr.net/gh/easyeye163/h3-video-coding@main/manifest.json`
- GitHub API 路径无缓存，但受 API 速率限制且有时不可访问

---

## 标准制作链路（单集 4 步）

```
[1] 文生图（Z-image）            → 场景图/概念图        images/songkou_epN/
        ↓
[2] 图生图（KREA-2-EDIT）        → 角色三视图/定妆图     images/songkou_characters/
        ↓
[3] 图生视频（MiniMax H3）       → 6段式提示词成片      videos/songkou_drama/
        ↓
[4] 音频设计（多角色声音一致性） → 对白+旁白+配乐        audio/voices/
```

## RunningHub 工作流速查

| 工作流 | App ID | 关键节点 |
|---|---|---|
| Z-image 文生图 | `2088920592350277634` | `17`=prompt |
| KREA-2-EDIT 图生图 | `2088926295186034689` | `1`=prompt |
| AnimateDiff 单图视频 | `2088844222551121921` | `137`首帧/`138`提示词/`157`音频/`156`角色/`165`Audio/`166`Pic2/`132`时长/`115`比例 |
| 多图像视频生成 | `2088878767828717570` | `137`首帧/`157`音频/`156`角色/`138`提示词 |
| 音频生成 | `2090440149267210242` | `3`声音设计/`5`TTS文本 |

## 当前进度（2026-08-29）

- **剧本+提示词**：100%（20 集 × 4 段 6 段式提示词）
- **成片**：5%（仅 EP1 完成 v2）
- **角色定妆图**：林小溪✅ / 神秘旅人⏳已提交 / 陈阿公⏳已提交v2 / 张导演❌ / 小糯米❌
- 详见主文档第三章"项目实施进度看板"

## 关联文档

- [1、【实施中】嵩口宣传项目.md](./1、【实施中】嵩口宣传项目.md) — 项目主文档（进度/资产/瑕疵/版本）
- [docs/嵩口EP3_鹤形之谜_极简制作单.md](./docs/嵩口EP3_鹤形之谜_极简制作单.md) — EP3 试制链路
- [docs/嵩口提示词优化_v2.md](./docs/嵩口提示词优化_v2.md) — v2 提示词规范
- [docs/长期记忆_工作流节点配置.md](./docs/长期记忆_工作流节点配置.md) — RunningHub 节点配置（已验证）
- [docs/runninghub-skill.md](./docs/runninghub-skill.md) — RunningHub API 技能指南
