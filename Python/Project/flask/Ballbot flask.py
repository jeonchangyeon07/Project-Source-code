from flask import Flask, render_template, request
import RPi.GPIO as GPIO

app = Flask(__name__)

DIR1_PIN = 23
BRK1_PIN = 24
PWM1_PIN = 12

DIR2_PIN = 17
BRK2_PIN = 27
PWM2_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(DIR1_PIN, GPIO.OUT)
GPIO.setup(BRK1_PIN, GPIO.OUT)
GPIO.setup(PWM1_PIN, GPIO.OUT)

GPIO.setup(DIR2_PIN, GPIO.OUT)
GPIO.setup(BRK2_PIN, GPIO.OUT)
GPIO.setup(PWM2_PIN, GPIO.OUT)

pwm1 = GPIO.PWM(PWM1_PIN, 1000)
pwm2 = GPIO.PWM(PWM2_PIN, 1000)
pwm1.start(0)
pwm2.start(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    cmd = request.form['cmd']

    if cmd == 'T':
        GPIO.output(DIR1_PIN, GPIO.HIGH)
        GPIO.output(BRK1_PIN, GPIO.LOW)
        pwm1.ChangeDutyCycle(20)

        GPIO.output(DIR2_PIN, GPIO.LOW)
        GPIO.output(BRK2_PIN, GPIO.LOW)
        pwm2.ChangeDutyCycle(20)

    elif cmd == 'B':
        GPIO.output(DIR1_PIN, GPIO.HIGH)
        GPIO.output(BRK1_PIN, GPIO.LOW)
        pwm1.ChangeDutyCycle(25)

        GPIO.output(DIR2_PIN, GPIO.LOW)
        GPIO.output(BRK2_PIN, GPIO.LOW)
        pwm2.ChangeDutyCycle(25)

    elif cmd == 'P':
        GPIO.output(DIR1_PIN, GPIO.HIGH)
        GPIO.output(BRK1_PIN, GPIO.LOW)
        pwm1.ChangeDutyCycle(10)

        GPIO.output(DIR2_PIN, GPIO.LOW)
        GPIO.output(BRK2_PIN, GPIO.LOW)
        pwm2.ChangeDutyCycle(10)

    elif cmd == 'S':
        GPIO.output(BRK1_PIN, GPIO.HIGH)
        pwm1.ChangeDutyCycle(0)

        GPIO.output(BRK2_PIN, GPIO.HIGH)
        pwm2.ChangeDutyCycle(0)

    return '', 204

@app.route('/shutdown', methods=['POST'])
def shutdown():
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    return 'GPIO cleaned up', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)