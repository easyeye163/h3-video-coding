# RunningHub 上传资源 fileName 缓存（2026-09-02 上传）

> fileName 一天内可复用，无需重复上传。超过有效期需重新上传。

## 音频资源

| 资源 | fileName | 原始文件 |
|------|----------|----------|
| 主歌一·夜泊秦淮 15s | `api/e9e8e4a418211122f7b3084a4fc68f48803a6d9fed9385fda20ee3e68c2f8b61.mp3` | `audio/music/wan_an_bao_verse1_15s.mp3` |
| Pre-Chorus·烟雨如织 15s | `api/ed8417460fb40a1b11f6839ff6b8d62ca06e511de4e0316665a123d109a3de3f.mp3` | `audio/music/wan_an_bao_prechorus_15s.mp3` |
| 副歌·画舫摇呀摇 15s | `api/e6ab1c5ed366a256f2daaa35cea435fd46f672a50dc403b8dbb792fba88255ce.mp3` | `audio/music/wan_an_bao_chorus_15s.mp3` |
| 终极副歌·古今交错 15s | `api/7d41462e4412de39dfee7e86165261fe083376a242dc3e2736b1eab261f7c59a.mp3` | `audio/music/wan_an_bao_final_chorus_15s.mp3` |
| 画钿副歌 15s（鹤形路） | 需重新上传 | `audio/music/huadian_15s.mp3` |
| 静音占位符 3s | `api/6135ce6d9cf7e62ba07612d65a5da687c155923b5cb16117833c45febad8f224.mp3` | `audio/voices/silent_placeholder.mp3` |

## 图片资源

| 资源 | fileName | 原始文件 |
|------|----------|----------|
| 林小溪角色三视图 | `api/19d6508bc565345e0a3ad64c3dff576389920f6c7db417b7b7efe07c26c04ad6.png` | `images/songkou_3d_characters/lin_xiaoxi_3d_turnaround.png` |
| 万安堡场景 | `api/2f245a10cbf61e4f96920fcccfae8d539b97b86a37a144675b5656a33d6f4684.png` | `images/songkou_3d_scenes_ig2img/万安堡_ig2img.png` |
| 鹤形路场景 | 需重新上传 | `images/songkou_3d_scenes_ig2img/鹤形路_ig2img.png` |
| 男生仙侠角色 | 需重新上传 | `images/songkou_3d_characters/global_ai_protagonist_xianxia_ig2img.png` |

## 使用方法

```python
# 直接用 fileName 作为 fieldValue，不需要 GitHub URL
payload = {
    'nodeInfoList': [
        {'nodeId': '137', 'fieldName': 'image', 'fieldValue': 'api/19d6508...26c04ad6.png'},  # 角色
        {'nodeId': '166', 'fieldName': 'image', 'fieldValue': 'api/2f245a1...33d6f4684.png'},  # 场景
        {'nodeId': '165', 'fieldName': 'audio', 'fieldValue': 'api/7d41462e...61f7c59a.mp3'},  # audio1
        {'nodeId': '169', 'fieldName': 'audio', 'fieldValue': 'api/6135ce6d...bad8f224.mp3'},  # audio2(静音)
    ],
}
```

## 上传接口

```bash
# 旧版（推荐，返回 fileName）
curl -s --location 'https://www.runninghub.cn/task/openapi/upload'   --header 'Authorization: Bearer $RUNNINGHUB_API_KEY'   --form 'apiKey="$RUNNINGHUB_API_KEY"'   --form 'file=@local_file.mp3'   --form 'fileType="input"'

# 新版（返回 fileName + download_url）
curl -s --location 'https://www.runninghub.cn/openapi/v2/media/upload/binary'   --header 'Authorization: Bearer $RUNNINGHUB_API_KEY'   --form 'file=@local_file.mp3'
```
