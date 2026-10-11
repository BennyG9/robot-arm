function dt_func = min_path_time_func(Q, robot)

    DQ = diff(Q, 1, 3);
    %D2Q = diff(Q, 2, 3);

    dQdt_max = [robot.base.max_speed; robot.shoulder.max_speed; robot.elbow.max_speed];
    %D2Q_max = [];

    dT = abs(DQ ./ dQdt_max);
    
    dt_func = (max(dT, [], 1));

end