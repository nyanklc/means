import serial

class SerialHandler:
    def __init__(self, PORT, BAUDRATE):
        self.PORT = PORT
        self.BAUDRATE = BAUDRATE
        self.ser = serial.Serial(self.PORT, self.BAUDRATE, timeout=1)
        self.ser.reset_input_buffer()
        self.last_received = None

    def sendMsg(self, msg):
        msg = str(msg) + "\n"
        self.ser.write(msg.encode())
        pass

    def getMsg(self):
        msg = self.ser.readline().decode('utf-8').rstrip()
        return msg
