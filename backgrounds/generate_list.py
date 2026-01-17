import os
import json

# 注意：必须以 https://raw.githubusercontent.com 开头
# 注意：末尾必须带一个斜杠 /
BASE_URL = "https://raw.githubusercontent.com/ikaorihara-source/RuKnot-Assets/main/backgrounds/"

def generate_json():
    files = []
    # 只扫描这些后缀
    valid_exts = ('.jpg', '.png', '.mp4', '.mov')

    for filename in os.listdir('.'):
        if not filename.lower().endswith(valid_exts): continue

        # 拼接 GitHub 原始链接
        raw_url = BASE_URL + filename

        # 判断是否为视频
        is_video = filename.lower().endswith(('.mp4', '.mov'))

        # 计算文件大小 (MB)
        size_mb = os.path.getsize(filename) / (1024 * 1024)

        files.append({
            "id": filename,            
            "name": filename.split('.')[0], 
            "url": raw_url,            # 存原始链接，镜像前缀由 App 加
            "isVideo": is_video,
            "size": f"{size_mb:.1f}MB"
        })

    # 生成 backgrounds.json
    with open('backgrounds.json', 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2, ensure_ascii=False)

    print(f"成功生成 {len(files)} 个文件！请把 backgrounds.json 上传到 GitHub。")

if __name__ == '__main__':
    generate_json()