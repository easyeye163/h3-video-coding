#!/bin/bash

# 永泰嵩口古镇 - 人物三视图同步脚本
# 将RunningHub生成的写实风格三视图同步到飞书作品列表并下载到本地

set -e

echo "🎬 永泰嵩口古镇 - 人物定妆照同步工具"
echo "================================"
echo ""

# 配置
BASE_TOKEN="MsfRbVPZ4aicuRsotmwcwgb9npc"
TABLE_ID="tbl9hKFVTAGrCzlA"
LOCAL_DIR="./images/songkou_characters"

# 创建本地目录
mkdir -p "$LOCAL_DIR"
echo "✅ 本地目录: $LOCAL_DIR"
echo ""

# 角色定义
declare -a CHARACTERS=(
  "林小溪|lin_xiaoxi_three_view.png|2092972777580744705|24岁中国女孩，马尾辫，浅蓝汉服+牛仔裤"
  "陈阿公|chen_agong_three_view.png|2092973318515949569|72岁老者，白发白须，传统对襟衫，持折扇"
  "张导演|zhang_director_three_view.png|2092973403551260673|35岁导演，黑框眼镜，黑T恤工装裤，背相机"
  "神秘旅人|mystery_traveler_three_view.png|2092973061623209985|28岁神秘男子，深邃眼神，卡其色风衣"
  "小糯米|xiaomi_three_view.png|2092973651837284354|8岁小女孩，双丸子头，红色小棉袄"
)

echo "📋 角色列表："
echo "----------------------------------------"
for i in "${!CHARACTERS[@]}"; do
  IFS='|' read -r name filename task_id desc <<< "${CHARACTERS[$i]}"
  echo "$((i+1)). $name"
  echo "   文件: $filename"
  echo "   任务ID: $task_id"
  echo "   描述: $desc"
  echo ""
done

echo "================================"
echo ""
echo "📌 操作步骤："
echo ""
echo "步骤1️⃣  从RunningHub下载图片"
echo "----------------------------------------"
echo "请访问以下网页下载5张写实风格三视图图片："
echo "👉  https://www.runninghub.cn/console/task"
echo ""
echo "任务ID列表："
for char in "${CHARACTERS[@]}"; do
  IFS='|' read -r name filename task_id desc <<< "$char"
  echo "  • $name: $task_id"
done
echo ""
echo "下载后请将图片保存到: $LOCAL_DIR"
echo ""

read -p "是否已下载完成？(y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "⏸️  请先下载图片后再运行此脚本"
  exit 1
fi

echo ""
echo "步骤2️⃣  验证本地文件"
echo "----------------------------------------"
all_files_exist=true
for char in "${CHARACTERS[@]}"; do
  IFS='|' read -r name filename task_id desc <<< "$char"
  if [ -f "$LOCAL_DIR/$filename" ]; then
    echo "✅ $filename 存在"
  else
    echo "❌ $filename 不存在"
    all_files_exist=false
  fi
done

if [ "$all_files_exist" = false ]; then
  echo ""
  echo "⚠️  部分文件缺失，请检查后重试"
  exit 1
fi

echo ""
echo "✅ 所有文件已就绪"
echo ""

echo "步骤3️⃣  上传到飞书云盘（可选）"
echo "----------------------------------------"
echo "正在上传图片到飞书云盘..."
echo ""

# 上传文件并记录URL
declare -a URLs=()
for char in "${CHARACTERS[@]}"; do
  IFS='|' read -r name filename task_id desc <<< "$char"
  
  echo "📤 上传: $filename"
  upload_result=$(lark-cli drive +upload-file --path "$LOCAL_DIR/$filename" --as user 2>&1)
  url=$(echo $upload_result | jq -r '.url // .file_url // empty')
  
  if [ -n "$url" ]; then
    echo "   ✅ 上传成功"
    URLs+=("$url")
  else
    echo "   ⚠️  上传失败，使用空URL"
    URLs+=("")
  fi
done

echo ""
echo "步骤4️⃣  创建飞书作品列表记录"
echo "----------------------------------------"
echo "正在创建记录..."
echo ""

# 构建JSON
records_json="{"create_records":["
for i in "${!CHARACTERS[@]}"; do
  IFS='|' read -r name filename task_id desc <<< "${CHARACTERS[$i]}"
  url="${URLS[$i]}"
  
  if [ $i -gt 0 ]; then
    records_json+=","
  fi
  
  records_json+="{\"fields\":{"
  records_json+="\"任务名称\":\"嵩口_${name}_写实三视图定妆照\","
  records_json+="\"任务类型\":[\"文生图\"],"
  records_json+="\"任务状态\":[\"已完成\"],"
  records_json+="\"提示词\":\"Professional three-view portrait photography, ${desc}, photorealistic, 8K ultra HD, cinematic lighting\","
  records_json+="\"本地目录\":\"${LOCAL_DIR}/${filename}\","
  if [ -n "$url" ]; then
    records_json+="\"远程链接\":\"${url}\","
  else
    records_json+="\"远程链接\":\"\","
  fi
  records_json+="\"任务创建日期\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000+08:00)\""
  records_json+="}}"
done
records_json+="]}"

echo "$records_json" | jq '.' > /tmp/songkou_records.json
echo "✅ JSON已生成: /tmp/songkou_records.json"

# 执行创建
create_result=$(lark-cli base +record-batch-create \
  --base-token "$BASE_TOKEN" \
  --table-id "$TABLE_ID" \
  --json "$(cat /tmp/songkou_records.json)" \
  --as user 2>&1)

if echo "$create_result" | jq -e '.ok' > /dev/null 2>&1; then
  echo "✅ 记录创建成功！"
else
  echo "⚠️  记录创建可能失败，错误信息："
  echo "$create_result" | head -c 500
fi

echo ""
echo "================================"
echo "🎉 同步完成！"
echo "================================"
echo ""
echo "📊 总结："
echo "  • 本地文件位置: $LOCAL_DIR/"
echo "  • 飞书Base: RunningHub AI 作品记录"
echo "  • 表名: 作品列表"
echo "  • 新增记录: 5条（角色写实风格三视图）"
echo ""
echo "📝 后续操作："
echo "  1. 在飞书中查看新增的5条记录"
echo "  2. 确认图片链接正确"
echo "  3. 可将这些记录关联到极简版本表的参考图字段"
echo ""
echo "💡 提示：这些三视图可用于："
echo "  • 作为视频生成的参考图（保证角色一致性）"
echo "  • 分镜脚本的配图素材"
echo "  • 宣传物料制作"
