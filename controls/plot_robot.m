function plot_robot(R0, R1, R2, R3)
    X = [0, R0(1), R1(1), R2(1), R3(1)];
    Y = [0, R0(2), R1(2), R2(2), R3(2)];
    Z = [0, R0(3), R1(3), R2(3), R3(3)];

    cla;
    hold on;
    plot3(X,Y,Z, '-o', 'LineWidth', 3);
    hold off;
    drawnow;

    grid on;
    axis equal;
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    view(45, 30);
end