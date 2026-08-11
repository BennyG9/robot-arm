function q = random_angles(robot)

    phi = robot.base.min_angle + (robot.base.max_angle - robot.base.min_angle) * rand();
    theta1 = robot.shoulder.min_angle + (robot.shoulder.max_angle - robot.shoulder.min_angle) * rand();
    theta2 = robot.elbow.min_angle + (robot.elbow.max_angle - robot.elbow.min_angle) * rand();

    q = [phi; theta1; theta2];
end