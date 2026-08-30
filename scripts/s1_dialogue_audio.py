#!/usr/bin/env python3
"""
第6集对话音频生成脚本
使用RunningHub API生成两个角色的语音
"""

import requests
import time
import json
import os

API_KEY = os.environ.get("RUNNINGHUB_API_KEY")
if not API_KEY:
    raise SystemExit("未设置环境变量 RUNNINGHUB_API_KEY")
BASE_URL = "https://www.runninghub.cn/openapi/v2"

# 对话内容
DIALOGUE = {
    "shot4": [
        {"role": "Audio1_神秘女子", "text": "这是……哪里？"},
        {"role": "Audio2_现代女子", "text": "这里是21世纪的上海。"},
        {"role": "Audio1_神秘女子", "text": "21世纪……我在做梦吗？"}
    ],
    "shot5": [
        {"role": "Audio1_神秘女子", "text": "那……这是什么机器？"},
        {"role": "Audio2_现代女子", "text": "这是咖啡机，你要尝尝吗？"},
        {"role": "Audio1_神秘女子", "text": "咖啡……是什么味道？"}
    ],
    "shot6": [
        {"role": "Audio1_神秘女子", "text": "我想……回到我的时代。"},
        {"role": "Audio2_现代女子", "text": "没关系，我们会再见的。"},
        {"role": "Audio1_神秘女子", "text": "谢谢你……朋友。"}
    ]
}

# 音色配置
VOICE_CONFIG = {
    "Audio1_神秘女子": {
        "voice_type": "female",
        "style": "清冷古风",
        "speed": 0.9
    },
    "Audio2_现代女子": {
        "voice_type": "female",
        "style": "温暖甜美",
        "speed": 1.0
    }
}

def generate_tts(text, voice_type, style, output_file):
    """生成TTS音频"""
    # TODO: 实现RunningHub TTS API调用
    print(f"生成TTS: {text} -> {output_file}")
    return output_file

def main():
    """主函数"""
    print("开始生成对话音频...")
    
    for shot, lines in DIALOGUE.items():
        print(f"\n{shot}:")
        for i, line in enumerate(lines):
            voice = line["role"]
            text = line["text"]
            config = VOICE_CONFIG[voice]
            output_file = f"audio/{shot}_line{i+1}_{voice}.flac"
            generate_tts(text, config["voice_type"], config["style"], output_file)
            time.sleep(1)  # 避免API限流
    
    print("\n✅ 对话音频生成完成！")

if __name__ == "__main__":
    main()
