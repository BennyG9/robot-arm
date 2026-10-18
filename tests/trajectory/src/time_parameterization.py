import numpy as np

# get maximum allowable time parameterization constant
def min_path_time_const(Q, robot):
    DQ = np.diff(Q)
    dQdt_max = np.array([robot["base_joint_max_speed"], robot["shoulder_joint_max_speed"], robot["elbow_joint_max_speed"]])

    dT = np.abs(DQ / dQdt_max[:, np.newaxis, np.newaxis])

    dt_const = np.max(dT)
    return dt_const

# get largerst allowable time parameterization function
def min_path_time_func(Q, robot):
    DQ = np.diff(Q)
    dQdt_max = np.array([robot["base_joint_max_speed"], robot["shoulder_joint_max_speed"], robot["elbow_joint_max_speed"]])

    #print(Q.shape)
    #print(DQ)

    dT = np.abs(DQ / dQdt_max[:, np.newaxis, np.newaxis])

    dt_func = np.max(dT, axis=(0,1)).tolist()
    return dt_func

# verify that time parameterization constant/function results in trajectory within speed interval 
def verify_time_func(Q, dt, robot):
    dT = np.ones((1, Q.shape[1]))
    if(np.isscalar(dt)):
        dT = dt * dT
    else:
        dT = dt

    DQ = np.diff(Q)
    dQdt = DQ / dT
    dQdt_max = np.array([robot["base_joint_max_speed"], robot["shoulder_joint_max_speed"], robot["elbow_joint_max_speed"]])

    speed_ratio = np.abs(dQdt / dQdt_max[:, np.newaxis])

    epsilon = 0.00001
    valid = np.all(speed_ratio < (1+epsilon))
    return valid 