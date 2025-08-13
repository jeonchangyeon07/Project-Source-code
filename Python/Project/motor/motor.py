from gpiozero import PhaseEnableMotor, OutputDevice
from time import sleep


INTAKE_MOTOR1_DIR_PIN = 23
INTAKE_MOTOR1_BRK_PIN = 24
INTAKE_MOTOR1_PWM_PIN = 12

INTAKE_MOTOR2_DIR_PIN = 17
INTAKE_MOTOR2_BRK_PIN = 27
INTAKE_MOTOR2_PWM_PIN = 13


DRIVE_LEFT_DIR_PIN = 5
DRIVE_LEFT_BRK_PIN = 6
DRIVE_LEFT_PWM_PIN = 19

DRIVE_RIGHT_DIR_PIN = 16
DRIVE_RIGHT_BRK_PIN = 20
DRIVE_RIGHT_PWM_PIN = 18


intake_motor1 = PhaseEnableMotor(phase=INTAKE_MOTOR1_DIR_PIN, enable=INTAKE_MOTOR1_PWM_PIN)
intake_brake1 = OutputDevice(INTAKE_MOTOR1_BRK_PIN, initial_value=True)

intake_motor2 = PhaseEnableMotor(phase=INTAKE_MOTOR2_DIR_PIN, enable=INTAKE_MOTOR2_PWM_PIN)
intake_brake2 = OutputDevice(INTAKE_MOTOR2_BRK_PIN, initial_value=True)

drive_left = PhaseEnableMotor(phase=DRIVE_LEFT_DIR_PIN, enable=DRIVE_LEFT_PWM_PIN)
drive_brake_left = OutputDevice(DRIVE_LEFT_BRK_PIN, initial_value=True)

drive_right = PhaseEnableMotor(phase=DRIVE_RIGHT_DIR_PIN, enable=DRIVE_RIGHT_PWM_PIN)
drive_brake_right = OutputDevice(DRIVE_RIGHT_BRK_PIN, initial_value=True)


def start_intake(speed_percent):
    speed = speed_percent / 100.0
    print(f"흡입 모터 작동 (속도: {speed_percent}%)")
    
    intake_brake1.off()
    intake_brake2.off()
    
    intake_motor1.forward(speed)
    intake_motor2.backward(speed)

def move_robot(left_speed_percent, right_speed_percent):
    left_speed = left_speed_percent / 100.0
    right_speed = right_speed_percent / 100.0
    
    drive_brake_left.off()
    drive_brake_right.off()
    
    if left_speed >= 0:
        drive_left.forward(left_speed)
    else:
        drive_left.backward(abs(left_speed))
        
    if right_speed >= 0:
        drive_right.forward(right_speed)
    else:
        drive_right.backward(abs(right_speed))

def stop_all_motors():
    print("모든 모터 정지")
    
    intake_motor1.stop()
    intake_motor2.stop()
    drive_left.stop()
    drive_right.stop()
    
    intake_brake1.on()
    intake_brake2.on()
    drive_brake_left.on()
    drive_brake_right.on()


try:
    print("로봇 제어 프로그램을 시작합니다. (T/B/P/F/L/R/S/Q)")
    stop_all_motors()

    while True:
        cmd = input("명령 입력: ").strip().upper()

        if cmd == 'T':
            start_intake(20)
        elif cmd == 'B':
            start_intake(25)
        elif cmd == 'P':
            start_intake(10)
        
        elif cmd == 'F':
            print("전진")
            move_robot(10, 10)
        elif cmd == 'L':
            print("좌회전")
            move_robot(10, 15)
        elif cmd == 'R':
            print("우회전")
            move_robot(15, 10)
            
        elif cmd == 'S':
            stop_all_motors()
            
        elif cmd == 'Q':
            print("프로그램을 종료합니다.")
            break
        else:
            print("알 수 없는 명령입니다.")

except KeyboardInterrupt:
    print("\n사용자에 의해 프로그램이 중단되었습니다.")

finally:
    stop_all_motors()
    intake_motor1.close()
    intake_brake1.close()
    intake_motor2.close()
    intake_brake2.close()
    drive_left.close()
    drive_brake_left.close()
    drive_right.close()
    drive_brake_right.close()
    print("GPIO 리소스 정리 완료.")