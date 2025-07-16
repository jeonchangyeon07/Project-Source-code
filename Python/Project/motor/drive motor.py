from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time

DIR3_PIN = 5
BRK3_PIN = 6
PWM3_PIN = 19

DIR4_PIN = 16
BRK4_PIN = 20
PWM4_PIN = 18

# gpiozero 객체 생성
dir3 = DigitalOutputDevice(DIR3_PIN)
brk3 = DigitalOutputDevice(BRK3_PIN)
pwm3 = PWMOutputDevice(PWM3_PIN, frequency=1000)

dir4 = DigitalOutputDevice(DIR4_PIN)
brk4 = DigitalOutputDevice(BRK4_PIN)
pwm4 = PWMOutputDevice(PWM4_PIN, frequency=1000)

try:
    while True:
        cmd = input("Enter F (Front), B (Back), L (Left), R (Right), S (Stop), Q (Quit): ").upper()
        
        if cmd == 'F':
            print("start - Front")
            dir3.on()
            brk3.off()
            pwm3.value = 0.1
            
            dir4.on()
            brk4.off()
            pwm4.value = 0.1
            
        elif cmd == 'B':
            print("start - Back")
            dir3.off()
            brk3.off()
            pwm3.value = 0.1
            
            dir4.off()
            brk4.off()
            pwm4.value = 0.1
            
        elif cmd == 'L':
            print("start - Left")
            dir3.on()
            brk3.off()
            pwm3.value = 0.1
            
            dir4.on()
            brk4.off()
            pwm4.value = 0.15
            
        elif cmd == 'R':
            print("start - Right")
            dir3.on()
            brk3.off()
            pwm3.value = 0.15
            
            dir4.on()
            brk4.off()
            pwm4.value = 0.1
            
        elif cmd =='S':
            print("stop")
            brk3.on()
            pwm3.value = 0
            
            brk4.on()
            pwm4.value = 0
            
        elif cmd =='Q':
            print("Quit")
            break
        
except KeyboardInterrupt:
    pass

finally:
    pwm3.value = 0
    pwm4.value = 0
    brk3.on()
    brk4.on()
    # gpiozero는 cleanup이 필요 없음