import json
import os

# open JSON file
path = os.path.join(os.path.dirname(__file__), "protocol.json")
with open(path, "r") as file:
    protocol = json.load(file)

# keep track of all argument data types present, largest argument size, number of arguments
argument_types = ["None"]
max_arg_size = 0
num_arguments = []

# create new source code fil
path = os.path.join(os.path.dirname(__file__), "protocol_data.c")
with open(path, "w") as protocol_data_c:
    # write include statements
    protocol_data_c.write("#include \"protocol_data.h\"\n")
    protocol_data_c.write("\n")

    # write function for getting size of packets
    protocol_data_c.write("uint16_t Protocol_GetPacketLength(uint8_t cmd_id){\n")
    protocol_data_c.write("\tswitch((CommandID)cmd_id){\n")
    for cmd_name, cmd_data in protocol["commands"].items():
        protocol_data_c.write("\t\tcase " + cmd_name + ":\n")
        num_bytes = 3
        for arg in cmd_data["args"]:
            type_size = 0
            if(not(arg["type"] in argument_types)):
                argument_types.append(arg["type"])
            if(arg["type"] == "float"): type_size = 4
            elif(arg["type"] == "uint8_t"): type_size = 1
            num_bytes += (type_size * arg["count"])
        protocol_data_c.write("\t\t\treturn " + str(num_bytes)+ ";\n")
        if(num_bytes-3 > max_arg_size):
            max_arg_size = num_bytes-3
    protocol_data_c.write("\t}\n")
    protocol_data_c.write("\treturn 0;\n")
    protocol_data_c.write("}\n")
    protocol_data_c.write("\n")

    # write function for getting argument types
    protocol_data_c.write("HAL_StatusTypeDef Protocol_GetArgumentTypes(uint8_t cmd_id, Type* type_list){\n")
    protocol_data_c.write("\tswitch((CommandID)cmd_id){\n")
    for cmd_name, cmd_data in protocol["commands"].items():
        protocol_data_c.write("\t\tcase " + cmd_name + ":\n")
        i = 0
        if(len(cmd_data["args"]) == 0):
            protocol_data_c.write("\t\t\ttype_list[0] = NONE;\n")
        else:
            for arg in cmd_data["args"]:
                for _ in range(arg["count"]):
                    protocol_data_c.write("\t\t\ttype_list[" + str(i) + "] = " + arg["type"].upper() + ";\n")
                    i += 1
        num_arguments.append(i)
        protocol_data_c.write("\t\t\treturn HAL_OK;\n")
    protocol_data_c.write("\t}\n")
    protocol_data_c.write("\treturn HAL_ERROR;\n")
    protocol_data_c.write("}\n")
    protocol_data_c.write("\n")

    # write function for getting the number of arguments
    protocol_data_c.write("uint16_t Protocol_GetNumArguments(uint8_t cmd_id){\n")
    protocol_data_c.write("\tswitch((CommandID)cmd_id){\n")
    i = 0
    for cmd_name, cmd_data in protocol["commands"].items():
        protocol_data_c.write("\t\tcase " + cmd_name + ":\n")
        protocol_data_c.write("\t\t\treturn " + str(num_arguments[i]) + ";\n")
        i += 1
    protocol_data_c.write("\t}\n")
    protocol_data_c.write("\treturn 0;\n")
    protocol_data_c.write("}\n")
    protocol_data_c.write("\n")

    pass

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
    protocol_data_h.write("#define MAX_ARG_SIZE " + str(max_arg_size) + "\n")
    protocol_data_h.write("\n")

    # write enum structure for command ids
    protocol_data_h.write("typedef enum{\n")
    for cmd_name, cmd_data in protocol["commands"].items():
        protocol_data_h.write("\t" + cmd_name + " = " + str(cmd_data["id"]) + ",\n")
    protocol_data_h.write("} CommandID;\n")
    protocol_data_h.write("\n")

    # write enum structure for variable types
    protocol_data_h.write("typedef enum{\n")
    for type in argument_types:
        protocol_data_h.write("\t" + type.upper() + ",\n")
    protocol_data_h.write("} Type;\n")
    protocol_data_h.write("\n")

    # write function for getting size of packets 
    protocol_data_h.write("uint16_t Protocol_GetPacketLength(uint8_t cmd_id);\n")
    protocol_data_h.write("\n")

    # write function for getting argument types 
    protocol_data_h.write("HAL_StatusTypeDef Protocol_GetArgumentTypes(uint8_t cmd_id, Type* type_list);\n")
    protocol_data_h.write("\n")

    # write function for getting the number of arguments
    protocol_data_h.write("uint16_t Protocol_GetNumArguments(uint8_t cmd_id);\n")
    protocol_data_h.write("\n")

    # write header file end
    protocol_data_h.write("#endif")

    pass