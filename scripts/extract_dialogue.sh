#!/bin/bash
# 提取对话音频片段

AUDIO_DIR="./audio"
OUTPUT_DIR="./audio/dialogue"

# Audio1 - 神秘女子（清冷）
AUDIO1="$AUDIO_DIR/20岁女生_清冷.flac"
# Audio2 - 现代女子（温暖）
AUDIO2="$AUDIO_DIR/20岁女生.flac"

echo "提取对话片段..."

# Shot 4 对话
ffmpeg -y -i "$AUDIO1" -ss 0 -t 3 -c copy "$OUTPUT_DIR/s4_a1_1.flac" 2>/dev/null
ffmpeg -y -i "$AUDIO2" -ss 0 -t 3 -c copy "$OUTPUT_DIR/s4_a2_1.flac" 2>/dev/null
ffmpeg -y -i "$AUDIO1" -ss 3 -t 3 -c copy "$OUTPUT_DIR/s4_a1_2.flac" 2>/dev/null

# Shot 5 对话
ffmpeg -y -i "$AUDIO1" -ss 6 -t 3 -c copy "$OUTPUT_DIR/s5_a1_1.flac" 2>/dev/null
ffmpeg -y -i "$AUDIO2" -ss 3 -t 3 -c copy "$OUTPUT_DIR/s5_a2_1.flac" 2>/dev/null
ffmpeg -y -i "$AUDIO1" -ss 9 -t 3 -c copy "$OUTPUT_DIR/s5_a1_2.flac" 2>/dev/null

# Shot 6 对话
ffmpeg -y -i "$AUDIO1" -ss 12 -t 3 -c copy "$OUTPUT_DIR/s6_a1_1.flac" 2>/dev/null
ffmpeg -y -i "$AUDIO2" -ss 6 -t 3 -c copy "$OUTPUT_DIR/s6_a2_1.flac" 2>/dev/null
ffmpeg -y -i "$AUDIO1" -ss 15 -t 4 -c copy "$OUTPUT_DIR/s6_a1_2.flac" 2>/dev/null

echo "✅ 对话片段提取完成！"
ls -lh "$OUTPUT_DIR/"
