#!/usr/bin/env python3
"""创建对话音频轨道"""
import subprocess
import os

AUDIO_DIR = "./audio"
DIALOGUE_DIR = f"{AUDIO_DIR}/dialogue"
os.makedirs(DIALOGUE_DIR, exist_ok=True)

# Audio sources
AUDIO1 = f"{AUDIO_DIR}/20岁女生_清冷.flac"  # 神秘女子
AUDIO2 = f"{AUDIO_DIR}/20岁女生.flac"      # 现代女子

def extract_segment(audio_file, start, duration, output_file):
    """提取音频片段"""
    cmd = [
        'ffmpeg', '-y', '-i', audio_file,
        '-ss', str(start), '-t', str(duration),
        '-c:a', 'libvorbis', output_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {os.path.basename(output_file)}")
        return True
    else:
        print(f"❌ 失败: {output_file}")
        return False

def concat_segments(segments, output_file):
    """合并多个片段"""
    if not segments:
        return
    # 使用concat demuxer
    list_file = f"{DIALOGUE_DIR}/concat_list.txt"
    with open(list_file, 'w') as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")
    
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', list_file, '-c:a', 'libvorbis', output_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {os.path.basename(output_file)}")
    else:
        print(f"❌ 合并失败: {output_file}")

# Shot 4 对话: "这是……哪里？" -> "这里是21世纪的上海。" -> "21世纪……我在做梦吗？"
print("\n=== Shot 4 触摸倒影 ===")
s4_a1_1 = f"{DIALOGUE_DIR}/s4_a1_1.ogg"
s4_a2_1 = f"{DIALOGUE_DIR}/s4_a2_1.ogg"
s4_a1_2 = f"{DIALOGUE_DIR}/s4_a1_2.ogg"
extract_segment(AUDIO1, 0, 3, s4_a1_1)
extract_segment(AUDIO2, 0, 3, s4_a2_1)
extract_segment(AUDIO1, 3, 3, s4_a1_2)
concat_segments([s4_a1_1, s4_a2_1, s4_a1_2], f"{DIALOGUE_DIR}/s4_dialogue.ogg")

# Shot 5 对话: "那……这是什么机器？" -> "这是咖啡机，你要尝尝吗？" -> "咖啡……是什么味道？"
print("\n=== Shot 5 咖啡厅相遇 ===")
s5_a1_1 = f"{DIALOGUE_DIR}/s5_a1_1.ogg"
s5_a2_1 = f"{DIALOGUE_DIR}/s5_a2_1.ogg"
s5_a1_2 = f"{DIALOGUE_DIR}/s5_a1_2.ogg"
extract_segment(AUDIO1, 6, 3, s5_a1_1)
extract_segment(AUDIO2, 3, 3, s5_a2_1)
extract_segment(AUDIO1, 9, 3, s5_a1_2)
concat_segments([s5_a1_1, s5_a2_1, s5_a1_2], f"{DIALOGUE_DIR}/s5_dialogue.ogg")

# Shot 6 对话: "我想……回到我的时代。" -> "没关系，我们会再见的。" -> "谢谢你……朋友。"
print("\n=== Shot 6 时空交汇 ===")
s6_a1_1 = f"{DIALOGUE_DIR}/s6_a1_1.ogg"
s6_a2_1 = f"{DIALOGUE_DIR}/s6_a2_1.ogg"
s6_a1_2 = f"{DIALOGUE_DIR}/s6_a1_2.ogg"
extract_segment(AUDIO1, 12, 3, s6_a1_1)
extract_segment(AUDIO2, 6, 3, s6_a2_1)
extract_segment(AUDIO1, 15, 4, s6_a1_2)
concat_segments([s6_a1_1, s6_a2_1, s6_a1_2], f"{DIALOGUE_DIR}/s6_dialogue.ogg")

print("\n✅ 所有对话音频创建完成！")
print(f"\n文件位置: {DIALOGUE_DIR}/")
