import xml.etree.ElementTree as ET
from pathlib import Path
import xacro

def parse_kinematics_parameters(urdf_path):

    urdf_path = Path(urdf_path)

    if(not urdf_path.exists()):
        raise FileNotFoundError(f"URDF file not found: {urdf_path}")

    #tree = ET.parse(urdf_path)
    #root = tree.getroot()
    #parameters = root.find("kinematic_parameters")

    xml_string = xacro.process(urdf_path)
    root = ET.fromstring(xml_string)
    parameters = root.find("kinematic_parameters")

    if(parameters is None):
        raise ValueError("Could not find <kinematics_parameters> in URDF")

    extracted = {}
    for name, value in parameters.attrib.items():
        extracted[name] = float(value)

    return extracted
