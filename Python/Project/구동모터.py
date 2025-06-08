import bluetooth
from gpiozero import Motor
from time import sleep

# 모터 설정
motor_left = Motor(forward=5, backward=6)
motor_right = Motor(forward=23, backward=24)

# 동작 함수
def go_forward():
    motor_left.forward()
    motor_right.forward()
    print("▶ 직진")

def go_backward():
    motor_left.backward()
    motor_right.backward()
    print("◀ 후진")

def turn_left():
    motor_left.backward()
    motor_right.forward()
    print("⟲ 좌회전")

def turn_right():
    motor_left.forward()
    motor_right.backward()
    print("⟳ 우회전")

def stop():
    motor_left.stop()
    motor_right.stop()
    print("⏹ 정지")

# 블루투스 연결 대기
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", 1))
server_socket.listen(1)
print("📡 블루투스 연결 대기 중...")

client_socket, address = server_socket.accept()
print(f"✅ 연결됨: {address}")

try:
    while True:
        data = client_socket.recv(1024).decode().strip()
        print(f"📥 받은 명령: {data}")
        
        if data == "forward":
            go_forward()
        elif data == "backward":
            go_backward()
        elif data == "left":
            turn_left()
        elif data == "right":
            turn_right()
        elif data == "stop":
            stop()
        else:
            print("❓ 알 수 없는 명령")
except KeyboardInterrupt:
    print("🔚 종료 중...")
    stop()
    client_socket.close()
    server_socket.close()
