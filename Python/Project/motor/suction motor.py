import RPi.GPIO as GPIO
import time
import serial

use_serial = False  # True로 바꾸면 블루투스(HC-06) 사용

if use_serial:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)  # 대소문자 오타 수정!

# 모터1 핀 설정
DIR1_PIN = 23
BRK1_PIN = 24
PWM1_PIN = 12

# 모터2 핀 설정
DIR2_PIN = 17
BRK2_PIN = 27
PWM2_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(DIR1_PIN, GPIO.OUT)
GPIO.setup(BRK1_PIN, GPIO.OUT)
GPIO.setup(PWM1_PIN, GPIO.OUT)

GPIO.setup(DIR2_PIN, GPIO.OUT)
GPIO.setup(BRK2_PIN, GPIO.OUT)
GPIO.setup(PWM2_PIN, GPIO.OUT)

pwm1 = GPIO.PWM(PWM1_PIN, 1000)  # 1kHz
pwm2 = GPIO.PWM(PWM2_PIN, 1000)
pwm1.start(0)
pwm2.start(0)

try:
    while True:
        cmd = None

        # 입력 방식에 따라 명령 받기
        if use_serial:
            if ser.in_waiting > 0:
                cmd = ser.read().decode().strip().upper()
        else:
            cmd = input("Enter T (Tennis), B (Baseball), P (Ping-pong), S (Stop), Q (Quit): ").strip().upper()

        # 명령이 들어왔을 때만 처리
        if cmd:
            print(f"Received: {cmd}")

            if cmd == 'T':
                print("start - Tennis mode (20%)")
                GPIO.output(DIR1_PIN, GPIO.HIGH)
                GPIO.output(BRK1_PIN, GPIO.LOW)
                pwm1.ChangeDutyCycle(20)

                GPIO.output(DIR2_PIN, GPIO.LOW)
                GPIO.output(BRK2_PIN, GPIO.LOW)
                pwm2.ChangeDutyCycle(20)

            elif cmd == 'B':
                print("start - Baseball mode (25%)")
                GPIO.output(DIR1_PIN, GPIO.HIGH)
                GPIO.output(BRK1_PIN, GPIO.LOW)
                pwm1.ChangeDutyCycle(25)

                GPIO.output(DIR2_PIN, GPIO.LOW)
                GPIO.output(BRK2_PIN, GPIO.LOW)
                pwm2.ChangeDutyCycle(25)

            elif cmd == 'P':
                print("start - Ping-pong mode (10%)")
                GPIO.output(DIR1_PIN, GPIO.HIGH)
                GPIO.output(BRK1_PIN, GPIO.LOW)
                pwm1.ChangeDutyCycle(10)

                GPIO.output(DIR2_PIN, GPIO.LOW)
                GPIO.output(BRK2_PIN, GPIO.LOW)
                pwm2.ChangeDutyCycle(10)

            elif cmd == 'S':
                print("stop")
                GPIO.output(BRK1_PIN, GPIO.HIGH)
                pwm1.ChangeDutyCycle(0)

                GPIO.output(BRK2_PIN, GPIO.HIGH)
                pwm2.ChangeDutyCycle(0)

            elif cmd == 'Q':
                print("Quit")
                break

            else:
                print("Invalid command")

except KeyboardInterrupt:
    pass

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    if use_serial:
        ser.close()