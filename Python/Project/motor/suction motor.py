from gpiozero import PWMOutputDevice, OutputDevice
import time
import serial

use_serial = False  # True로 바꾸면 블루투스(HC-06) 사용

if use_serial:
    ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

# 모터1 핀 설정
dir1 = OutputDevice(23)
brk1 = OutputDevice(24)
pwm1 = PWMOutputDevice(12, frequency=1000)

# 모터2 핀 설정
dir2 = OutputDevice(17)
brk2 = OutputDevice(27)
pwm2 = PWMOutputDevice(13, frequency=1000)

pwm1.value = 0
pwm2.value = 0

def set_motor(mode):
    if mode == 'T':
        print("start - Tennis mode (20%)")
        dir1.on()
        brk1.off()
        pwm1.value = 0.2
        dir2.off()
        brk2.off()
        pwm2.value = 0.2
    elif mode == 'B':
        print("start - Baseball mode (25%)")
        dir1.on()
        brk1.off()
        pwm1.value = 0.25
        dir2.off()
        brk2.off()
        pwm2.value = 0.25
    elif mode == 'P':
        print("start - Ping-pong mode (10%)")
        dir1.on()
        brk1.off()
        pwm1.value = 0.1
        dir2.off()
        brk2.off()
        pwm2.value = 0.1
    elif mode == 'S':
        print("stop")
        brk1.on()
        pwm1.value = 0
        brk2.on()
        pwm2.value = 0

try:
    while True:
        cmd = None
        if use_serial:
            if ser.in_waiting > 0:
                cmd = ser.read().decode().strip().upper()
        else:
            cmd = input("Enter T (Tennis), B (Baseball), P (Ping-pong), S (Stop), Q (Quit): ").strip().upper()
        if cmd:
            print(f"Received: {cmd}")
            if cmd in ['T', 'B', 'P', 'S']:
                set_motor(cmd)
            elif cmd == 'Q':
                print("Quit")
                break
            else:
                print("Invalid command")
except KeyboardInterrupt:
    pass
finally:
    pwm1.value = 0
    pwm2.value = 0
    brk1.on()
    brk2.on()
    if use_serial:
        ser.close()