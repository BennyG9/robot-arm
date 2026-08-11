function [valid, base, shoulder, elbow] = verify_angles(q, robot)

    phi = q(1);
    theta1 = q(2);
    theta2 = q(3);

    base = (phi>=robot.base.min_angle && phi<=robot.base.max_angle);
    shoulder = (theta1>=robot.shoulder.min_angle && theta1<=robot.shoulder.max_angle);
    elbow = (theta2>=robot.elbow.min_angle && theta2<=robot.elbow.max_angle);

    valid = base && shoulder && elbow;
end