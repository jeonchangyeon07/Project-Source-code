from rplidar import RPLidar
import time

PORT_NAME = '/dev/ttyUSB0'

lidar = RPLidar(PORT_NAME)

try:
    print("▶ 라이다 실시간 측정 시작! (종료: Thonny 중지 버튼 또는 Ctrl+C)")
    
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            print(f'각도: {angle:.1f}°, 거리: {distance:.1f} mm')
        
        time.sleep(0.05)  # 출력 너무 빠른 경우 조절용

except KeyboardInterrupt:
    print("\n▶ 측정 중단됨 (Ctrl+C 입력)")

finally:
    print("▶ 라이다 종료 중...")
    lidar.stop()
    lidar.disconnect()