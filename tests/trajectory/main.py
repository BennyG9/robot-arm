from src.time_parameterization import *
from src.path_to_angles import *
from src.forward_kinematics import *
from src.generate_path import *
from src.inverse_kinematics import *
from src.validation import *

import numpy as np

robot = {
    "base_height": 0.055,
    "L1": 0.07166,
    "L2": 0.14074976,
    "L3": 0.08187597,

    "base_joint_min": -1.5707963267948966,
    "base_joint_max": 1.3962634015954636,
    "base_joint_max_speed": 2.0943951023931953,

    "shoulder_joint_min": -1.5707963267948966,
    "shoulder_joint_max": 1.361356816555577,
    "shoulder_joint_max_speed": 2.8902652413026098,

    "elbow_joint_min": -2.6179938779914944,
    "elbow_joint_max": 2.076941809873252,
    "elbow_joint_offset": 0.04,
    "elbow_joint_max_speed": 1.2566370614359172
}


starting_angles = (np.array([-70, 70, -100]))
ending_angles =   (np.array([ 45, 30,  -60]))

pos1 = forward_kinematics(starting_angles, robot)[5][:3,3]
pos2 = forward_kinematics(ending_angles, robot)[5][:3,3]

path = linear_path(pos1, pos2, 200)
Q = path_to_angles(path, robot)

path_index = None
for i in range(4):
    if(np.allclose(Q[i, :, 0], np.radians(starting_angles))):
        path_index = i
        break
if(path_index == None):
    raise Exception("No Path Index Found...")
path_angles = Q[:][path_index][:]

time_param_func = min_path_time_const(path_angles, robot)
time_param_validity = verify_time_func(path_angles, time_param_func, robot)
time_param_len = 0

trajectory_length = path_angles.shape[1]

print(f"Trajectory Length: {trajectory_length}")
print("\n\nAngles: ")
print(path_angles)
print(f"\n\nTime Parameterization Length: {time_param_len}")
print(f"Time Parameterization Validity: {time_param_validity}")
print("Time Parameterization: ")
print(time_param_func)