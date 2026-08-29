#!/bin/bash
# 第7集《时空对话》视频生成脚本

API_KEY="${RUNNINGHUB_API_KEY:?未设置环境变量 RUNNINGHUB_API_KEY}"
APP_ID="2090774740146413570"
BASE_URL="https://www.runninghub.cn/openapi/v2/run/ai-app/$APP_ID"

echo "🎬 开始生成第7集《时空对话》..."
echo ""

# Shot A - 公园初遇
echo "📹 Shot A: 公园初遇 (15秒)"
curl -s --location "$BASE_URL" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $API_KEY" \
  --data '{
    "nodeInfoList": [
      {"nodeId": "132", "fieldName": "value", "fieldValue": "15", "description": "时长"},
      {"nodeId": "115", "fieldName": "aspect_ratio", "fieldValue": "16:9 (Widescreen)", "description": "方向"},
      {"nodeId": "115", "fieldName": "megapixels", "fieldValue": "0.7", "description": "分辨率"},
      {"nodeId": "137", "fieldName": "image", "fieldValue": "sunset_beach.png", "description": "picture1"},
      {"nodeId": "138", "fieldName": "value", "fieldValue": "subject_definitions:\\n<Picture 1> 古代东方女子，身穿唐装汉服，银饰头冠，长发披肩，清冷高贵气质\\n<Picture 2> 现代都市公园，黄昏时分，长椅，远处高楼剪影\\nsummary:\\n神秘古代女子婉儿坐在公园长椅上困惑地看着周围，现代女子小雅走近问候\\nretention_analysis:\\n人物不变量：婉儿的汉服、发饰、清冷气质全程一致\\n场景不变量：公园长椅、黄昏光线、远处建筑稳定\\n风格不变量：梦幻写实，温暖黄昏色调\\ndetailed_description:\\n黄昏时分，现代都市公园。身穿华丽唐装汉服的神秘女子婉儿独自坐在公园长椅上，她困惑地环顾四周，看着远处的高楼大厦和来往的行人。她的表情充满好奇和迷茫。一位穿着简约现代服装的年轻女子小雅走过来，温和地在她身边坐下，微笑着说：「这里是上海，一个很美的城市。」婉儿惊讶地问：「上海……我在古籍中听过。」镜头特写两人交汇的目光，背景是美丽的黄昏城市天际线。\\noverall_soundscape:\\n公园环境音：鸟鸣声、远处儿童笑声、树叶沙沙声\\nAudio1（清冷古风）：「这里……是什么地方？」\\nAudio2（温暖甜美）：「这里是上海，一个很美的城市。」\\nAudio1：「上海……我在古籍中听过。」\\nnon_diegetic_music:\\n温暖治愈钢琴曲，带有东方乐器元素", "description": "提示词"},
      {"nodeId": "166", "fieldName": "image", "fieldValue": "ancient_woman.png", "description": "picture2"},
      {"nodeId": "165", "fieldName": "audio", "fieldValue": "20岁女生_清冷.flac", "description": "audio1"},
      {"nodeId": "167", "fieldName": "image", "fieldValue": "ancient_woman.png", "description": "picture3"},
      {"nodeId": "168", "fieldName": "image", "fieldValue": "sunset_beach.png", "description": "picture4"},
      {"nodeId": "169", "fieldName": "audio", "fieldValue": "20岁女生.flac", "description": "audio2"}
    ],
    "instanceType": "default",
    "usePersonalQueue": "false"
  }' | python3 -m json.tool 2>/dev/null || echo "API 响应异常"

echo ""
sleep 3

# Shot B - 文化差异
echo "📹 Shot B: 文化差异 (15秒)"
curl -s --location "$BASE_URL" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $API_KEY" \
  --data '{
    "nodeInfoList": [
      {"nodeId": "132", "fieldName": "value", "fieldValue": "15", "description": "时长"},
      {"nodeId": "115", "fieldName": "aspect_ratio", "fieldValue": "16:9 (Widescreen)", "description": "方向"},
      {"nodeId": "115", "fieldName": "megapixels", "fieldValue": "0.7", "description": "分辨率"},
      {"nodeId": "137", "fieldName": "image", "fieldValue": "modern_city_night.png", "description": "picture1"},
      {"nodeId": "138", "fieldName": "value", "fieldValue": "subject_definitions:\\n<Picture 1> 古代女子好奇表情，指着手机\\n<Picture 2> 现代女子手持智能手机，微笑讲解\\nsummary:\\n神秘女子对现代科技感到困惑，现代女子耐心解释手机功能\\nretention_analysis:\\n人物不变量：汉服女子气质保持，惊讶表情自然\\n场景不变量：公园长椅、手机作为关键道具稳定\\n风格不变量：温馨互动场景，光线柔和\\ndetailed_description:\\n公园长椅上，神秘女子婉儿好奇地盯着小雅手中的智能手机。她伸出手指轻轻触碰屏幕，疑惑地问：「那些发光的盒子是什么？」小雅笑着展示手机功能：「这是手机，可以联系任何人。」婉儿惊叹：「神奇……我们那里只有书信。」镜头在两人之间切换，展现文化碰撞的有趣瞬间。\\noverall_soundscape:\\n公园环境音、手机操作声\\nAudio1：「那些发光的盒子是什么？」\\nAudio2：「这是手机，可以联系任何人。」\\nAudio1：「神奇……我们那里只有书信。」\\nnon_diegetic_music:\\n轻快好奇的钢琴旋律", "description": "提示词"},
      {"nodeId": "166", "fieldName": "image", "fieldValue": "ancient_woman.png", "description": "picture2"},
      {"nodeId": "165", "fieldName": "audio", "fieldValue": "20岁女生_清冷.flac", "description": "audio1"},
      {"nodeId": "167", "fieldName": "image", "fieldValue": "ancient_woman.png", "description": "picture3"},
      {"nodeId": "168", "fieldName": "image", "fieldValue": "modern_city_night.png", "description": "picture4"},
      {"nodeId": "169", "fieldName": "audio", "fieldValue": "20岁女生.flac", "description": "audio2"}
    ],
    "instanceType": "default",
    "usePersonalQueue": "false"
  }' | python3 -m json.tool 2>/dev/null || echo "API 响应异常"

echo ""
sleep 3

# Shot C - 建立友谊
echo "📹 Shot C: 建立友谊 (15秒)"
curl -s --location "$BASE_URL" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $API_KEY" \
  --data '{
    "nodeInfoList": [
      {"nodeId": "132", "fieldName": "value", "fieldValue": "15", "description": "时长"},
      {"nodeId": "115", "fieldName": "aspect_ratio", "fieldValue": "16:9 (Widescreen)", "description": "方向"},
      {"nodeId": "115", "fieldName": "megapixels", "fieldValue": "0.7", "description": "分辨率"},
      {"nodeId": "137", "fieldName": "image", "fieldValue": "crystal_palace.png", "description": "picture1"},
      {"nodeId": "138", "fieldName": "value", "fieldValue": "subject_definitions:\\n<Picture 1> 古代女子优雅握手，微笑\\n<Picture 2> 现代女子热情回应，握手\\nsummary:\\n两人互相介绍名字，建立跨时空友谊\\nretention_analysis:\\n人物不变量：两人表情自然友好，握手动作流畅\\n场景不变量：公园黄昏背景稳定\\n风格不变量：温馨感人，友谊主题\\ndetailed_description:\\n小雅转向婉儿，真诚地说：「我叫小雅，很高兴认识你。」她伸出手。婉儿优雅地握住她的手：「我叫婉儿，来自唐朝。」小雅惊讶但友好地睁大眼睛：「唐朝？那是很久以前了！」两人相视而笑，黄昏的光线洒在她们身上，象征跨越时空的友谊。镜头缓缓拉远，展现两个时代的女性在公园长椅上成为朋友的温馨画面。\\noverall_soundscape:\\n温暖的背景音乐、轻柔风声\\nAudio2：「我叫小雅，很高兴认识你。」\\nAudio1：「我叫婉儿，来自唐朝。」\\nAudio2：「唐朝？那是很久以前了！」\\nnon_diegetic_music:\\n温馨感人的弦乐与钢琴合奏", "description": "提示词"},
      {"nodeId": "166", "fieldName": "image", "fieldValue": "ancient_woman.png", "description": "picture2"},
      {"nodeId": "165", "fieldName": "audio", "fieldValue": "20岁女生_清冷.flac", "description": "audio1"},
      {"nodeId": "167", "fieldName": "image", "fieldValue": "ancient_woman.png", "description": "picture3"},
      {"nodeId": "168", "fieldName": "image", "fieldValue": "crystal_palace.png", "description": "picture4"},
      {"nodeId": "169", "fieldName": "audio", "fieldValue": "20岁女生.flac", "description": "audio2"}
    ],
    "instanceType": "default",
    "usePersonalQueue": "false"
  }' | python3 -m json.tool 2>/dev/null || echo "API 响应异常"

echo ""
echo "✅ 所有视频已提交生成！"
