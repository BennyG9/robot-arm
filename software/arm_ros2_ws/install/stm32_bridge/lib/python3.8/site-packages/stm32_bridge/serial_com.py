import serial

class SerialCom:

    def __init__(self, port="ttyACM0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=0.01)
        pass

    def available(self):
        return self.ser.in_waiting

    def clear(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        pass

    def write_bytes(self, bytes):
        self.ser.write(bytes)
        pass

    def read_line(self):
        try:
            if(self.ser.in_waiting > 0):
                return self.ser.readline().decode("utf-8").strip()
        except:
                return None
        return None

    def read_byte(self):
        try:
            if(self.ser.in_waiting > 0):
                return self.ser.read(1)
        except:
            return None
        return None

    pass
