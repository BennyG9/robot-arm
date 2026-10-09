function dt = min_path_time_const(Q, robot)

    DQ = diff(Q, 1, 3);
    %D2Q = diff(Q, 2, 3);

    dQdt_max = [robot.base.max_speed; robot.shoulder.max_speed; robot.elbow.max_speed];
    %D2Q_max = [];

    %disp(DQ);
    %disp(DQ_max);

    % disp(size(Q));
    % disp(size(DQ));

    dT = abs(DQ ./ dQdt_max);
    dt = max(dT(:));

    % disp(dt);
end