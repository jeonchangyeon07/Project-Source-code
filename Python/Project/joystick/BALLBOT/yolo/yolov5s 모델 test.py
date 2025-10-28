import torch
import cv2
import numpy as np

# ---------------------------------------------------------------- #
# 1. 모델 로드
# ---------------------------------------------------------------- #
# 'yolov5' 폴더가 없으면 자동으로 다운로드합니다.
# 'custom'을 사용해 로컬에 있는 best.pt 가중치를 불러옵니다.
try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Source code/Project-Source-code/Python/Project/joystick/BALLBOT/yolo/best.pt', force_reload=True)
    print("YOLOv5 모델 로딩 성공!")
except Exception as e:
    print(f"모델 로딩 중 오류 발생: {e}")
    exit() # 모델 로딩 실패 시 프로그램 종료

# (선택사항) 모델의 신뢰도(Confidence) 임계값 설정
# 이 값보다 높은 신뢰도를 가진 객체만 감지합니다. (기본값: 0.25)
# model.conf = 0.5 

# ---------------------------------------------------------------- #
# 2. 웹캠 설정
# ---------------------------------------------------------------- #
# 0은 보통 내장 카메라입니다. 로지텍 스트림캠이 다른 번호일 수 있으니
# 0으로 안되면 1, 2 등으로 바꿔서 시도해보세요.
cap = cv2.VideoCapture(1) 

if not cap.isOpened():
    print("카메라를 열 수 없습니다. 카메라 인덱스를 확인해주세요.")
    exit()

print("카메라 준비 완료. 'q' 키를 누르면 종료됩니다.")

# ---------------------------------------------------------------- #
# 3. 실시간 감지 루프
# ---------------------------------------------------------------- #
while True:
    # 카메라에서 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 프로그램을 종료합니다.")
        break

    # 모델에 프레임 입력하여 객체 감지 수행
    results = model(frame)

    # 감지 결과를 화면에 렌더링 (바운딩 박스, 클래스 이름, 신뢰도 표시)
    # results.render()는 결과가 그려진 numpy 배열을 반환합니다.
    rendered_frame = np.squeeze(results.render())

    # 결과 화면 보여주기
    cv2.imshow('YOLOv5 Real-Time Detection', rendered_frame)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------------------------------------------------------- #
# 4. 자원 해제
# ---------------------------------------------------------------- #
cap.release()
cv2.destroyAllWindows()
print("프로그램을 종료합니다.")