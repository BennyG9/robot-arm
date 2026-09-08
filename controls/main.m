%% INITIALIZATIONS

clear;
clc;
close all;

robot = load_robot();


%% SINGLE POSITION

%%% Position #1
% pos_fig1 = create_robot_figure();
% q1 = deg2rad([
%     0;
%     0;
%     0
% ]);
% T1 = forward_kinematics(q1, robot);
% plot_robot(T1);
% 
% pos_fig2 = create_robot_figure();
% q2 = inverse_kinematics(T1(1:3,4,6), robot);
% T2 = forward_kinematics(q2, robot);
% plot_robot(T2);
% 
% disp(T1(:,:,6));
% disp(T2(:,:,6));

%%% Random Position
% pos_fig1 = create_robot_figure();
% q1 = random_angles(robot);
% T1 = forward_kinematics(q1, robot);
% plot_robot(T1);
% 
% pos_fig2 = create_robot_figure();
% [q2, succ] = inverse_kinematics(T1(1:3,4,6), robot);
% q2 = q2(1:3, 1);
% T2 = forward_kinematics(q2, robot);
% plot_robot(T2);
% 
% disp(T1(:,:,6));
% disp(T2(:,:,6));
% 
% fprintf("Original Angles:\n");
% disp(rad2deg(q1));
% 
% fprintf("IK Angles: %s\n", string(succ));
% disp(rad2deg(q2));
% 
% fprintf( "Valid Position: %s \n", string( verify_position(T1(1:3,4,5), robot) ) );

%%% Position #2
% pos_fig1 = create_robot_figure();
% q1 = deg2rad([
%     75.2256;
%     29.6251;
%     -110.3858
% ]);
% T1 = forward_kinematics(q1, robot);
% plot_robot(T1);
% 
% pos_fig2 = create_robot_figure();
% [q2, succ] = inverse_kinematics(T1(1:3,4,6), robot);
% q2 = q2(1:3, 1);
% T2 = forward_kinematics(q2, robot);
% plot_robot(T2);
% 
% disp(T1(:,:,6));
% disp(T2(:,:,6));
% 
% fprintf("Original Angles:\n");
% disp(rad2deg(q1));
% 
% fprintf("IK Angles: %s\n", string(succ));
% disp(rad2deg(q2));
% 
% fprintf( "Valid Position: %s \n", string( verify_position(T1(1:3,4,5), robot) ) );


%% ANGLE SWEEP ANIMATION

%%% Animation #1
% an_fig1 = create_robot_figure();
% 
% Q = [
%     linspace(pi/2, -pi/2, 100);
%     linspace(0, pi/2, 100);
%     linspace(0, -pi/2, 100);
% ];
% 
% animate_path("angles", Q, robot);


%% IK TEST

%%% Test #1
% tests = 10^3;
% 
% pos_err = zeros(1,tests);
% failed_verifications = [];
% for i = 1:tests
%     q1 = random_angles(robot);
%     T1 = forward_kinematics(q1, robot);
%     q2 = inverse_kinematics(T1(1:3,4,5), robot);
%     q2 = q2(1:3,1);
% 
%     T2 = forward_kinematics(q2, robot);
% 
%     p1 = T1(1:3,4,5);
%     p2 = T2(1:3,4,5);
% 
%     pos_err(i) = norm(p1 - p2);
% 
%     if(~verify_position(T1(1:3,4,5), robot))
%         failed_verifications(1:3,end+1) = q1;
%     end
% end
% 
% fprintf("Attempts:          : %i \n", tests);
% fprintf("Mean position error: %e m\n", mean(pos_err));
% fprintf("Max position error : %e m\n", max(pos_err));
% fprintf("Std deviation      : %e m\n", std(pos_err));
% fprintf("Failed Attempts    : %i \n", length(failed_verifications));
% 
% histogram(pos_err);
% xlabel("Position Error (m)");
% ylabel("Count");
% 
% for q = failed_verifications
%     disp(rad2deg(q));
% end

%%% Test #2
% tests = 10^3;
% 
% pos_err = [];
% failed_verifications = [];
% 
% for i = 1:tests
%     q1 = random_angles(robot);
%     T1 = forward_kinematics(q1, robot);
%     q2 = inverse_kinematics(T1(1:3,4,5), robot);
% 
%     % if(size(q2, 2) < 2)
%     %     continue;
%     % end
% 
%     for q = q2(:,:)
% 
%         T2 = forward_kinematics(q, robot);
% 
%         p1 = T1(1:3,4,5);
%         p2 = T2(1:3,4,5);
% 
%         pos_err(end+1) = norm(p1 - p2);
% 
%         if(~verify_position(T1(1:3,4,5), robot))
%             failed_verifications(1:3,end+1) = q1;
%         end
% 
%     end
% end
% 
% fprintf("Attempts:          : %i \n", tests);
% fprintf("Mean position error: %e m\n", mean(pos_err));
% fprintf("Max position error : %e m\n", max(pos_err));
% fprintf("Std deviation      : %e m\n", std(pos_err));
% fprintf("Failed Attempts    : %i \n", length(failed_verifications));
% 
% histogram(pos_err);
% xlabel("Position Error (m)");
% ylabel("Count");
% 
% for q = failed_verifications
%     disp(rad2deg(q));
% end


%% ANIMATE PATHS

%%% Random Linear Path
% path_fig1 = create_robot_figure();
% T1 = forward_kinematics(random_angles(robot), robot);
% T2 = forward_kinematics(random_angles(robot), robot);
% R = line_path(T1(1:3,4,6), T2(1:3,4,6), 200);
% Q = path2angles(R, robot);
% %disp(Q);
% %disp(Q(:,1,:));
% animate_path("angles", Q(:,1,:), robot);

%%% Random Sequence of Linear Paths 
% path_fig2 = create_robot_figure();
% num_points = 5;
% T1 = forward_kinematics(random_angles(robot), robot);
% for i = 1:num_points
%     T2 = forward_kinematics(random_angles(robot), robot);
%     R = line_path(T1(1:3,4,6), T2(1:3,4,6), 200);
%     Q = path2angles(R, robot);
%     animate_path("angles", Q(:,1,:), robot);
%     T1 = T2;
%     pause(0.5);
% end

%%% Linear Path Boomerang
path_fig3 = create_robot_figure();
q1 = deg2rad([
    -70;
    70;
    -100;
]);
q2 = deg2rad([
    45;
    30;
    -60;
]);
T1 = forward_kinematics(q1, robot);
T2 = forward_kinematics(q2, robot);
R1 = line_path(T1(1:3,4,6), T2(1:3,4,6), 200);
Q1 = path2angles(R1, robot);
R2 = line_path(T2(1:3,4,6), T1(1:3,4,6), 200);
Q2 = path2angles(R2, robot);
plot_robot(T1);
pause(1);
animate_path("angles", Q1(:,1,:), robot);
pause(0.5);
animate_path("angles", Q2(:,1,:), robot);



