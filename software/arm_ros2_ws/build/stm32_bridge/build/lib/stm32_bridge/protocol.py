import json
from .serial_com import SerialCom

class Protocol:

    def __init__(self):
        self.protocol = json.load(protocol.json)
        self.serial = SerialCom()
        pass

    def read_packet(self):

        # check for starte byte
        current_byte = self.serial.read_byte()
        if(current_byte != bytes([int(self.protocol["framing"]["start_byte"], 16)])):
            return None

        # initialize packet
        packet = [0xAA]

        # get command
        current_byte = self.serial.read_byte()
        packet.append(current_byte)

        # determine length of packet
        cmd_length = self.get_command_length(current_byte)

        # get the rest of the packet
        for _ in range(cmd_length - 2):
            packet.append(self.serial.read_byte())

        # verify checksum
        checksum = get_checksum(packet)
        if(checksum != packet[len(packet)-1]):
            return -1

        return packet

    def parse_packet(self, packet):

        # get command JSON data
        command = self.get_command_data(packet[len(packet)-1])

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
        return num_bytes

    # calculates checksum from raw packet bytes (does not include first and last bytes)
    def get_checksum(self, bytes):
        return sum(bytes[1:len(bytes)-1]) % 0xFF

    # gets JSON data for command with id: cmd_id
    def get_command_data(self, cmd_id):
        for cmd in self.protocol["commands"].items():
            if(cmd_id == self.protocol["commands"][cmd]["id"]):
                return self.protocol["commands"][cmd]
        return None

    pass



















