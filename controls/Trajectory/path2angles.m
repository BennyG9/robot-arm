function Q = path2angles(path, robot)
    Q = [];
    path_index = 0;
    for pos = path
        path_index = path_index + 1;

        q = inverse_kinematics(pos, robot);
        disp(q);

        %Q(1:3, end+1) = q(1:3, 1);
        if(isempty(Q))
            Q(1:3, path_index) = q(1:3,1);
            continue;
        end

        min_norm = Inf;
        for qi = q
            current_norm = norm(qi - Q(1:3, end));
            if(current_norm < min_norm)
                min_norm = current_norm;
                Q(1:3, path_index) = qi;
            end
        end
    end
end