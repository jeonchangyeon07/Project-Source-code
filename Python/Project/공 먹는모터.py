import RPi.GPIO as GPIO
import time

DIR_PIN = 23
BRK_PIN = 24
PWM_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(BRK_PIN, GPIO.OUT)
GPIO.setup(PWM_PIN, GPIO.OUT)

pwm = GPIO.PWM(PWM_PIN, 1000)
pwm.start(0)

try:
    while True:
        cmd = input("Enter T (Tennis), B (Baseball), P (Ping-pong), S (Stop), Q (Quit): ").upper()
        
        if cmd == 'T':
            print("start - tennis mode (20%)")
            GPIO.output(DIR_PIN, GPIO.HIGH)
            GPIO.output(BRK_PIN, GPIO.LOW)
            pwm.ChangeDutyCycle(20)
            
        elif cmd == 'B':
            print("start - Baseball mode (25%)")
            GPIO.output(DIR_PIN, GPIO.HIGH)
            GPIO.output(BRK_PIN, GPIO.LOW)
            pwm.ChangeDutyCycle(25)
            
        elif cmd == 'P':
            print("start - Ping-pong mode (10%)")
            GPIO.output(DIR_PIN, GPIO.HIGH)
            GPIO.output(BRK_PIN, GPIO.LOW)
            pwm.ChangeDutyCycle(10)
            
        elif cmd =='S':
            print("stop")
            GPIO.output(BRK_PIN, GPIO.HIGH)
            pwm.ChangeDutyCycle(0)
            
        elif cmd =='Q':
            print("Quit")
            break

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()