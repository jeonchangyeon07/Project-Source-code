import RPi.GPIO as GPIO
import time

DIR3_PIN = 5
BRK3_PIN = 6
PWM3_PIN = 19

DIR4_PIN = 16
BRK4_PIN = 20
PWM4_PIN = 18

GPIO.setmode(GPIO.BCM)

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
        cmd = input("Enter F (Front), B (Back), L (Left), R (Right), S (Stop), Q (Quit): ").upper()
        
        if cmd == 'F':
            print("start - Front")
            GPIO.output(DIR3_PIN, GPIO.HIGH)
            GPIO.output(BRK3_PIN, GPIO.LOW)
            pwm3.ChangeDutyCycle(10)
            
            GPIO.output(DIR4_PIN, GPIO.HIGH)
            GPIO.output(BRK4_PIN, GPIO.LOW)
            pwm4.ChangeDutyCycle(10)
            
        elif cmd == 'B':
            print("start - Back")
            GPIO.output(DIR3_PIN, GPIO.LOW)
            GPIO.output(BRK3_PIN, GPIO.LOW)
            pwm3.ChangeDutyCycle(10)
            
            GPIO.output(DIR4_PIN, GPIO.LOW)
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
            
        elif cmd =='S':
            print("stop")
            GPIO.output(BRK3_PIN, GPIO.HIGH)
            pwm3.ChangeDutyCycle(0)
            
            GPIO.output(BRK4_PIN, GPIO.HIGH)
            pwm4.ChangeDutyCycle(0)
            
        elif cmd =='Q':
            print("Quit")
            break
        
except KeyboardInterrupt:
    pass

finally:
    pwm3.stop()
    pwm4.stop()
    GPIO.cleanup()