import cv2
import numpy as np
import glob
import os
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

def resize_image(img, target_width, target_height):
    h, w = img.shape[:2]
    aspect = w / h
    
    if aspect > target_width / target_height:
        new_w = target_width
        new_h = int(new_w / aspect)
    else:
        new_h = target_height
        new_w = int(new_h * aspect)
    
    resized = cv2.resize(img, (new_w, new_h))
    
    # 創建一個白色背景
    canvas = np.ones((target_height, target_width, 3), dtype=np.uint8) * 255
    
    # 計算居中位置
    x_offset = (target_width - new_w) // 2
    y_offset = (target_height - new_h) // 2
    
    # 將調整大小後的圖像放在畫布中央
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    
    return canvas

def create_photo_collage(input_images, output_path):
    # 設定輸出圖像的尺寸和解析度
    dpi = 300
    width_inches, height_inches = 6, 4
    width_pixels = int(width_inches * dpi)
    height_pixels = int(height_inches * dpi)
    
    # 創建白色背景
    output_image = np.ones((height_pixels, width_pixels, 3), dtype=np.uint8) * 255
    
    # 計算每張圖片的尺寸和間距
    img_width = width_pixels // 2 - 40
    img_height = height_pixels // 2 - 40
    h_spacing = (width_pixels - img_width * 2) // 3
    v_spacing = (height_pixels - img_height * 2) // 3
    
    # 定義四張圖片的位置
    positions = [
        (h_spacing, v_spacing),
        (h_spacing * 2 + img_width, v_spacing),
        (h_spacing, v_spacing * 2 + img_height),
        (h_spacing * 2 + img_width, v_spacing * 2 + img_height)
    ]
    
    # 處理每張輸入圖片
    for i, img_path in enumerate(input_images):
        # 讀取圖片
        # img = cv2.imread(img_path)
        img = None
        if img_path == "":
            img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        else: 
            pil_img = Image.open(img_path)
            img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
        
        # pil_img = Image.open(img_path)

        # img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)


        if img is None:
            print(f"無法讀取圖片: {img_path}")
            img = np.ones((100, 100, 3), dtype=np.uint8) * 255
            # continue

        if(img.shape[0] > img.shape[1]):
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        
        # 調整圖片大小並保持比例
        img_resized = resize_image(img, img_width, img_height)
        
        # 將調整後的圖片放置到輸出圖像中
        print(i)
        x, y = positions[i]
        output_image[y:y+img_height, x:x+img_width] = img_resized
    
    # 保存輸出圖像
    cv2.imwrite(output_path, output_image)
    print(f"拼貼圖片已保存至: {output_path}")





# 使用示例
img_paths = glob.glob("/Users/rinku/Album/4x6x4/*.*", recursive=True)
print(len(img_paths))
for count, idx in enumerate(range(0, len(img_paths), 4)):
    output = f"./output/collage_4_{count}.jpg"
    print(idx)
    input_imgs = list()
    for j in range(4):
        if idx+j > len(img_paths) - 1:
            # input_imgs.append(np.ones((100, 100, 3), dtype=np.uint8) * 255)
            input_imgs.append("")
            continue
        
        input_imgs.append(img_paths[idx+j])

    print('len=', len(input_imgs))

    create_photo_collage(input_imgs, output)



# input_images = [
#     "1.jpg",
#     "2.jpg",
#     "3.jpg",
#     "4.jpg"
# ]
# output_path = "output_collage.jpg"

# create_photo_collage(input_images, output_path)