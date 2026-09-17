import math
import numpy as np

def forward_kinematics(q):

    transformations = get_transformation_matrices(q)

    frames = transformations
    for i in range(1, len(frames)):
        frames[i] = frames[i-1] @ frames[i]
        pass

    return frames


def get_transformation_matrices(q):
    phi = q[0]
    theta1 = q[1]
    theta2 = q[2]

    # Ground - ground transform
    T0 = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    # Ground - top of base transform    rotz(-phi)
    T01 = np.array([[math.cos(-phi), -math.sin(-phi), 0, 0],
                    [math.sin(-phi), math.cos(-phi), 0, 0],
                    [0, 0, 0, base_height],
                    [0, 0, 0, 1]])

    # Top of base - shoulder transform  rotx(-theta1)
    T12 = np.array([[1, 0, 0, 0],
                    [0, math.cos(-theta1), -math.sin(-theta1), 0],
                    [0, math.sin(-theta1), math.cos(-theta1), L1],
                    [0, 0, 0, 1]])

    # Shoulder - elbow1 transform   roty(pi/2)
    T23 = np.array([[0, 0, 1, 0],
                    [0, 1, 0, 0],
                    [-1, 0, 0, L2],
                    [0, 0, 0, 1]])

    # Elbow1 - elbow2 transform     roty(-pi/2) * rotx(theta2)
    T34 = np.array([[0, -math.sin(theta2), -math.cos(theta2), 0],
                    [0, math.cos(theta2), -math.sin(theta2), 0],
                    [1, 0, 0, l3],
                    [0, 0, 0, 1]])

    # Elbow2 - end effector transform
    T45 = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, L3],
                    [0, 0, 0, 1]])

    return [T0, T01, T12, T23, T34, T45]