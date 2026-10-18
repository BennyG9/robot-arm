import numpy as np

from src.inverse_kinematics import inverse_kinematics
from src.validation import validate_angles

# convert cartesian path to joint space
def path_to_angles(path, robot):

    all_angles = np.zeros((4,3,len(path[0])))
    path_index = -1

    last_valid_angles = np.zeros((4,3))
    for pos in path.T:
        path_index += 1

        valid, angles = inverse_kinematics(pos, robot)

        # unable to calculate valid angles
        if(not valid):
            all_angles[:3, :4, path_index] = np.zeros((4,3))
            continue

        # first point in path
        if(path_index == 0):
            all_angles[:4, :3, 0] = angles
            last_valid_angles[:4, :3] = angles
            continue

        # insert rest of angles based on continuity 
        for i in range(4):

            min_norm = np.inf

            for q in angles:         # ??

                current_norm = 0                

                if(np.all(all_angles[i, :3, path_index-1] == 0)):
                    current_norm = np.linalg.norm(q - last_valid_angles[i, :3])
                else:
                    current_norm = np.linalg.norm(q - all_angles[i, :3, path_index-1])

                if(current_norm < min_norm):
                    min_norm = current_norm
                    all_angles[i, :3, path_index] = q[:]
                pass

            last_valid_angles[:][:] = angles

            pass
        pass

    Q = all_angles
                
    # replace sequences of invalid angles 
    for k in range(4):

        last_nonzero_angles = np.zeros(3)
        last_nonzero_index = 0
        invalid_angles = 0

        for i in range(Q.shape[2]):

            qki = Q[k, :, i]

            if(np.all(qki == 0)):
                invalid_angles += 1
                continue

            valid = validate_angles(qki, robot)
            if(not valid):
                invalid_angles += 1
                Q[k, :, i] = clamp_angles(qki, robot)

            if(last_nonzero_index != 0 and last_nonzero_index != i-1):
                current_angles = Q[k, :, i]
                Q[k, :, last_nonzero_index:i] = np.array[
                    np.linspace(last_valid_angles[0], current_angles[0], (i-last_nonzero_index), endpoint=False),
                    np.linspace(last_valid_angles[0], current_angles[0], (i-last_nonzero_index), endpoint=False),
                    np.linspace(last_valid_angles[0], current_angles[0], (i-last_nonzero_index), endpoint=False)
                ]
                pass

            
            last_nonzero_angles[:] = Q[k, :, i]
            last_nonzero_index = i
            pass
        pass
    
    return Q


# clamp angles to within robot hardware allowable range
def clamp_angles(q, robot):
    joints = ["base", "shoulder", "elbow"]
    angles = q
    for i in range(len(joints)):
        if(q[i] < robot[joints[i] + "_joint_min"]):
            angles[i] = robot[joints[i] + "_joint_min"]
        elif(q[i] > robot[joints[i] + "_joint_max"]):
            angles[i] = robot[joints[i] + "_joint_max"]
    return angles