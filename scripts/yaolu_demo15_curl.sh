#!/bin/bash
# ============================================================
#  嵩口镇妖录 · 5个15秒爆裂酷炫demo · 图生图版
# ============================================================
#  Demo1: 御剑裂空·万安堡封印爆发（男主solo·御剑+阵法）
#  Demo2: 双剑合璧·荒原雷狱斩妖（男女双主·分剑+雷法）
#  Demo3: 仙鹤归元·鹤形路觉醒（女主solo·仙鹤灵脉+觉醒）
#  Demo4: 水脉雷狱·古码头镇妖（男主solo·雷法+水脉）
#  Demo5: 七阵齐鸣·嵩口觉醒（男女双主·全镇阵眼+仙鹤）
# ============================================================
#  使用方法：
#    1. 设置环境变量：export RUNNINGHUB_API_KEY="你的api_key"
#    2. 执行全部：bash yaolu_demo15_curl.sh
#    3. 或执行单个：bash yaolu_demo15_curl.sh demo1
# ============================================================

set -e

APP_ID="2090774740146413570"
API_BASE="https://www.runninghub.cn/openapi/v2"
RUN_URL="${API_BASE}/run/ai-app/${APP_ID}"
QUERY_URL="${API_BASE}/query"

if [ -z "$RUNNINGHUB_API_KEY" ]; then
    echo "❌ 错误：请先设置 RUNNINGHUB_API_KEY 环境变量"
    echo "   export RUNNINGHUB_API_KEY=\"你的api_key\""
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_FILTER="${1:-all}"

submit_task() {
    local demo_id="$1"
    local demo_title="$2"
    local payload_file="$3"

    if [ "$DEMO_FILTER" != "all" ] && [ "$DEMO_FILTER" != "$demo_id" ]; then
        return
    fi

    echo "========================================"
    echo " $demo_id: $demo_title"
    echo "========================================"

    PAYLOAD=$(python3 -c "
import json, sys
with open('${SCRIPT_DIR}/${payload_file}', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(json.dumps(data, ensure_ascii=False))
")

    RESPONSE=$(curl -s -X POST "$RUN_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $RUNNINGHUB_API_KEY" \
        -d "$PAYLOAD")

    echo "📋 响应："
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"

    TASK_ID=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('taskId', ''))
" 2>/dev/null || echo "")

    if [ -n "$TASK_ID" ] && [ "$TASK_ID" != "" ]; then
        echo "✅ 任务提交成功！Task ID: $TASK_ID"
        echo "🔍 查询：curl -s -X POST '${QUERY_URL}' -H 'Content-Type: application/json' -H 'Authorization: Bearer $RUNNINGHUB_API_KEY' -d '{\"taskId\": \"${TASK_ID}\"}'"
        echo ""
    else
        echo "❌ 任务提交失败"
        echo ""
    fi

    # 并发限制：每个任务间隔3秒
    sleep 3
}

submit_task "demo1" "御剑裂空·万安堡封印爆发" "yaolu_demo15_demo1_wanan_sword_split_payload.json"
submit_task "demo2" "双剑合璧·荒原雷狱斩妖" "yaolu_demo15_demo2_wasteland_duo_thunder_payload.json"
submit_task "demo3" "仙鹤归元·鹤形路觉醒" "yaolu_demo15_demo3_hexing_crane_awakening_payload.json"
submit_task "demo4" "水脉雷狱·古码头镇妖" "yaolu_demo15_demo4_pier_water_thunder_payload.json"
submit_task "demo5" "七阵齐鸣·嵩口觉醒" "yaolu_demo15_demo5_panorama_seven_arrays_payload.json"

echo "========================================"
echo " 全部任务提交完成！"
echo "========================================"
echo "⏳ 每个任务约5-6分钟生成完成"
echo "⚠️  COS 链接 24 小时失效，请及时查询并下载到 videos/songkou_xianxia/ 目录"
