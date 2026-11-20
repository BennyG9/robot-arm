function [param, arc_length] = arc_length_parameterization(points)

    arc_length_acc = zeros(1, size(points, 2));

    for path_index = 2:size(points, 2)
        %compute linear distance between current point and last point
        dX = norm(points(:,path_index) - points(:,path_index-1));

        %accumulate arc length in list
        arc_length_acc(path_index) = arc_length_acc(path_index-1) + dX; 
    end

    %total arc length is just the fully accumulated value 
    arc_length = arc_length_acc(end);

    %scale arc length accumulation 
    param = arc_length_acc ./ arc_length; 
end