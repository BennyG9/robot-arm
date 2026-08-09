function plot_robot(T)

    X = reshape(T(1,4,:), 1, []);
    Y = reshape(T(2,4,:), 1, []);
    Z = reshape(T(3,4,:), 1, []);

    cla;
    hold on;
    plot3(X,Y,Z, '-o', 'LineWidth', 3);

    scale = 0.04;
    for i = 1:size(T,3)
        origin = T(1:3,4,i);

        x_axis = T(1:3,1,i);
        y_axis = T(1:3,2,i);
        z_axis = T(1:3,3,i);

        quiver3(origin(1), origin(2), origin(3), scale*x_axis(1), scale*x_axis(2), scale*x_axis(3), 'r');
        quiver3(origin(1), origin(2), origin(3), scale*y_axis(1), scale*y_axis(2), scale*y_axis(3), 'g');
        quiver3(origin(1), origin(2), origin(3), scale*z_axis(1), scale*z_axis(2), scale*z_axis(3), 'b');
    end

    hold off;
    drawnow;
end