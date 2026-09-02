# 当千年古镇遇上AI：嵩口IP如何用MiniMax M3+ASR实现音乐视频自动化

> 一座藏在福建深山里的千年古镇，一段用AI谱写的国风旋律，一场从歌词到视频的全链路自动化实验。

---

## 嵩口古镇：从现实到IP的跨越

嵩口，福建永泰的一座千年古镇，鹤形路蜿蜒如仙鹤展翅，万安堡巍然耸立诉说着岁月沧桑。这里有青石板路、夯土老墙、古码头的落日，也有我们正在打造的仙侠IP——林小溪的故事。

但今天要说的，不是古镇的历史，而是一个更有趣的话题：**如何用AI给一座古镇写歌、打字幕、拍视频？**

答案是三个工具的组合拳：

- **MiniMax H3** — 文本直接生成带人声的完整歌曲
- **ASR语音识别** — 自动把音乐转成带时间轴的字幕
- **H3全能参考视频** — 参考音乐+场景图生成音画同步视频

整条链路跑通后，从写歌词到出成片，只需要十几分钟。

---

## 第一步：让AI给嵩口写首歌

你没看错，现在的AI已经能直接根据歌词文本生成完整的歌曲了——有旋律、有编曲、有人声演唱。

我们给嵩口IP写了一首中国风慢摇，歌名就叫《画舫摇》。歌词里藏着朱雀桥、乌衣巷、秦淮夜——这些意象和嵩口的古镇意境完美契合。

用的是 **MiniMax H3 音乐生成**模型，输入一段包含曲风描述和完整歌词的文本，它就能输出一首2-3分钟的歌曲。

```python
"""
工作流一：MiniMax H3 AI音乐生成
基于嵩口IP主题，文本直接生成带人声的完整歌曲
"""
import requests
import json
import time
import os

# ===== 配置 =====
API_KEY = os.environ.get("RUNNINGHUB_API_KEY")
APP_ID = "2094807049065558018"  # MiniMax H3 音乐生成
BASE_URL = "https://www.runninghub.cn/openapi/v2"

# ===== 1. 编写歌曲提示词 =====
# 标准结构：【曲风构想】+ Intro + Verse + Chorus + Bridge + Outro
song_prompt = """【曲风构想】
中慢速中国风慢摇，深沉的 808 Bass 驱动着四拍子鼓点，
古筝与二胡在迷幻的电音延迟中交织，营造出古今交错的夜游意境。

(Intro 前奏)
(深沉的 Kick 鼓点低频敲击，伴随水波声与采样极重延迟的古筝单音)

(Verse 1 主歌一)
夜泊秦淮 岸边的灯火渐次熄灭
笙歌散尽 谁在船头 泼墨成雪
朱雀桥边 岁月被风 轻轻掀开一页
你挑灯的侧脸 模糊了 整个时节

(Chorus 副歌)
画舫摇呀摇 摇晃着千年的寂寞
你在故事的角落 哼着哪首江南的歌
风吹过 雕花的木窗 吹散了功名与承诺
只留下 纸上那一抹 晕开的执着

(Outro 尾声)
(鼓点逐渐抽离，只剩 Bass 低鸣与古筝余音缓缓 Fade Out)
秦淮夜… 慢摇过客…"""

# ===== 2. 提交音乐生成任务 =====
def generate_music(prompt, cfg=1.7):
    """调用 MiniMax H3 生成音乐"""
    url = f"{BASE_URL}/run/ai-app/{APP_ID}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "nodeInfoList": [
            {
                "nodeId": "55",
                "fieldName": "text",
                "fieldValue": prompt,
                "description": "歌曲风格及歌词"
            },
            {
                "nodeId": "49",
                "fieldName": "cfg",
                "fieldValue": str(cfg),
                "description": "提示词强度"
            }
        ],
        "instanceType": "default",
        "usePersonalQueue": "false"
    }

    resp = requests.post(url, headers=headers, json=payload)
    data = resp.json()
    task_id = data.get("taskId")
    print(f"音乐生成任务已提交: {task_id}")
    return task_id

# ===== 3. 轮询任务状态 =====
def query_task(task_id, interval=30, max_wait=600):
    """查询任务状态，直到完成或超时"""
    url = f"{BASE_URL}/query"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    for i in range(max_wait // interval):
        resp = requests.post(url, headers=headers, json={"taskId": task_id})
        data = resp.json()
        status = data.get("status")

        if status == "SUCCESS":
            result_url = data["results"][0]["url"]
            coins = data["usage"]["consumeCoins"]
            cost_time = data["usage"]["taskCostTime"]
            print(f"任务完成！耗时 {cost_time}s，消耗 {coins} coins")
            return result_url
        elif status == "FAILED":
            print(f"任务失败: {data.get('errorMessage')}")
            return None

        print(f"第 {i+1} 次轮询，状态: {status}，等待 {interval}s...")
        time.sleep(interval)

    print("任务超时")
    return None

# ===== 4. 下载音乐文件 =====
def download_file(url, save_path):
    """下载文件到本地"""
    resp = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(resp.content)
    print(f"已保存到: {save_path}")

# ===== 主流程 =====
if __name__ == "__main__":
    # 生成嵩口主题曲
    task_id = generate_music(song_prompt, cfg=1.7)
    music_url = query_task(task_id)

    if music_url:
        download_file(music_url, "audio/music/songkou_theme.mp3")
        print("音乐生成完成！")
```

**几个实用的小技巧：**

- **曲风描述要具体**：别只写"中国风"，要写清楚配器（古筝、二胡、808 Bass）、节奏（四拍子）、效果（Delay延迟），AI生成的编曲会更精准
- **cfg参数调一调**：提示词强度建议在 1.5-2.0 之间，太低容易跑调，太高会很机械
- **歌词结构要规范**：标注清楚 Verse / Chorus / Bridge / Outro，AI会自动对应段落情绪变化

---

## 第二步：ASR自动识别歌词时间轴

音乐生成好了，但要做视频，还需要知道每句歌词对应的时间点——这就是ASR（语音识别）的用武之地。

你可能会说，歌词是我写的，我还不知道内容吗？

知道内容是一回事，知道**每句歌在第几秒开始、第几秒结束**是另一回事。ASR给你的不是歌词文本，而是精确到毫秒的 **SRT时间轴字幕**。

有了时间轴，你才能：
- 给视频加同步歌词字幕
- 根据副歌段落选最有画面感的15秒
- 让画面变化踩准音乐的节奏点

```python
"""
工作流二：ASR语音转字幕
自动识别音乐中的歌词并生成SRT时间轴字幕
"""
import requests
import json
import time
import os

# ===== 配置 =====
API_KEY = os.environ.get("RUNNINGHUB_API_KEY")
APP_ID = "2094729697874763777"  # ASR 语音转字幕
BASE_URL = "https://www.runninghub.cn/openapi/v2"

# ===== 1. 提交ASR识别任务 =====
def asr_submit(audio_url):
    """提交音频进行语音识别，返回任务ID"""
    url = f"{BASE_URL}/run/ai-app/{APP_ID}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "nodeInfoList": [
            {
                "nodeId": "25",
                "fieldName": "audio",
                "fieldValue": audio_url,
                "description": "audio"
            }
        ],
        "instanceType": "default",
        "usePersonalQueue": "false"
    }

    resp = requests.post(url, headers=headers, json=payload)
    data = resp.json()
    task_id = data.get("taskId")
    print(f"ASR任务已提交: {task_id}")
    return task_id

# ===== 2. 轮询并获取SRT字幕 =====
def asr_query(task_id, interval=10, max_wait=120):
    """查询ASR结果，返回SRT字幕内容"""
    url = f"{BASE_URL}/query"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    for i in range(max_wait // interval):
        resp = requests.post(url, headers=headers, json={"taskId": task_id})
        data = resp.json()
        status = data.get("status")

        if status == "SUCCESS":
            srt_url = data["results"][0]["url"]
            # 下载SRT内容
            srt_content = requests.get(srt_url).text
            print(f"识别完成！共 {srt_content.count('-->')} 句歌词")
            return srt_content
        elif status == "running":
            print(f"识别中... 第 {i+1} 次轮询")
            time.sleep(interval)
        elif status == "FAILED":
            print(f"识别失败: {data.get('errorMessage')}")
            return None
        else:
            print(f"状态: {status}")
            time.sleep(interval)

    print("任务超时")
    return None

# ===== 3. 解析SRT，提取副歌段落 =====
def parse_srt(srt_content):
    """解析SRT字幕，返回每句的时间和文本"""
    lines = srt_content.strip().split("\n")
    subtitles = []
    i = 0
    while i < len(lines):
        if lines[i].strip().isdigit():  # 序号行
            time_line = lines[i + 1]  # 时间行
            start_str, end_str = time_line.split(" --> ")
            text = lines[i + 2]  # 文本行
            subtitles.append({
                "start": start_str.strip(),
                "end": end_str.strip(),
                "text": text.strip()
            })
            i += 3
        else:
            i += 1
    return subtitles

# ===== 4. 截取15秒副歌片段 =====
def find_chorus_segment(subtitles, keyword="画舫摇呀摇", duration=15):
    """找到包含关键词的段落，截取15秒片段的起止时间"""
    for sub in subtitles:
        if keyword in sub["text"]:
            start_seconds = srt_time_to_seconds(sub["start"])
            return start_seconds, start_seconds + duration
    return None, None

def srt_time_to_seconds(srt_time):
    """SRT时间格式转秒数：00:01:23,456 -> 83.456"""
    h, m, s_ms = srt_time.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

# ===== 主流程 =====
if __name__ == "__main__":
    # 音频文件先传到GitHub，用raw链接调用
    audio_url = "https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/audio/music/songkou_theme.mp3"

    # 提交识别
    task_id = asr_submit(audio_url)
    srt_content = asr_query(task_id)

    if srt_content:
        # 保存SRT文件
        with open("audio/music/songkou_theme.srt", "w", encoding="utf-8") as f:
            f.write(srt_content)

        # 解析字幕
        subs = parse_srt(srt_content)
        print(f"\n识别到 {len(subs)} 句歌词：")
        for s in subs:
            print(f"  [{s['start']}] {s['text']}")

        # 找到副歌段落
        start, end = find_chorus_segment(subs, keyword="画舫摇呀摇")
        if start:
            print(f"\n副歌片段: {start:.1f}s - {end:.1f}s")
            print("可以用 ffmpeg 截取这15秒做视频")
```

---

## 整条链路跑下来是什么体验

整个流程是这样的：

**写歌词 → H3生成音乐 → 上传GitHub → ASR识别字幕 → 截取副歌片段 → H3生成视频**

每一步都是API调用，全自动。

以嵩口IP为例，我们选了"画舫摇呀摇"这段副歌，截取15秒，配上鹤形路的场景图和林小溪的角色参考，调用H3全能参考视频生成。

出来的效果是：**15秒的古风慢摇MV，画面跟着音乐节奏动，角色在古镇仙鹤巷道里缓缓转身，额头的花钿符文若隐若现。**

**成本方面：**

| 环节 | 工具 | 消耗 | 耗时 |
|------|------|------|------|
| 音乐生成 | MiniMax H3 | 约 80 coins | 5-6分钟 |
| 字幕识别 | ASR | 约 8 coins | 30-60秒 |
| 视频生成 | H3全能参考 | 约 80 coins | 6-7分钟 |

总共十几块钱、十几分钟，一首完整的IP主题曲+一段15秒MV就出来了。

---

## 写在最后

AI工具的发展速度，常常超出我们的预期。

一年前，"用文本生成带人声的歌曲"还像天方夜谭；现在，它已经是一个可以稳定调用的API。再过一年呢？或许整条动画短片的生成都会变成一行命令。

但工具再强，核心还是**内容本身**。嵩口的故事、林小溪的人物、那些关于古镇与仙侠的想象，才是真正打动人心的东西。AI只是把这些想象更快、更便宜地变成了可以看见听见的画面。

就像画舫摇呀摇，摇晃着千年的寂寞——
技术在变，讲故事的人，永远在岸上。

---

*本文中的两个Python工作流脚本均可直接运行，只需设置 `RUNNINGHUB_API_KEY` 环境变量。完整项目代码见 GitHub: easyeye163/h3-video-coding*
