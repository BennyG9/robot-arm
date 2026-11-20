function errors = vector_errors_alp(path1, param1, path2, param2)
    
    %make path1 the longer path (problematic if path is very stationary) 
    if(size(path1, 2) < size(path2, 2))
        path_temp = path1;
        path1 = path2;
        path2 = path_temp;
    end

    %init errors list to size of path with more samples 
    errors = zeros(size(path1));

    %path2 index
    index_p2 = 1;

    %iterate over entirety of path1
    for index_p1 = 1:size(path1, 2)

        %get current point on path1
        path1_point = path1(:, index_p1);

        %get 2 closest points on path2 (1 each side)

        %linearly interpolate point on path2
        path2_interpoalted_point = 0;

        %compute and store VECTOR errors
        error = path1_point - path2_interpoalted_point;
        errors(:, index_p1) = error(:);
    end
    
end