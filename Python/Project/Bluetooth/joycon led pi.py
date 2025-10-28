import asyncio
import struct
from bleak import BleakClient, BleakScanner
from gpiozero import PWMLED
from signal import pause

# --- 설정 변수 ---
# Pico W의 MAC 주소를 여기에 입력하세요.
PICO_ADDRESS = "2C:CF:67:C3:D4:D6"  # <<-- 여기에 Pico W의 실제 주소를 입력하세요!

# Pico W 코드와 동일한 UUID를 사용해야 합니다.
SERVICE_UUID = "00001848-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"

# LED를 연결한 GPIO 핀 번호 (BCM 모드 기준)
LED_PIN = 18
# --- 설정 끝 ---

# gpiozero를 사용하여 PWMLED 객체 생성
# gpiozero는 종료 시 자동으로 리소스를 정리합니다.
led = PWMLED(LED_PIN)

async def main():
    print(f"'{PICO_ADDRESS}' 주소를 가진 Pico W를 스캔합니다...")
    
    device = await BleakScanner.find_device_by_address(PICO_ADDRESS, timeout=20.0)
    if not device:
        print(f"Pico W를 찾을 수 없습니다. Advertising 중인지 확인하세요.")
        return

    print(f"Pico W에 연결 중...")
    
    try:
        async with BleakClient(device) as client:
            if client.is_connected:
                print(f"연결 성공: {device.name} ({device.address})")
            else:
                print("연결 실패.")
                return

            while client.is_connected:
                # Pico W로부터 특성 값 읽기 (2바이트 데이터)
                raw_data = await client.read_gatt_char(CHARACTERISTIC_UUID)
                
                # 2바이트 데이터를 정수(0-65535)로 언패킹
                adc_value = struct.unpack("<H", raw_data)[0]
                
                # ADC 값(0-65535)을 LED 밝기 값(0.0-1.0)으로 변환
                # gpiozero의 PWMLED.value는 0.0(꺼짐)에서 1.0(최대 밝기) 사이의 값을 사용합니다.
                led_brightness = adc_value / 65535.0
                
                # LED 밝기 설정
                led.value = led_brightness
                
                print(f"수신 값: {adc_value}, LED 밝기: {led.value:.2f}")
                
                # 0.1초 대기
                await asyncio.sleep(0.1)

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        print("연결이 끊겼거나 프로그램이 종료됩니다.")
        led.off() # LED 끄기

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("사용자에 의해 프로그램이 중단되었습니다.")

