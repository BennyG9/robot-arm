function q = inverse_kinematics(position, robot)
    
    x = position(1);
    y = position(2);
    z = position(3);

    r = sqrt(x^2 + y^2 - robot.l3^2);

    phi = atan2(x, y) - atan2(robot.l3, r);

    D2 = r^2  + (z-robot.L1)^2;
    theta2 = acos((D2 - robot.L2^2 - robot.L3^2) / (2 * robot.L2 * robot.L3));

    alpha = atan2(r, z - robot.L1);
    beta = acos((robot.L2^2 + D2 - robot.L3^2) / (2 * robot.L2 * sqrt(D2)));
    theta1 = alpha - beta;

    q = [phi; theta1; -theta2];
end