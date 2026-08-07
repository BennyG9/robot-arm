function plot_robot(R)

    X = [0, R(1,:)];
    Y = [0, R(2,:)];
    Z = [0, R(3,:)];

    cla;
    hold on;
    plot3(X,Y,Z, '-o', 'LineWidth', 3);

    % grid on;
    % axis equal;
    % xlim([-0.4 0.4]);
    % ylim([-0.4 0.4]);
    % zlim([0 0.4]);
    % xlabel('X');
    % ylabel('Y');
    % zlabel('Z');
    % view(45, 30);

    hold off;
    drawnow;
end