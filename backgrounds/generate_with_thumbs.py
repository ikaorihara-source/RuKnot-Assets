import os
import json
import cv2  # OpenCV，用来截取视频画面
from PIL import Image # Pillow，用来压缩图片

# ★★★ 你的 GitHub 仓库地址 ★★★
BASE_URL = "https://raw.githubusercontent.com/ikaorihara-source/RuKnot-Assets/main/backgrounds/"

def make_thumbnail(filename):
    thumb_name = "thumb_" + os.path.splitext(filename)[0] + ".jpg"
    
    # 如果缩略图已经存在，就不重新生成了
    if os.path.exists(thumb_name):
        return thumb_name
        
    print(f"正在生成缩略图: {filename} ...")
    
    try:
        # A. 如果是视频：截取第一帧
        if filename.endswith(('.mp4', '.mov')):
            cap = cv2.VideoCapture(filename)
            success, frame = cap.read()
            if success:
                # 把截取到的画面保存为 jpg
                cv2.imwrite(thumb_name, frame)
                cap.release()
                # 再次用 Pillow 打开并压缩尺寸
                compress_image(thumb_name)
                return thumb_name
            cap.release()
            
        # B. 如果是图片：直接压缩
        elif filename.endswith(('.jpg', '.png', '.jpeg')):
            img = Image.open(filename)
            # 转成 RGB (防止 PNG 透明底变黑)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            # 保存为缩略图
            img.save(thumb_name)
            compress_image(thumb_name)
            return thumb_name
            
    except Exception as e:
        print(f"❌ 生成失败 {filename}: {e}")
        return filename # 失败了就用原图兜底

    return filename

def compress_image(image_path):
    # 把图片强制缩小到高度 300px (宽度自适应)
    try:
        img = Image.open(image_path)
        base_height = 300
        if img.height > base_height:
            w_percent = (base_height / float(img.height))
            h_size = int((float(img.width) * float(w_percent)))
            img = img.resize((h_size, base_height), Image.Resampling.LANCZOS)
            img.save(image_path, quality=70) # 70% 质量足够做预览了
    except:
        pass

def generate_json():
    files = []
    valid_exts = ('.jpg', '.png', '.jpeg', '.mp4', '.mov')
    
    for filename in os.listdir('.'):
        if not filename.lower().endswith(valid_exts): continue
        if filename.startswith('thumb_'): continue # 跳过缩略图本身

        # 1. 生成缩略图文件
        thumb_filename = make_thumbnail(filename)
        
        # 2. 计算大小
        size_mb = os.path.getsize(filename) / (1024 * 1024)

        files.append({
            "id": filename,
            "name": filename.split('.')[0],
            "url": BASE_URL + filename,          # 原文件链接
            "thumb": BASE_URL + thumb_filename,  # ★ 新增：缩略图链接
            "isVideo": filename.lower().endswith(('.mp4', '.mov')),
            "size": f"{size_mb:.1f}MB"
        })

    with open('backgrounds.json', 'w', encoding='utf-8') as f:
        json.dump(files, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 完成！生成了 backgrounds.json 和 {len(files)} 张缩略图。")
    print("👉 请把所有新增的 thumb_xxx.jpg 也一起上传到 GitHub！")

if __name__ == '__main__':
    generate_json()