def validate_angles(q, robot):
    phi = q[0]
    theta1 = q[1]
    theta2 = q[2]

    base = (phi >= robot.base_joint_min) and (phi <= robot.base_joint_max)
    shoulder = (theta1 >= robot.shoulder_joint_min) and (theta1 <= robot.shoulder_joint_max)
    elbow = (theta2 >= robot.elbow_joint_min) and (theta2 <= robot.elbow_joint_max)

    return base and shoulder and elbow