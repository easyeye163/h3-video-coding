#!/bin/bash
# ============================================================
# 视频生成 curl 模板（MiniMax H3 · 15秒 · 6段式 Full-Reference）
# ============================================================
# 使用方法：
#   1. 先设置环境变量：export RUNNINGHUB_API_KEY="你的api_key"
#   2. 修改下方的 FILE_PATHS 区域，指定本地图片/音频路径
#   3. 修改 PROMPT 区域，填入6段式提示词
#   4. 执行：bash video_generation_curl_template.sh
# ============================================================

set -e

# ==================== 【必填】文件路径配置 ====================
# 参考图1（角色/主图，对应 nodeId 137）
PICTURE1_PATH="./images/songkou_characters/lin_xiaoxi_three_view.png"
# 参考图2（场景/副图，对应 nodeId 166）
PICTURE2_PATH="./images/嵩口真实场景图/嵩口全景.png"
# 参考音频1（音色参考，对应 nodeId 165）
AUDIO1_PATH="./audio/voices/songkou_girl_main.flac"

# ==================== 【必填】视频参数 ====================
VIDEO_DURATION="15"          # 时长（秒）：10 或 15
ASPECT_RATIO="16:9 (Widescreen)"  # 画面比例
MEGAPIXELS="0.7000000000000001"   # 分辨率（保持默认即可）

# ==================== 【必填】6段式提示词 ====================
# 注意：所有换行符会自动转义为 \n，直接写多行即可
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
UPLOAD_URL="${API_BASE}/media/upload/binary"
RUN_URL="${API_BASE}/run/ai-app/${APP_ID}"

# 未使用节点的占位值（必须保留，不能删改）
PICTURE3_PLACEHOLDER="example.png"
PICTURE4_PLACEHOLDER="example.png"
AUDIO2_PLACEHOLDER="ffc133718aa6119fa7538413581a64da5754e3405d1d4ef1ba3edbbe09c06ccd.flac"

# ==================== 检查 API Key ====================
if [ -z "$RUNNINGHUB_API_KEY" ]; then
    echo "❌ 错误：请先设置 RUNNINGHUB_API_KEY 环境变量"
    echo "   export RUNNINGHUB_API_KEY=\"你的api_key\""
    exit 1
fi

# ==================== 函数：上传文件 ====================
upload_file() {
    local file_path="$1"
    local file_type="$2"  # image 或 audio

    echo "📤 正在上传：$file_path"

    local response
    response=$(curl -s -X POST "$UPLOAD_URL" \
        -H "Authorization: Bearer ${RUNNINGHUB_API_KEY}" \
        -F "file=@${file_path}")

    # 提取文件名（data.download_url 中的文件名部分）
    local filename
    filename=$(echo "$response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
url = data.get('data', {}).get('download_url', '')
# download_url 格式可能是完整URL或只是文件名
if '/' in url:
    filename = url.split('/')[-1]
else:
    filename = url
print(filename)
")

    if [ -z "$filename" ] || [ "$filename" = "None" ]; then
        echo "❌ 上传失败：$response"
        exit 1
    fi

    echo "   ✅ 上传成功：$filename"
    echo "$filename"
}

# ==================== 步骤1：上传图片和音频 ====================
echo "========================================"
echo " 步骤 1/2：上传参考素材"
echo "========================================"

PICTURE1_FILE=$(upload_file "$PICTURE1_PATH" "image")
sleep 2

PICTURE2_FILE=$(upload_file "$PICTURE2_PATH" "image")
sleep 2

AUDIO1_FILE=$(upload_file "$AUDIO1_PATH" "audio")
sleep 2

echo ""
echo "📁 上传结果："
echo "   Picture1: $PICTURE1_FILE"
echo "   Picture2: $PICTURE2_FILE"
echo "   Audio1:   $AUDIO1_FILE"
echo ""

# ==================== 步骤2：提交视频生成任务 ====================
echo "========================================"
echo " 步骤 2/2：提交视频生成任务"
echo "========================================"

# 转义提示词中的双引号和换行符
ESCAPED_PROMPT=$(echo "$PROMPT" | python3 -c "
import sys, json
prompt = sys.stdin.read()
print(json.dumps(prompt))
")

# 构建请求体
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
      "fieldValue": "${PICTURE1_FILE}",
      "description": "picture1"
    },
    {
      "nodeId": "138",
      "fieldName": "value",
      "fieldValue": ${ESCAPED_PROMPT},
      "description": "提示词"
    },
    {
      "nodeId": "166",
      "fieldName": "image",
      "fieldValue": "${PICTURE2_FILE}",
      "description": "picture2"
    },
    {
      "nodeId": "165",
      "fieldName": "audio",
      "fieldValue": "${AUDIO1_FILE}",
      "description": "audio1"
    },
    {
      "nodeId": "167",
      "fieldName": "image",
      "fieldValue": "${PICTURE3_PLACEHOLDER}",
      "description": "picture3"
    },
    {
      "nodeId": "168",
      "fieldName": "image",
      "fieldValue": "${PICTURE4_PLACEHOLDER}",
      "description": "picture4"
    },
    {
      "nodeId": "169",
      "fieldName": "audio",
      "fieldValue": "${AUDIO2_PLACEHOLDER}",
      "description": "audio2"
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

# 提取 taskId
TASK_ID=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('taskId', ''))
")

if [ -n "$TASK_ID" ]; then
    echo ""
    echo "✅ 任务提交成功！"
    echo "   Task ID: $TASK_ID"
    echo "   查询状态: curl -s -X POST '${API_BASE}/query' -H 'Content-Type: application/json' -d '{\"taskId\": \"${TASK_ID}\"}'"
    echo ""
    echo "⚠️  注意：COS 链接 24 小时失效，生成成功后请及时下载到本地。"
else
    echo ""
    echo "❌ 任务提交失败，请检查错误信息。"
    exit 1
fi
