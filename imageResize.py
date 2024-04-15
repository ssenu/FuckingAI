from PIL import Image
import os


listname = ["파인애플", "키위", "복숭아", "바나나", "멜론", "레몬"]

for i in range(len(listname)):
    # 이미지 파일이 저장된 디렉토리 경로
    directory = f"C:/images1/{listname[i]}"

    # 디렉토리 내의 모든 파일 탐색
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 파일 경로
            filepath = os.path.join(root, file)
            # 이미지 파일인지 확인
            if filepath.endswith(".jpg") or filepath.endswith(".png"):
                # 이미지 열기
                img = Image.open(filepath)
                # 이미지를 RGB 모드로 변환 (알파 채널 제거)
                img = img.convert("RGB")
                # 이미지의 용량 확인
                img_size_kb = os.path.getsize(filepath) / 1024  # 파일 크기를 KB로 변환
                # 이미지 용량이 500KB 이상인 경우에만 압축
                if img_size_kb > 500:
                    # 이미지를 JPEG 형식으로 저장하여 압축 (품질 조절 가능)
                    img.save(filepath, quality=40)  # quality 값은 0에서 100까지 설정 가능
                # 이미지 닫기
                img.close()
                print(f"{filepath} 전처리 완료")
