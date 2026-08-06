% set at fixed angle

phi = 0;
theta1 = 0;
theta2 = 0;

R = forward_kinematics(phi, theta1, theta2, 3, 2, 1, 0.5);
disp(R);
plot_robot(R(:,1), R(:,2), R(:,3), R(:,4));