function R = forward_kinematics(phi, theta1, theta2, L1, L2, L3, l3)
    z0 = L1;
    R0 = [0; 0; z0];

    r = L2*sin(theta1);
    x1 = r*sin(phi);
    y1 = r*cos(phi);
    z1 = L1 + L2*cos(theta1);
    R1 = [x1 ;y1; z1];

    x2 = x1 + l3*cos(phi);
    y2 = y1 - l3*sin(phi);
    z2 = z1;
    R2 = [x2; y2; z2];

    r = r + L3*sin(theta1-theta2);
    x3 = r*sin(phi) + l3*cos(phi);
    y3 = r*cos(phi) + l3*sin(phi);
    z3 = L1 + L2*cos(theta1) + L3*cos(theta1-theta2);
    R3 = [x3; y3; z3];

    R = [R0, R1, R2, R3];
end