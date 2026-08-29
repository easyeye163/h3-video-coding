#!/bin/bash
# 合并对话轨道

AUDIO_DIR="./audio"
OUTPUT_DIR="./audio/dialogue"

# 合并Shot 4对话
ffmpeg -y -i "$OUTPUT_DIR/s4_a1_1.flac" -i "$OUTPUT_DIR/s4_a2_1.flac" \
  -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" \
  "$OUTPUT_DIR/s4_dialogue.flac" 2>/dev/null

# 合并Shot 5对话
ffmpeg -y -i "$OUTPUT_DIR/s5_a1_1.flac" -i "$OUTPUT_DIR/s5_a2_1.flac" \
  -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" \
  "$OUTPUT_DIR/s5_dialogue.flac" 2>/dev/null

# 合并Shot 6对话
ffmpeg -y -i "$OUTPUT_DIR/s6_a1_1.flac" -i "$OUTPUT_DIR/s6_a2_1.flac" \
  -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" \
  "$OUTPUT_DIR/s6_dialogue.flac" 2>/dev/null

echo "✅ 对话轨道合并完成！"
ls -lh "$OUTPUT_DIR/"
