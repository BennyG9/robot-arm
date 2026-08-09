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
%     90;
%     -90
% ]);
% T1 = forward_kinematics(q1, robot);
% plot_robot(T1);
% 
% 
% pos_fig2 = create_robot_figure();
% q2 = inverse_kinematics(T1(1:3,4,5), robot);
% T2 = forward_kinematics(q2, robot);
% plot_robot(T2);
% 
% disp(T1(:,:,5));
% disp(T2(:,:,5));

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

