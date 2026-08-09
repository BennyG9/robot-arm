function T = forward_kinematics(q, robot)

    phi = q(1);
    theta1 = q(2);
    theta2 = q(3);

    %base frame relative to stationary environment frame
    T01 = [
        rot_z(-phi) [0; 0; 0];
        0 0 0 1
    ];

    %shoulder frame relative to base
    T12 = [
        rot_x(-theta1) [0; 0; robot.L1];
        0 0 0 1
    ];

    %elbow1 frame relative to shoulder
    T23 = [
        rot_y(pi/2) [0; 0; robot.L2];
        0 0 0 1
    ];

    %elbow2 frame relative to elbow1
    T34 = [
        rot_y(-pi/2)*rot_x(theta2) [0; 0; robot.l3];
        0 0 0 1
    ];

    %end effector frame relative to elbow2
    T45 = [
        1 0 0 0;
        0 1 0 0;
        0 0 1 robot.L3;
        0 0 0 1
    ];

    T(:,:,1) = T01; 
    T(:,:,2) = T01*T12;
    T(:,:,3) = T01*T12*T23;
    T(:,:,4) = T01*T12*T23*T34;
    T(:,:,5) = T01*T12*T23*T34*T45;
end