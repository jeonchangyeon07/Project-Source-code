import machine
import bluetooth
import aioble
import asyncio
import struct

# 조이스틱 ADC 핀 설정
joy_x = machine.ADC(machine.Pin(26))  # X축: GP26

# BLE 서비스 및 특성 UUID 정의
# Nordic Semiconductor의 UART Service UUID를 변형하여 사용하거나,
# 직접 생성한 128-bit UUID를 사용하는 것이 좋습니다.
# 여기서는 예시로 간단한 16-bit UUID를 사용합니다.
_SERVICE_UUID = bluetooth.UUID(0x181A)  # 예: Environmental Sensing 서비스
_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A6E) # 예: Temperature 특성

# BLE 장치 이름 설정
_DEVICE_NAME = "PicoJoystick"

# 비동기 BLE 주변 장치(Peripheral) 작업을 위한 함수
async def peripheral_task():
    print("BLE 주변 장치(Peripheral) 시작 중...")
    
    # 서비스 및 특성 생성
    # read=True: 중앙 장치가 이 특성의 값을 읽을 수 있도록 허용
    # notify=True: 값이 변경될 때 중앙 장치에 알림을 보낼 수 있도록 허용
    service = aioble.Service(_SERVICE_UUID)
    characteristic = aioble.Characteristic(
        service, _CHARACTERISTIC_UUID, read=True, notify=True
    )
    aioble.register_services(service)
    
    while True:
        print(f"'{_DEVICE_NAME}'으로 Advertising 시작...")
        # 연결을 기다리며 Advertising 시작
        # interval_us: Advertising 간격 (마이크로초)
        async with await aioble.advertise(
            250000,
            name=_DEVICE_NAME,
            services=[_SERVICE_UUID],
        ) as connection:
            print(f"연결 성공: {connection.device}")
            
            while connection.is_connected():
                # X축 아날로그 값 읽기 (0-65535 범위의 16-bit 값)
                adc_value = joy_x.read_u16()
                
                # 정수 값을 2바이트 데이터로 패킹 (little-endian, unsigned short)
                # BLE는 바이트 스트림으로 통신하므로, 정수를 바이트로 변환해야 합니다.
                packed_data = struct.pack("<H", adc_value)
                
                # 특성 값 쓰기 및 클라이언트에 알림(notify)
                characteristic.write(packed_data)
                
                print(f"전송된 ADC 값: {adc_value}")
                
                # 0.1초 대기
                await asyncio.sleep_ms(100)
            
            print(f"연결 끊김: {connection.device}")

# 메인 함수 실행
async def main():
    await peripheral_task()

# 비동기 루프 실행
asyncio.run(main())
