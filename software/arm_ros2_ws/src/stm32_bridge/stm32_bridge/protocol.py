import json
import os

from .serial_com import SerialCom

class Protocol:

    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "protocol.json")
        with open(path, "r") as file:
            self.protocol = json.load(file)

        self.commands_id = {}
        self.commands_name = {}
        for name, data in self.protocol["commands"].items():
            self.commands_name[name] = data
            self.commands_id[data["id"]] = data

        self.serial = SerialCom(port="/dev/ttyACM0")
        pass

    def read_packet(self):

        # check for starte byte
        current_byte = self.serial.read_byte()
        if(current_byte != bytes([int(self.protocol["framing"]["start_byte"], 16)])):
            return None

        # initialize packet
        packet = [current_byte]

        # get command
        current_byte = self.serial.read_byte()
        packet.append(current_byte)

        # determine length of packet
        cmd_length = self.get_command_length(current_byte)

        # get the rest of the packet
        for _ in range(cmd_length - 2):
            packet.append(self.serial.read_byte())

        print(packet)

        # verify checksum
        checksum = self.get_checksum(packet)
        if(checksum != packet[len(packet)-1][0]):
            return -1

        return packet

    def parse_packet(self, packet):

        # get command JSON data
        command = self.get_command_data(packet[1])

        # parse arguments
        args = []
        i = 2
        for arg in command["args"]:
            args.append([])
            arg_type = arg["type"]
            for _ in range(arg["count"]):
                if(arg_type == "uint8_t"):
                    args[len(args)-1].append(packet[i])
                    i += 1
                elif(arg_type == "float"):
                    args[len(args)-1].append(self.parse_float(packet[i:i+4]))
                    i += 4

        return command["name"], args

    def get_direction(self, command_name : str):
        return self.commands_name[command_name]["direction"]

#******************#
# HELPER FUNCTIONS #
#******************#

    # returns the total command packet length in # of bytes
    def get_command_length(self, cmd_id):
        #for cmd in self.protocol["commands"].items():
        #    if(cmd_id == self.protocol["commands"][cmd]["id"]):
        #        num_bytes = 0
        #        for arg in self.protocol["commands"][cmd]["args"]:
        #            type_size = 0
        #            if(arg["type"] == "float"): type_size = 4
        #            elif(arg["type"] == "uint8_t"): type_size = 1
        #            num_bytes += (type_size * arg["count"])
        #        return num_bytes + 3
        #return 0

        cmd = self.get_command_data(cmd_id)
        if(cmd == None): return 0
        num_bytes = 0
        for arg in cmd["args"]:
            type_size = 0
            if(arg["type"] == "float"): type_size = 4
            elif(arg["type"] == "uint8_t"): type_size = 1
            num_bytes += (type_size * arg["count"])
        return num_bytes + 3

    # calculates checksum from raw packet bytes (does not include first and last bytes)
    def get_checksum(self, byte_list):
        return sum(b[0] for b in byte_list[1:len(byte_list)-1]) % 0xFF

    # gets JSON data for command with id: cmd_id
    def get_command_data(self, cmd_id):
        return self.commands_id[int.from_bytes(cmd_id, byteorder="little")]

    # parses float data type from bytes
    def parse_float(self, bytes_list):
        raw_bytes = bytes(bytes_list)
        value = struct.unpack('<f', raw_bytes[0])
        return value

    pass



















