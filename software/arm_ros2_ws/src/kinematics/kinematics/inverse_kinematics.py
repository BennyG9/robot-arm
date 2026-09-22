import math

epsilon = 1 * 10**(-14)

def inverse_kinematics(R, robot):
    x = R(0)
    y = R(1)
    z = R(2)

    # calculate and verify horizontal radius
    r2 = (x**2 + y**2 - robot.l3**2)
    if(r2 < 0):
        return False, [0,0,0]
    r = math.sqrt(r2)

    # calculate both base angles
    phi = math.atan2(x, y) - math.atan2(robot.l3, r)
    if(phi < -math.pi):
        phi += 2*math.pi
    elif(phi > math.pi):
        phi -= 2*math.pi
    phi2 = math.atan2(x, y) + math.atan2(robot.l3, r) - math.pi;
    if(phi2 < -math.pi):
        phi2 += 2*math.pi
    elif(phi2 > math.pi):
        phi2 -= 2*math.pi

    # calculate and verify theta2
    D2 = r2  + (z - (robot.L1 + robot.base_height))**2;
    if(D2 < epsilon):
        return False, [0,0,0]
    C2 = (D2 - robot.L2**2 - robot.L3**2) / (2 * robot.L2 * robot.L3);
    if(math.abs(C2) > 1):
        return False, [0,0,0]
    C2 = max(-1, min(1, C2))
    theta2 = math.acos(C2)

    # calculate alpha and beta for theta1 configurations (elbow up / elbow down)
    alpha = math.atan2(r, z - (robot.L1 + robot.base_height));
    C1 = (robot.L2**2 + D2 - robot.L3**2) / (2 * robot.L2 * math.sqrt(D2))
    if(abs(C1) > 1):
        return False, [0,0,0]
    C1 = max(-1, min(1, C1))
    beta = math.acos(C1)

    # all positionally accurate configurations 
    Q = [
        [phi, alpha-beta, -theta2],
        [phi2, -alpha+beta, theta2],
        [phi, alpha+beta, theta2],
        [phi2, -alpha-beta, -theta2]
    ]

    # validity marker, configurations 
    return True, Q