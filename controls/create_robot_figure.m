function fig = create_robot_figure()
    fig = figure;
    
    hold on;
    grid on;
    axis equal;

    xlim([-0.4 0.4]);
    ylim([-0.4 0.4]);
    zlim([0 0.4]);

    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    
    view(45, 30);
end