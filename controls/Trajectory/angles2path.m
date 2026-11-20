function path = angles2path(Q, robot)

    path = zeros(size(Q));
    index = 1;

    for q = Q

        %discard angles out of reach
        valid_angles = verify_angles(q, robot);
        if(~valid_angles)
            path(:, index) = [NaN, NaN, NaN];
            index = index + 1;
            continue;
        end

        %convert angles to cartesian frames 
        frames = forward_kinematics(q, robot);
        end_coords = frames(1:3,4,6);

        %save coordinates 
        path(:, index) = end_coords(:);

        index = index + 1;    
    end

end