from gpiozero import PWMOutputDevice, Button
import time

# 모터 설정 (GPIO 핀 번호는 상황에 맞게 수정하세요)
motor_left = PWMOutputDevice(17)
motor_right = PWMOutputDevice(18)

# 버튼 설정 (예: GPIO 2번 핀에 연결)
stop_button = Button(2)

# 공 종류별 모터 속도 설정 (왼쪽, 오른쪽)
speed_profiles = {
    'pingpong': (0.3, 0.3),     # 탁구공
    'tennis': (0.6, 0.6),       # 테니스공
    'baseball': (1.0, 1.0)      # 야구공
}

# 공 종류에 따라 속도 설정 함수
def set_mode(ball_type):
    if ball_type not in speed_profiles:
        print(f"[오류] '{ball_type}'은 지원하지 않는 공 종류입니다.")
        return
    
    left_speed, right_speed = speed_profiles[ball_type]
    motor_left.value = left_speed
    motor_right.value = right_speed
    print(f"[{ball_type}] 모터 속도 설정: 왼쪽={left_speed}, 오른쪽={right_speed}")

# === 테스트: 모드 선택 후 버튼으로 멈추기 ===

# 원하는 공 종류로 설정 (필요시 바꾸세요)
set_mode('pingpong')  # 예: 'tennis' 또는 'baseball'

print("▶ 모터 작동 중... 버튼을 누르면 정지합니다.")

# 계속 회전하다가 버튼이 눌리면 정지
while True:
    if stop_button.is_pressed:
        print("⏹ 버튼 눌림: 모터 정지 중...")
        motor_left.value = 0
        motor_right.value = 0
        print("✅ 모터 정지 완료")
        break
    time.sleep(0.1)
