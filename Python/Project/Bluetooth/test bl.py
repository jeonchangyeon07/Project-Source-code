import serial

BlSerial = serial.Serial("/dev/ttyAMA10", baudrate=9600, timeout=1.0)

try:
    while True:
        sendData = "nice to meet you! \r\n"
        BlSerial.write(sendData.encode())
        data = BlSerial.readline()
        data = data.decode()
        print(data)
except KeyboardInterrupt:
    pass

BlSerial.close()