function valid = verify_position(position, robot)
    epsilon = 1e-8;

    [q, valid] = inverse_kinematics(position, robot);

    if(~valid)
        return;
    end

    if(~verify_angles(q, robot))
        valid = false;
        return;
    end

    T = forward_kinematics(q, robot);
    robot_position = T(1:3,4,5);

    valid = norm(position-robot_position) <= epsilon;
end