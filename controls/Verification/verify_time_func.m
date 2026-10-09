function valid = verify_time_func(Q, dt, robot)

    dT = ones(1, size(Q,3));
    if(isscalar(dt))
        dT = dt * dT;
    else
        dT = dt;
    end
    %disp(size(Q));
    %disp(size(dT));
    
    DQ = diff(Q, 1, 3);
    dQdt = DQ ./ dT;
    dQdt_max = [robot.base.max_speed; robot.shoulder.max_speed; robot.elbow.max_speed];

    speed_ratio = abs(dQdt ./ dQdt_max);

    valid = all(speed_ratio <= 1, 'all');
end