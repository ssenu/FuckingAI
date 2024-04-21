from PIL import Image
import os


listname = ["사과", "배", "포도", "수박", "귤", "망고", "자몽", "딸기", "파인애플", "키위", "복숭아", "바나나", "멜론", "레몬"]

for i in range(len(listname)):

    directory = f"C:/images1/{listname[i]}"

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if filepath.endswith(".jpg") or filepath.endswith(".png"):
                img = Image.open(filepath)
                img = img.convert("RGB")
                img_size_kb = os.path.getsize(filepath) / 1024  # 파일 크기를 KB로 변환
                # 이미지 용량이 500KB 이상인 경우에만 압축
                if img_size_kb > 500:
                    # 이미지를 JPEG 형식으로 저장하여 압축 (품질 조절 가능)
                    img.save(filepath, quality=40)  # quality 값은 0에서 100까지 설정 가능
                img.close()
                print(f"{filepath} 전처리 완료")
