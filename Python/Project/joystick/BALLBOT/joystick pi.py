# -*- coding: utf-8 -*-
import asyncio
import struct
from bleak import BleakClient, BleakScanner, uuids
# --- 수정된 부분 ---
# PhaseEnableMotor 외에 OutputDevice를 gpiozero에서 가져옵니다.
from gpiozero import PhaseEnableMotor, OutputDevice, AngularServo
from typing import Dict, Any

# --- 1. BLE 및 컨트롤러 설정 ---
PICO_ADDRESS = "2C:CF:67:C3:D4:D6"  # <<-- Pico W의 실제 주소를 입력하세요!

# Pico 코드와 동일한 UUID 사용
SERVICE_UUID = uuids.normalize_uuid_16(0x1848)
JOY_Y_CHAR_UUID = uuids.normalize_uuid_16(0x2A6E)  # Y축
JOY_X_CHAR_UUID = uuids.normalize_uuid_16(0x2A6F)  # X축
BUTTON_CHAR_UUID = uuids.normalize_uuid_16(0x2A70)  # 버튼 상태

# 조이스틱 값 범위 및 민감도 설정
JOY_CENTER = 32767.0
JOY_SCALE_DIVISOR = JOY_CENTER / 100.0
ACTION_THRESHOLD = 70

# 버튼 이름과 비트마스크 매핑
BUTTON_MAP = {
    "Joy_Btn": 0, "Btn_1": 1, "Btn_2": 2, "Btn_3": 3,
    "Btn_4": 4, "Btn_5": 5, "Btn_6": 6
}

# ======================================================================
# --- 2. 로봇 설정 (사용자 수정 영역) ---
# ======================================================================
ROBOT_CONFIG: Dict[str, Any] = {
    'pins': {
        # --- 수정된 부분 ---
        # 흡입 모터 핀 설정을 단순 ON/OFF 핀 번호로 변경
        'intake_motor_left_pin': 12,
        'intake_motor_right_pin': 13,
        
        # 주행 모터 및 서보 핀은 그대로 유지
        'drive_left':  {'dir': 5,  'brk': 6,  'pwm': 19},
        'drive_right': {'dir': 16, 'brk': 20, 'pwm': 18},
        'servo_left': 21,
        'servo_right': 22,
    },
    'drive_speeds': {
        'forward':  [50, 50],
        'backward': [-50, -50],
        'left':     [-30, 30],  # 제자리 좌회전 (왼쪽 후진, 오른쪽 전진)
        'right':    [30, -30],  # 제자리 우회전 (왼쪽 전진, 오른쪽 후진)
    },
    'modes': {
        # 흡입 모터 속도 설정은 더 이상 코드에서 사용되지 않지만,
        # 모드 구분을 위해 남겨둡니다.
        'tennis':   {'intake_speed': 35, 'servo_angle': 90},
        'baseball': {'intake_speed': 30, 'servo_angle': 45},
        'pingpong': {'intake_speed': 10, 'servo_angle': 30},
    },
    'servo_angles': {
        'default': 90, # 기본 서보 각도 (흡입이 아닐 때)
        'center': 90,  # 서보의 중앙 기준 각도
    },
    'motor_inversion': {
        'drive_left': False,  # 왼쪽 주행 모터는 방향을 그대로 사용
        'drive_right': True,  # 오른쪽 주행 모터는 방향을 반전시킴
        # 흡입 모터는 이제 방향 제어가 없으므로 이 설정은 무시됩니다.
    },
    'default_mode': 'tennis', # 프로그램 시작 시 기본 모드
}

# ======================================================================
# --- 3. 로봇 클래스 정의 ---
# ======================================================================
class Robot:
    """로봇 하드웨어 제어를 담당하는 클래스."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        pins = self.config['pins']
        angles = self.config['servo_angles']

        # 주행 모터 초기화 (기존과 동일)
        self.drive_left = PhaseEnableMotor(phase=pins['drive_left']['dir'], enable=pins['drive_left']['pwm'])
        self.drive_brake_left = OutputDevice(pins['drive_left']['brk'], initial_value=True)
        self.drive_right = PhaseEnableMotor(phase=pins['drive_right']['dir'], enable=pins['drive_right']['pwm'])
        self.drive_brake_right = OutputDevice(pins['drive_right']['brk'], initial_value=True)

        # --- 수정된 부분 ---
        # 흡입 모터를 단순 ON/OFF 제어를 위한 OutputDevice로 초기화합니다.
        self.intake_motor_left = OutputDevice(pins['intake_motor_left_pin'])
        self.intake_motor_right = OutputDevice(pins['intake_motor_right_pin'])

        # 서보 모터 초기화 (기존과 동일)
        self.servo_left = AngularServo(pins['servo_left'], min_angle=0, max_angle=180, initial_angle=angles['default'])
        self.servo_right = AngularServo(pins['servo_right'], min_angle=0, max_angle=180, initial_angle=angles['default'])

        print("✅ 로봇이 성공적으로 초기화되었습니다.")

    def _set_motor_speed(self, motor: PhaseEnableMotor, speed: float):
        """-100 ~ 100 범위의 속도 값으로 모터를 제어합니다."""
        normalized_speed = max(min(speed / 100.0, 1.0), -1.0)
        motor.value = normalized_speed

    def move(self, left_speed: int, right_speed: int):
        """좌우 주행 모터의 속도를 설정값에 따라 방향을 조절하여 설정합니다."""
        if self.config['motor_inversion']['drive_left']:
            left_speed *= -1
        if self.config['motor_inversion']['drive_right']:
            right_speed *= -1
        self._set_drive_brakes(False)
        self._set_motor_speed(self.drive_left, left_speed)
        self._set_motor_speed(self.drive_right, right_speed)

    def stop_drive(self):
        """주행 모터를 정지하고 브레이크를 겁니다."""
        self.drive_left.stop()
        self.drive_right.stop()
        self._set_drive_brakes(True)

    # --- 수정된 부분 ---
    def start_intake(self, mode_name: str):
        """흡입 모터를 켜고, 지정된 모드로 서보를 작동시킵니다."""
        mode_settings = self.config['modes'].get(mode_name)
        if not mode_settings:
            print(f"⚠️ 경고: '{mode_name}' 모드를 찾을 수 없습니다.")
            return

        print(f"💨 흡입 모터 작동 (모드: {mode_name})")
        # .on() 메서드로 GPIO 핀에 1(HIGH) 신호를 보냅니다.
        self.intake_motor_left.on()
        self.intake_motor_right.on()

        # 서보 각도 설정 로직은 그대로 유지
        angle = mode_settings['servo_angle']
        center_angle = self.config['servo_angles']['center']
        self.servo_left.angle = center_angle - angle
        self.servo_right.angle = center_angle + angle
        print(f"📐 서보 각도 설정: 좌 {self.servo_left.angle}°, 우 {self.servo_right.angle}°")

    # --- 수정된 부분 ---
    def stop_intake(self):
        """흡입 모터를 끄고 서보를 기본 위치로 되돌립니다."""
        print("🛑 흡입 정지")
        # .off() 메서드로 GPIO 핀에 0(LOW) 신호를 보냅니다.
        self.intake_motor_left.off()
        self.intake_motor_right.off()
        self.reset_servos()

    def reset_servos(self):
        """서보를 기본 각도로 설정합니다."""
        default_angle = self.config['servo_angles']['default']
        self.servo_left.angle = default_angle
        self.servo_right.angle = default_angle

    def _set_drive_brakes(self, active: bool):
        """주행 모터 브레이크를 켜거나 끕니다."""
        self.drive_brake_left.value = active
        self.drive_brake_right.value = active

    def shutdown(self):
        """모든 모터를 정지하고 리소스를 정리합니다."""
        print("셧다운: 모든 모터 정지 및 리소스 정리")
        self.stop_drive()
        self.stop_intake()

# ======================================================================
# --- 4. 메인 제어 로직 (이하 부분은 수정 없음) ---
# ======================================================================

def is_button_pressed(button_mask: int, button_name: str) -> bool:
    """버튼 마스크에서 특정 버튼이 눌렸는지 확인합니다."""
    return bool(button_mask & (1 << BUTTON_MAP[button_name]))

def _handle_buttons(robot: Robot, state: Dict[str, Any], button_mask: int):
    """버튼 입력을 처리하여 모드를 변경하거나 흡입을 토글합니다."""
    last_mask = state['last_button_mask']
    if button_mask == last_mask:
        return

    new_mode = state['current_mode']
    if is_button_pressed(button_mask, "Btn_1"): new_mode = 'tennis'
    elif is_button_pressed(button_mask, "Btn_2"): new_mode = 'baseball'
    elif is_button_pressed(button_mask, "Btn_3"): new_mode = 'pingpong'

    if new_mode != state['current_mode']:
        state['current_mode'] = new_mode
        print(f"\n🔄 모드 변경 -> {new_mode.upper()}")
        if state['intake_on']:
            robot.start_intake(new_mode)

    if not is_button_pressed(button_mask, "Joy_Btn") and is_button_pressed(last_mask, "Joy_Btn"):
        state['intake_on'] = not state['intake_on']
        if state['intake_on']:
            robot.start_intake(state['current_mode'])
        else:
            robot.stop_intake()

    state['last_button_mask'] = button_mask

def _handle_joystick(robot: Robot, state: Dict[str, Any], x_val: int, y_val: int):
    """조이스틱 입력을 처리하여 로봇의 움직임을 결정합니다."""
    y_scaled = (y_val - JOY_CENTER) / JOY_SCALE_DIVISOR
    x_scaled = (x_val - JOY_CENTER) / JOY_SCALE_DIVISOR
    
    current_action = "stop"
    if abs(y_scaled) > abs(x_scaled):
        if y_scaled > ACTION_THRESHOLD: current_action = "right"
        elif y_scaled < -ACTION_THRESHOLD: current_action = "left"
    else:
        if x_scaled > ACTION_THRESHOLD: current_action = "forward"
        elif x_scaled < -ACTION_THRESHOLD: current_action = "backward"

    if current_action != state['last_action']:
        speeds = robot.config['drive_speeds']
        action_map = {
            "forward":  ("전진", speeds['forward']),
            "backward": ("후진", speeds['backward']),
            "right":    ("우회전", speeds['right']),
            "left":     ("좌회전", speeds['left']),
        }
        
        if current_action in action_map:
            action_name, speed_pair = action_map[current_action]
            print(f"\n🤖 로봇 동작: {action_name}")
            robot.move(speed_pair[0], speed_pair[1])
        else:
            print("\n🤖 로봇 동작: 정지")
            robot.stop_drive()
        
        state['last_action'] = current_action

async def main():
    """메인 비동기 함수. BLE 스캔, 연결 및 제어 루프를 실행합니다."""
    robot = Robot(ROBOT_CONFIG)
    
    state = {
        'current_mode': ROBOT_CONFIG['default_mode'],
        'intake_on': False,
        'last_button_mask': 0,
        'last_action': "stop",
    }
    
    print(f"🔍 '{PICO_ADDRESS}' 주소의 Pico를 스캔합니다...")
    device = await BleakScanner.find_device_by_address(PICO_ADDRESS, timeout=20.0)
    if not device:
        print("❌ Pico를 찾을 수 없습니다. 주소를 확인하거나 Pico가 켜져 있는지 확인하세요.")
        return

    print("🔌 Pico에 연결 중...")
    try:
        async with BleakClient(device) as client:
            print(f"✅ 연결 성공: {device.name} ({device.address})")
            print(f"🎾 현재 모드: {state['current_mode'].upper()}")

            while client.is_connected:
                raw_y, raw_x, raw_buttons = await asyncio.gather(
                    client.read_gatt_char(JOY_Y_CHAR_UUID),
                    client.read_gatt_char(JOY_X_CHAR_UUID),
                    client.read_gatt_char(BUTTON_CHAR_UUID)
                )
                
                y_val = struct.unpack("<H", raw_y)[0]
                x_val = struct.unpack("<H", raw_x)[0]
                button_mask = struct.unpack("<B", raw_buttons)[0]
                
                _handle_buttons(robot, state, button_mask)
                _handle_joystick(robot, state, x_val, y_val)
                
                await asyncio.sleep(0.05)

    except Exception as e:
        print(f"\n🚨 오류 발생: {e}")
    finally:
        print("\n👋 연결이 끊겼거나 프로그램이 종료됩니다.")
        robot.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🚫 사용자에 의해 프로그램이 중단되었습니다.")
