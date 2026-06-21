import json
import os

# open JSON file
path = os.path.join(os.path.dirname(__file__), "protocol.json")
with open(path, "r") as file:
    protocol = json.load(file)

# create new header file
path = os.path.join(os.path.dirname(__file__), "protocol_data.h")
with open(path, "w") as protocol_data_h:
    # write header file starter
    protocol_data_h.write("#ifndef INC_PROTOCOL_DATA_H_\n")
    protocol_data_h.write("#define INC_PROTOCOL_DATA_H_\n")
    protocol_data_h.write("\n")

    # write include statements
    protocol_data_h.write("#include \"main.h\"\n")
    protocol_data_h.write("\n")

    # write packet framing data
    protocol_data_h.write("#define START_BYTE " + protocol["framing"]["start_byte"] + "\n")
    protocol_data_h.write("#define MAX_ARG_SIZE " + protocol["framing"]["max_arg_size"] + "\n")
    protocol_data_h.write("\n")

    # write enum structure for command ids
    protocol_data_h.write("enum CommandID{\n")
    for cmd_name, cmd_data in protocol["commands"].items():
        protocol_data_h.write("\t" + cmd_name + " = " + str(cmd_data["id"]) + ",\n")
    protocol_data_h.write("};\n")
    protocol_data_h.write("\n")

    # write function for getting size of packets 
    protocol_data_h.write("uint16_t Protocol_GetPacketLength(uint8_t cmd_id);\n")
    protocol_data_h.write("\n")
    
    # write header file end
    protocol_data_h.write("#endif")

    pass

# create new source code fil
path = os.path.join(os.path.dirname(__file__), "protocol_data.c")
with open(path, "w") as protocol_data_c:
    # write include statements
    protocol_data_c.write("#include \"protocol_data.h\"\n")
    protocol_data_c.write("\n")

    # write function for getting size of packets
    protocol_data_c.write("uint16_t Protocol_GetPacketLength(uint8_t cmd_id){\n")
    protocol_data_c.write("\tswitch(cmd_id){\n")
    for cmd_name, cmd_data in protocol["commands"].items():
        protocol_data_c.write("\t\tcase " + cmd_name + ":\n")
        num_bytes = 3
        for arg in cmd_data["args"]:
            type_size = 0
            if(arg["type"] == "float"): type_size = 4
            elif(arg["type"] == "uint8_t"): type_size = 1
            num_bytes += (type_size * arg["count"])
        protocol_data_c.write("\t\t\treturn " + str(num_bytes)+ ";\n\n")
    protocol_data_c.write("\t}\n")
    protocol_data_c.write("\treturn 0;\n")
    protocol_data_c.write("}\n")
    protocol_data_c.write("\n")

    pass