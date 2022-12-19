import serial

class SerialHandler:
    def __init__(self, PORT, BAUDRATE):
        self.PORT = PORT
        self.BAUDRATE = BAUDRATE
        self.ser = serial.Serial(self.PORT, self.BAUDRATE, timeout=1)
        self.ser.reset_input_buffer()
        self.last_received = None

    def sendMsg(self, msg):
        pure_msg = str(msg)
        msg = pure_msg + "\n"
        self.ser.write(msg.encode())
        print("sent: " + pure_msg)
        return

    def getMsg(self):
        msg = self.ser.readline().decode('utf-8').rstrip()
        return msg
