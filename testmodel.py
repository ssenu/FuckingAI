import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn
import torchvision.transforms as T


class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels, hidden_dim):
        super(BasicBlock, self).__init__()

        # 합성곱
        self.conv1 = nn.Conv2d(in_channels, hidden_dim, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(hidden_dim, out_channels, kernel_size=3, padding=1)
        self.relu = nn.ReLU()

        # stride
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)

        return x
    
class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()

        # 합성곱 기본 블록
        self.block1 = BasicBlock(in_channels=3, out_channels=32, hidden_dim=16)
        self.block2 = BasicBlock(in_channels=32, out_channels=128, hidden_dim=64)
        self.block3 = BasicBlock(in_channels=128, out_channels=256, hidden_dim=128)

        # 분류기
        self.fc1 = nn.Linear(in_features=4096, out_features=2048)
        self.fc2 = nn.Linear(in_features=2048, out_features=256)
        self.fc3 = nn.Linear(in_features=256, out_features=num_classes)

        # 활성화 함수
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = torch.flatten(x, start_dim=1)

        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)

        return x
    

# 이미지를 불러오고 전처리하는 함수
def load_and_preprocess_image(image_path):
    image = Image.open(image_path)
    preprocess = transforms = T.Compose([
        T.Resize((32, 32)),  # 원하는 크기로 조정
        T.RandomCrop((32, 32), padding=4), # 32x32로 잘라내어 가장자리에 padding 4 추가
        T.RandomHorizontalFlip(p=0.5), # 이미지를 50% 확률로 수평으로 뒤집기
        T.ToTensor(),
        T.Normalize(mean=(0.6700974, 0.59195954, 0.43890765), std=(0.26962617, 0.2685, 0.313767)), # 정규화
  #  T.ToPILImage()
])
    image = preprocess(image)
    # 배치 차원을 추가하여 모델에 입력할 수 있도록 함
    image = image.unsqueeze(0)
    return image



def imageFunc(imagepath):
# 모델 불러오기
    model = CNN(num_classes=12)
    model.load_state_dict(torch.load("CNNmodel.pth"))
    model.eval()



    # 클래스 목록
    class_names = ['딸기', 
                '레몬',
                '망고',
                '멜론',
                '바나나',
                '배',
                '복숭아',
                '사과',
                '수박',
                '키위',
                '파인애플',
                '포도']


    # 이미지의 경로
    image_path = imagepath

    # 이미지 불러오기 및 전처리
    image = load_and_preprocess_image(image_path)

    # 모델로부터 클래스 예측
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    # 예측된 클래스 출력
    predicted_class = class_names[predicted.item()]
    # print("Predicted class:", predicted_class)

    return predicted_class

