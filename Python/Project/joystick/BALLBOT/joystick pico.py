import machine
import bluetooth
import aioble
import asyncio
import struct
import time

# --- 1. 설정 ---
# 조이스틱 ADC 핀
joy_y = machine.ADC(machine.Pin(26))  # Y축: GP26
joy_x = machine.ADC(machine.Pin(27))  # X축: GP27

# 버튼 핀 설정 (내장 풀업 저항 사용)
button_pins = {
    # 버튼 이름: GPIO 핀 번호
    "Joy_Btn": 28, "Btn_1": 21, "Btn_2": 20,
    "Btn_3": 19, "Btn_4": 18, "Btn_5": 17, "Btn_6": 16
}
# 버튼 이름을 순서대로 리스트로 만들어 비트마스킹에 사용
button_order = ["Joy_Btn", "Btn_1", "Btn_2", "Btn_3", "Btn_4", "Btn_5", "Btn_6"]
buttons = {name: machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for name, pin in button_pins.items()}

# BLE 서비스 및 특성 UUID
_CONTROL_SERVICE_UUID = bluetooth.UUID(0x1848)
_JOY_Y_CHAR_UUID = bluetooth.UUID(0x2A6E)  # Y축
_JOY_X_CHAR_UUID = bluetooth.UUID(0x2A6F)  # X축
_BUTTON_CHAR_UUID = bluetooth.UUID(0x2A70) # 버튼 상태

# BLE 장치 이름
_DEVICE_NAME = "PicoRobotControllerV2"

# --- 2. 비동기 BLE 주변장치(Peripheral) 작업 ---
async def peripheral_task():
    print("BLE 주변 장치 시작 중...")

    service = aioble.Service(_CONTROL_SERVICE_UUID)
    char_y = aioble.Characteristic(service, _JOY_Y_CHAR_UUID, read=True)
    char_x = aioble.Characteristic(service, _JOY_X_CHAR_UUID, read=True)
    char_buttons = aioble.Characteristic(service, _BUTTON_CHAR_UUID, read=True)
    aioble.register_services(service)

    while True:
        print(f"'{_DEVICE_NAME}'으로 Advertising 시작...")
        async with await aioble.advertise(
            250000, name=_DEVICE_NAME, services=[_CONTROL_SERVICE_UUID]
        ) as connection:
            print(f"연결 성공: {connection.device}")

            while connection.is_connected():
                # --- 조이스틱 값 읽기 ---
                y_val = joy_y.read_u16()
                x_val = joy_x.read_u16()

                # --- 버튼 상태 읽고 비트마스크 생성 ---
                # 버튼을 누르면 0(LOW), 안 누르면 1(HIGH)
                button_mask = 0
                for i, name in enumerate(button_order):
                    if buttons[name].value() == 0: # 버튼이 눌렸다면
                        button_mask |= (1 << i) # 해당 순서의 비트를 1로 설정

                # --- 데이터 패킹 ---
                packed_y = struct.pack("<H", y_val)
                packed_x = struct.pack("<H", x_val)
                # 버튼 상태는 1바이트(Unsigned Char)로 충분
                packed_buttons = struct.pack("<B", button_mask)

                # --- 특성 값 쓰기 ---
                char_y.write(packed_y)
                char_x.write(packed_x)
                char_buttons.write(packed_buttons)

                # 전송 값 확인용 출력 (디버깅 시 주석 해제)
                # print(f"Y: {y_val}, X: {x_val}, BTN: {button_mask:07b}")

                await asyncio.sleep_ms(50) # 50ms 마다 전송

            print(f"연결 끊김: {connection.device}")

# --- 3. 메인 함수 ---
async def main():
    await peripheral_task()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("프로그램 중단됨")

