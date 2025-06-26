import RPi.GPIO as GPIO
import time
import serial

use_serial = False

if use_serial:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DIR1_PIN = 23
BRK1_PIN = 24
PWM1_PIN = 12

DIR2_PIN = 17
BRK2_PIN = 27
PWM2_PIN = 13

GPIO.setup(DIR1_PIN, GPIO.OUT)
GPIO.setup(BRK1_PIN, GPIO.OUT)
GPIO.setup(PWM1_PIN, GPIO.OUT)

GPIO.setup(DIR2_PIN, GPIO.OUT)
GPIO.setup(BRK2_PIN, GPIO.OUT)
GPIO.setup(PWM2_PIN, GPIO.OUT)

pwm1 = GPIO.PWM(PWM1_PIN, 1000)
pwm2 = GPIO.PWM(PWM2_PIN, 1000)
pwm1.start(0)
pwm2.start(0)

DIR3_PIN = 5
BRK3_PIN = 6
PWM3_PIN = 19

DIR4_PIN = 16
BRK4_PIN = 20
PWM4_PIN = 18

GPIO.setup(DIR3_PIN, GPIO.OUT)
GPIO.setup(BRK3_PIN, GPIO.OUT)
GPIO.setup(PWM3_PIN, GPIO.OUT)

GPIO.setup(DIR4_PIN, GPIO.OUT)
GPIO.setup(BRK4_PIN, GPIO.OUT)
GPIO.setup(PWM4_PIN, GPIO.OUT)

pwm3 = GPIO.PWM(PWM3_PIN, 1000)
pwm4 = GPIO.PWM(PWM4_PIN, 1000)
pwm3.start(0)
pwm4.start(0)

try:
    while True:
        cmd = None

        if use_serial:
            if ser.in_waiting > 0:
                cmd = ser.read().decode().strip().upper()
        else:
            cmd = input("Enter command (T/B/P/F/B/L/R/S/Q): ").strip().upper()

        if cmd:
            print(f"Received: {cmd}")

            if cmd == 'T':
                print("start - tennis mode (20%)")
                GPIO.output(DIR1_PIN, GPIO.HIGH)
                GPIO.output(BRK1_PIN, GPIO.LOW)
                pwm1.ChangeDutyCycle(20)

                GPIO.output(DIR2_PIN, GPIO.LOW)
                GPIO.output(BRK2_PIN, GPIO.LOW)
                pwm2.ChangeDutyCycle(20)

            elif cmd == 'B':
                print("start - baseball mode (25%)")
                GPIO.output(DIR1_PIN, GPIO.HIGH)
                GPIO.output(BRK1_PIN, GPIO.LOW)
                pwm1.ChangeDutyCycle(25)

                GPIO.output(DIR2_PIN, GPIO.LOW)
                GPIO.output(BRK2_PIN, GPIO.LOW)
                pwm2.ChangeDutyCycle(25)

            elif cmd == 'P':
                print("start - ping-pong mode (10%)")
                GPIO.output(DIR1_PIN, GPIO.HIGH)
                GPIO.output(BRK1_PIN, GPIO.LOW)
                pwm1.ChangeDutyCycle(10)

                GPIO.output(DIR2_PIN, GPIO.LOW)
                GPIO.output(BRK2_PIN, GPIO.LOW)
                pwm2.ChangeDutyCycle(10)

            elif cmd == 'F':
                print("start - Forward")
                GPIO.output(DIR3_PIN, GPIO.HIGH)
                GPIO.output(BRK3_PIN, GPIO.LOW)
                pwm3.ChangeDutyCycle(10)

                GPIO.output(DIR4_PIN, GPIO.HIGH)
                GPIO.output(BRK4_PIN, GPIO.LOW)
                pwm4.ChangeDutyCycle(10)

            elif cmd == 'L':
                print("start - Left")
                GPIO.output(DIR3_PIN, GPIO.HIGH)
                GPIO.output(BRK3_PIN, GPIO.LOW)
                pwm3.ChangeDutyCycle(10)

                GPIO.output(DIR4_PIN, GPIO.HIGH)
                GPIO.output(BRK4_PIN, GPIO.LOW)
                pwm4.ChangeDutyCycle(15)

            elif cmd == 'R':
                print("start - Right")
                GPIO.output(DIR3_PIN, GPIO.HIGH)
                GPIO.output(BRK3_PIN, GPIO.LOW)
                pwm3.ChangeDutyCycle(15)

                GPIO.output(DIR4_PIN, GPIO.HIGH)
                GPIO.output(BRK4_PIN, GPIO.LOW)
                pwm4.ChangeDutyCycle(10)

            elif cmd == 'S':
                print("Stop all motors")
                GPIO.output(BRK1_PIN, GPIO.HIGH)
                GPIO.output(BRK2_PIN, GPIO.HIGH)
                GPIO.output(BRK3_PIN, GPIO.HIGH)
                GPIO.output(BRK4_PIN, GPIO.HIGH)

                pwm1.ChangeDutyCycle(0)
                pwm2.ChangeDutyCycle(0)
                pwm3.ChangeDutyCycle(0)
                pwm4.ChangeDutyCycle(0)

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
    pwm3.stop()
    pwm4.stop()
    GPIO.cleanup()
    if use_serial:
        ser.close()