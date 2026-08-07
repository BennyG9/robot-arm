function R = forward_kinematics(q, robot)
    z0 = robot.L1;
    R0 = [0; 0; z0];

    r = robot.L2*sin(q(2));
    x1 = r*sin(q(1));
    y1 = r*cos(q(1));
    z1 = robot.L1 + robot.L2*cos(q(2));
    R1 = [x1 ;y1; z1];

    x2 = x1 + robot.l3*cos(q(1));
    y2 = y1 - robot.l3*sin(q(1));
    z2 = z1;
    R2 = [x2; y2; z2];

    r = r + robot.L3*sin(q(2)-q(3));
    x3 = r*sin(q(1)) + robot.l3*cos(q(1));
    y3 = r*cos(q(1)) - robot.l3*sin(q(1));
    z3 = robot.L1 + robot.L2*cos(q(2)) + robot.L3*cos(q(2)-q(3));
    R3 = [x3; y3; z3];

    R = [R0, R1, R2, R3];
end