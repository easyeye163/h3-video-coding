#!/usr/bin/env python3
"""
第6集《时空相遇》带对话视频生成脚本
使用RunningHub高级视频工作流
"""

import requests
import time
import json
import os

API_KEY = os.environ.get("RUNNINGHUB_API_KEY")
if not API_KEY:
    raise SystemExit("未设置环境变量 RUNNINGHUB_API_KEY")
BASE_URL = "https://www.runninghub.cn/openapi/v2/run/ai-app/2090774740146413570"
PROJECT_DIR = "."
AUDIO_DIR = f"{PROJECT_DIR}/audio"
VIDEO_DIR = f"{PROJECT_DIR}/videos"
IMAGE_DIR = f"{PROJECT_DIR}/images"

# 确保目录存在
os.makedirs(VIDEO_DIR, exist_ok=True)

def upload_audio_to_runninghub(audio_path):
    """上传音频到RunningHub获取fileId"""
    # 注意：实际API需要先上传文件获取fileId
    # 这里简化处理，直接使用文件名
    return os.path.basename(audio_path)

def generate_video_shot(shot_number, title, prompt_text, scene_image, character_image, audio_file, output_name):
    """生成单个Shot视频"""
    
    payload = {
        "nodeInfoList": [
            {
                "nodeId": "132",
                "fieldName": "value",
                "fieldValue": "10",
                "description": "时长"
            },
            {
                "nodeId": "115",
                "fieldName": "aspect_ratio",
                "fieldValue": "16:9 (Widescreen)",
                "description": "方向"
            },
            {
                "nodeId": "115",
                "fieldName": "megapixels",
                "fieldValue": "0.7",
                "description": "分辨率"
            },
            {
                "nodeId": "137",
                "fieldName": "image",
                "fieldValue": scene_image,
                "description": "首帧场景"
            },
            {
                "nodeId": "166",
                "fieldName": "image",
                "fieldValue": character_image,
                "description": "角色参考"
            },
            {
                "nodeId": "165",
                "fieldName": "audio",
                "fieldValue": audio_file,
                "description": "音频"
            },
            {
                "nodeId": "138",
                "fieldName": "value",
                "fieldValue": prompt_text,
                "description": "提示词"
            }
        ],
        "instanceType": "default",
        "usePersonalQueue": "false"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers, timeout=60)
        result = response.json()
        
        if result.get("code") == 0 or result.get("code") == 200:
            task_id = result.get("data", {}).get("taskId") or result.get("data", {}).get("id")
            print(f"✅ Shot {shot_number} [{title}] 已提交，TaskID: {task_id}")
            return task_id
        else:
            print(f"❌ Shot {shot_number} 提交失败: {result.get('msg')}")
            return None
    except Exception as e:
        print(f"❌ Shot {shot_number} 异常: {e}")
        return None

def main():
    """主函数"""
    print("🎬 开始生成带对话的视频...")
    
    # Shot 4: 触摸倒影
    shot4_prompt = """subject_definitions:
<Picture 1> 古代东方女子，身穿精致汉服，银饰头冠，长发披肩，清冷高贵气质，表情从好奇转为惊讶
<Picture 2> 现代咖啡厅场景，落地玻璃窗，夜晚城市灯光倒影

summary:
神秘女子触摸玻璃窗看到现代倒影，现代女子出现问候，展现时空交错的奇幻感

retention_analysis:
人物不变量：汉服女子的面部特征、发饰、服装全程保持一致
场景不变量：玻璃窗位置、城市夜景灯光保持稳定
风格不变量：梦幻写实风格，光影对比强烈，冷暖色调交织

detailed_description:
[Shot] 夜晚，一座现代都市高楼前。身穿华丽汉服的神秘女子站在巨大的落地玻璃窗前，她伸出纤细的手指轻轻触摸玻璃表面。镜头特写她的手指与玻璃接触的瞬间，玻璃中映出她的倒影——但倒影中的她穿着现代服装。她惊讶地睁大眼睛，困惑地歪头看着倒影。随后她转身，发现身后站着一位穿着简约现代服装的温暖微笑的年轻女子。现代女子温柔地说："这里是21世纪的上海。"神秘女子惊讶地问："21世纪……我在做梦吗？"镜头缓缓推进，展现两人交汇的目光和表情变化。

overall_soundscape:
夜晚城市环境音、远处车流声、玻璃轻触声、轻柔脚步声
Audio1（神秘女子清冷）：「这是……哪里？」
Audio2（现代女子温暖）：「这里是21世纪的上海。」
Audio1：「21世纪……我在做梦吗？」

non_diegetic_music:
梦幻神秘钢琴曲，逐渐过渡到温暖的弦乐"""
    
    # Shot 5: 咖啡厅相遇
    shot5_prompt = """subject_definitions:
<Picture 1> 古代东方女子，汉服银饰，好奇困惑表情
<Picture 2> 现代咖啡厅内部，温馨灯光，咖啡机设备

summary:
神秘女子在咖啡厅好奇观察咖啡机，现代咖啡师女子耐心解释并邀请品尝

retention_analysis:
人物不变量：汉服女子的发饰、服装、清冷气质保持一致
场景不变量：咖啡厅暖色调灯光、咖啡机位置稳定
风格不变量：温馨治愈风格，柔和光线，生活化场景

detailed_description:
[Shot] 现代咖啡厅内，温暖的灯光。身穿汉服的神秘女子站在咖啡机前，好奇地盯着旋转的咖啡喷嘴。她的眼神充满困惑和好奇，眉头微皱。现代咖啡师女子走到她身边，温柔地微笑说："这是咖啡机，你要尝尝吗？"神秘女子眨了眨眼，疑惑地问："咖啡……是什么味道？"咖啡师微笑着递过一杯香醇的咖啡，镜头特写两人交汇的目光，神秘女子眼中闪过一丝期待。

overall_soundscape:
咖啡厅轻柔爵士乐、咖啡机运作声、杯子轻放声
Audio1：「那……这是什么机器？」
Audio2：「这是咖啡机，你要尝尝吗？」
Audio1：「咖啡……是什么味道？」

non_diegetic_music:
轻快温馨的钢琴旋律"""
    
    # Shot 6: 时空交汇
    shot6_prompt = """subject_definitions:
<Picture 1> 古代东方女子，汉服银饰，眼中含泪不舍
<Picture 2> 现代咖啡厅与星空交汇的奇幻场景

summary:
神秘女子准备离开回到古代，两人握手告别，时空光芒绽放，温情收尾

retention_analysis:
人物不变量：汉服女子面部特征、发饰保持，眼泪表情自然
场景不变量：咖啡厅背景逐渐融入星空光芒
风格不变量：史诗奇幻风格，金光璀璨，情感饱满

detailed_description:
[Shot] 咖啡厅内，神秘女子看着周围开始闪烁的时空光芒，眼中含泪。她转向现代女子，轻声说："我想……回到我的时代。"现代女子握住她的手，温暖地说："没关系，我们会再见的。"神秘女子感激地微笑："谢谢你……朋友。"两人牵手，时空漩涡在她们周围绽放金色光芒，越来越亮。镜头缓缓拉远，定格在现代女子挥手告别的温暖画面，时空之门逐渐关闭。

overall_soundscape:
时空魔法音效、心跳声、轻柔风声
Audio1：「我想……回到我的时代。」
Audio2：「没关系，我们会再见的。」
Audio1：「谢谢你……朋友。」

non_diegetic_music:
史诗感弦乐，渐强后渐弱，温暖收尾"""
    
    # 音频文件
    audio1 = "20岁女生_清冷.flac"  # 神秘女子
    audio2 = "20岁女生.flac"       # 现代女子
    
    # 使用现有的场景图和角色图
    scene_images = {
        4: "modern_city_night.png",
        5: "cafe_interior.png",
        6: "time_portal_scene.png"
    }
    
    character_images = {
        4: "ancient_woman.png",
        5: "ancient_woman.png",
        6: "ancient_woman.png"
    }
    
    # 生成视频
    shots = [
        (4, "触摸倒影", shot4_prompt, scene_images[4], character_images[4], audio1, "27_时空相遇-触摸倒影-对话版"),
        (5, "咖啡厅相遇", shot5_prompt, scene_images[5], character_images[5], audio1, "28_时空相遇-咖啡厅相遇-对话版"),
        (6, "时空交汇", shot6_prompt, scene_images[6], character_images[6], audio1, "29_时空相遇-时空交汇-对话版")
    ]
    
    task_ids = []
    for shot_num, title, prompt, scene_img, char_img, audio, output_name in shots:
        print(f"\n🎬 生成 Shot {shot_num}: {title}")
        task_id = generate_video_shot(
            shot_num, title, prompt, scene_img, char_img, audio, output_name
        )
        if task_id:
            task_ids.append(task_id)
        time.sleep(3)  # 避免API限流
    
    print(f"\n✅ 所有视频已提交生成！")
    print(f"Task IDs: {task_ids}")

if __name__ == "__main__":
    main()
