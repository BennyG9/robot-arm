function Q = path2angles(path, robot)
    Q = [];
    path_index = 0;

    invalid_indices = [];
    invalid_segments = 0;

    for pos = path
        path_index = path_index + 1;

        [q, valid] = inverse_kinematics(pos, robot);
        % disp(q);
        % disp(valid);

        if(valid == 0)
            Q(1:3, path_index) = q(1:3, 1);
            if(invalid_segments == 0 || invalid_indices(invalid_segments, end) ~= path_index-1)
                invalid_segments = invalid_segments + 1;
                invalid_indices(invalid_segments, 1) = path_index;
                invalid_indices(invalid_segments, 2) = path_index;
            else
                invalid_indices(invalid_segments, 2) = path_index;
            end
            continue;
        end
        
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

    disp(invalid_indices);

    if(isempty(invalid_indices))
        return;
    end

    for invalid_segments = 1:size(invalid_indices,1)
        i_start = invalid_indices(invalid_segments, 1);
        i_end = invalid_indices(invalid_segments, 2);
        n = i_end - i_start + 1 + 2;
        q_start = Q(1:3, i_start-1);
        q_end = Q(1:3, i_end+1);
        Q(1:3, i_start-1:i_end+1) = [linspace(q_start(1),q_end(1),n); linspace(q_start(2),q_end(2),n); linspace(q_start(3),q_end(3),n)];
    end
end