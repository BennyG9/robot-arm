function plot_trajectory(trajectory, time_stamps, robot)

    marker_size = 60;
    color_start = [0, 0, 1]; %blue
    color_end = [1, 0, 0]; %red
    color_diff = color_end - color_start;

    coordinates = zeros(size(trajectory));
    colors = zeros(size(trajectory, 2), 3);
    first_frames = zeros(4,4,6);
    last_frames = zeros(4,4,6);
    trajectory_index = 1;

    time_start = time_stamps(1);
    time_end = time_stamps(size(time_stamps, 2));

    for q = trajectory

        %convert angles to cartesian frames 
        frames = forward_kinematics(q, robot);
        end_coords = frames(1:3,4,6);

        %save first and last frames for later use
        if(trajectory_index == 1)
            first_frames(:,:,:) = frames(:,:,:);
        elseif(trajectory_index == size(trajectory, 2))
            last_frames(:,:,:) = frames(:,:,:);
        end

        %save coordinates 
        coordinates(:, trajectory_index) = end_coords(:);

        %calculate color gradient
        time_current = time_stamps(trajectory_index);
        temporal_progress = (time_current - time_start) / (time_end - time_start);
        point_rgb = color_start + (color_diff .* temporal_progress);
        colors(trajectory_index, :) = point_rgb(:);        

        %next point
        trajectory_index = trajectory_index + 1;
    end

    X = coordinates(1, :);
    Y = coordinates(2, :);
    Z = coordinates(3, :);

    %disp(colors);

    scatter3(X, Y, Z, marker_size, colors, 'filled');
    plot_robot(first_frames, false);
    plot_robot(last_frames, false);
end