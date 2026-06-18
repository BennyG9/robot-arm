import serial

class SerialCom:

    def __init__(self, port="ttyACM0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=0.01)
        pass

    def write(self, msg):
        self.ser.write(msg.encode("utf-8"))
        pass

    def read_line(self):
        try:
            if(self.ser.in_waiting > 0):
                return self.ser.readline().decode("utf-8").strip()
            except:
                return None
        return None
