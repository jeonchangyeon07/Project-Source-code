import RPi.GPIO as GPIO
import time
import serial

use_serial = False

if use_serial:
    ser = serial.serial('/dev/serial0', baudrate=9600, timeout=1)

DIR1_PIN = 23
BRK1_PIN = 24
PWM1_PIN = 12

DIR2_PIN = 17
BRK2_PIN = 27
PWM2_PIN = 13

GPIO.setmode(GPIO.BCM)

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

try:
    while True:
        cmd = None
        
        if use_serial:
            if ser.in_waiting > 0:
                cmd = ser.read().decode().strip().upper()
        else:
            cmd = input("Enter T (Tennis), B (Baseball), P (Ping-pong), S (Stop), Q (Quit): ").upper()
            
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
            
        elif cmd =='S':
            print("stop")
            GPIO.output(BRK1_PIN, GPIO.HIGH)
            pwm1.ChangeDutyCycle(0)
            
            GPIO.output(BRK2_PIN, GPIO.HIGH)
            pwm2.ChangeDutyCycle(0)
            
        elif cmd =='Q':
            print("Quit")
            break
        
        else:
            print("invalid command")

except KeyboardInterrupt:
    pass

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    if use_serial:
        ser.close()