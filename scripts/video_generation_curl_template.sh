#!/bin/bash
# ============================================================
# 视频生成脚本（GitHub直链版 · 15秒 · 6段式 Full-Reference）
# ============================================================
# 使用方法：
#   1. 设置环境变量：export RUNNINGHUB_API_KEY="你的api_key"
#   2. 修改下方素材链接和提示词
#   3. 执行：bash video_generation_curl_template.sh
# ============================================================

set -e

# ==================== 【必填】素材链接（GitHub raw 完整URL） ====================
PICTURE1_URL="https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/images/songkou_characters/lin_xiaoxi_three_view.png"
PICTURE2_URL="https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/images/%E5%B5%A9%E5%8F%A3%E7%9C%9F%E5%AE%9E%E5%9C%BA%E6%99%AF%E5%9B%BE/%E5%B5%A9%E5%8F%A3%E5%85%A8%E6%99%AF.png"
PICTURE3_URL="example.png"   # 未使用填 example.png
AUDIO1_URL="https://raw.githubusercontent.com/easyeye163/h3-video-coding/main/audio/voices/songkou_girl_main.flac"
AUDIO2_URL="$AUDIO1_URL"     # 未使用则复用 audio1

# ==================== 【必填】视频参数 ====================
VIDEO_DURATION="15"
ASPECT_RATIO="16:9 (Widescreen)"
MEGAPIXELS="0.7000000000000001"

# ==================== 【必填】6段式提示词 ====================
PROMPT=$(cat <<'PROMPT_EOF'
subject_definitions:
<Picture 1> 严格负责女性角色的身份与造型：林小溪，24岁返乡青年，黑长低马尾，空气刘海，浅蓝交领汉服上衣配白边，蓝色牛仔阔腿裤，白色帆布鞋，温柔微笑。全片不得漂移。
<Picture 2> 仅负责场景空间环境与机位参照：大樟溪穿镇而过，白墙黑瓦明清古民居群依山傍水，航拍俯瞰全貌。以图2为准确定建筑群纵深、溪流走向与晨雾氛围，不参与人物造型。
<Audio 1> 为 <Subject 1>（S1）的音色参考：温柔活泼的年轻女声。

summary:
15秒嵩口古镇文化宣传质感镜头。清晨薄雾笼罩下的嵩口古镇全貌（场景参照<Picture 2>嵩口全景），航拍俯瞰到地面跟拍，S1在场，暖光初现，乡愁与期待交织。

retention_analysis:
<Picture 1>（角色锚点）：完全保留 - 林小溪的身份、发型、服装保持一致。
<Subject 1>（全程出镜）：完全保留 - 身份与服装保持一致。
<Audio 1>：参考 - 目标说话人遵循参考音色，不复制信号。

detailed_description:
目标视频采用电影感、文学化文化宣传风格，柔和暖光，嵩口薄雾永恒氛围，白墙黛瓦徽派建筑，大樟溪晨雾，轻度去饱和SLOG质感。
[Shot 1]（0s-7s）中景跟拍，<Picture 1> 参照的 <Subject 1>（S1）林小溪拖着行李箱走在青石板巷道上，薄雾飘过白墙黛瓦屋顶，她四下张望，轻声感叹<d>嵩口……我回来了。</d>[Shot 2]（7s-15s）中近景，她停下脚步仰望古镇屋檐，薄雾捕捉到第一缕暖光，眼眶微红，嘴角带着释然微笑。

overall_soundscape:
远处鸟鸣与柔和的河雾环境声。

non_diegetic_music:
古筝独奏，温柔而苏醒。
PROMPT_EOF
)

# ==================== 【工作流配置】（一般不需要改） ====================
APP_ID="2090774740146413570"
API_BASE="https://www.runninghub.cn/openapi/v2"
RUN_URL="${API_BASE}/run/ai-app/${APP_ID}"
QUERY_URL="${API_BASE}/query"

# ==================== 检查 API Key ====================
if [ -z "$RUNNINGHUB_API_KEY" ]; then
    echo "❌ 错误：请先设置 RUNNINGHUB_API_KEY 环境变量"
    echo "   export RUNNINGHUB_API_KEY=\"你的api_key\""
    exit 1
fi

# ==================== 转义提示词为 JSON 字符串 ====================
ESCAPED_PROMPT=$(echo "$PROMPT" | python3 -c "
import sys, json
prompt = sys.stdin.read()
print(json.dumps(prompt, ensure_ascii=False), end='')
")

# ==================== 构建并提交 ====================
echo "========================================"
echo " 提交视频生成任务（GitHub直链版）"
echo "========================================"
echo " Picture 1: $PICTURE1_URL"
echo " Picture 2: $PICTURE2_URL"
echo " Picture 3: $PICTURE3_URL"
echo " Audio 1:   $AUDIO1_URL"
echo " Audio 2:   $AUDIO2_URL"
echo " 时长:      ${VIDEO_DURATION}秒 / ${ASPECT_RATIO}"
echo ""

REQUEST_BODY=$(cat <<EOF
{
  "nodeInfoList": [
    {
      "nodeId": "132",
      "fieldName": "value",
      "fieldValue": "${VIDEO_DURATION}",
      "description": "时长（秒）"
    },
    {
      "nodeId": "115",
      "fieldName": "aspect_ratio",
      "fieldData": "[\"COMBO\", {\"default\": \"1:1 (Square)\", \"options\": [\"1:1 (Square)\", \"2:3 (Portrait Photo)\", \"3:2 (Photo)\", \"3:4 (Portrait Standard)\", \"4:3 (Standard)\", \"9:16 (Portrait Widescreen)\", \"16:9 (Widescreen)\", \"21:9 (Ultrawide)\"], \"tooltip\": \"The aspect ratio for the output dimensions.\", \"multiselect\": false}]",
      "fieldValue": "${ASPECT_RATIO}",
      "description": "方向"
    },
    {
      "nodeId": "115",
      "fieldName": "megapixels",
      "fieldValue": "${MEGAPIXELS}",
      "description": "分辨率"
    },
    {
      "nodeId": "137",
      "fieldName": "image",
      "fieldValue": "${PICTURE1_URL}",
      "description": "picture1"
    },
    {
      "nodeId": "138",
      "fieldName": "value",
      "fieldValue": ${ESCAPED_PROMPT},
      "description": "提示词（6段式 Full-Reference）"
    },
    {
      "nodeId": "166",
      "fieldName": "image",
      "fieldValue": "${PICTURE2_URL}",
      "description": "picture2"
    },
    {
      "nodeId": "165",
      "fieldName": "audio",
      "fieldValue": "${AUDIO1_URL}",
      "description": "audio1"
    },
    {
      "nodeId": "167",
      "fieldName": "image",
      "fieldValue": "${PICTURE3_URL}",
      "description": "picture3"
    },
    {
      "nodeId": "168",
      "fieldName": "image",
      "fieldValue": "example.png",
      "description": "picture4（占位，不要改）"
    },
    {
      "nodeId": "169",
      "fieldName": "audio",
      "fieldValue": "${AUDIO2_URL}",
      "description": "audio2（未使用则复用audio1）"
    }
  ],
  "instanceType": "default",
  "usePersonalQueue": "false"
}
EOF
)

echo "🚀 提交任务中..."
echo ""

RESPONSE=$(curl -s -X POST "$RUN_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
    -d "$REQUEST_BODY")

echo "📋 响应："
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"

TASK_ID=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('taskId', ''))
")

if [ -n "$TASK_ID" ]; then
    echo ""
    echo "✅ 任务提交成功！"
    echo "   Task ID: $TASK_ID"
    echo ""
    echo "🔍 查询结果："
    echo "   curl -s -X POST '${QUERY_URL}' -H 'Content-Type: application/json' -H \"Authorization: Bearer \$RUNNINGHUB_API_KEY\" -d '{\"taskId\": \"${TASK_ID}\"}'"
    echo ""
    echo "⚠️  COS 链接 24 小时失效，生成成功后请及时下载到本地。"
else
    echo ""
    echo "❌ 任务提交失败，请检查错误信息。"
    exit 1
fi
