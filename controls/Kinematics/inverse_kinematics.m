function [q, valid] = inverse_kinematics(position, robot)

    valid = true;

    x = position(1);
    y = position(2);
    z = position(3);

    %verify and caluculate horizontal radius
    r2 = (x^2 + y^2 - robot.l3^2);
    if(r2 < 0)
        valid = false;
        q = [0; 0; 0];
        return;
    end
    r = sqrt(r2);

    %calculate both phi angles
    phi = atan2(x, y) - atan2(robot.l3, r);
    if(phi < -pi)
        phi = phi + 2*pi;
    elseif(phi > pi)
        phi = phi - 2*pi;
    end
    phi2 = atan2(x, y) + atan2(robot.l3, r) - pi;
    if(phi2 < -pi)
        phi2 = phi2 + 2*pi;
    elseif(phi2 > pi)
        phi2 = phi2 - 2*pi;
    end

    %calculate and verify theta2
    D2 = r^2  + (z-robot.L1)^2;
    if(D2 < 1e-14)
        valid = false;
        q = [0; 0; 0];
        return;
    end
    C2 = (D2 - robot.L2^2 - robot.L3^2) / (2 * robot.L2 * robot.L3);
    if(abs(C2) > 1)
        valid = false;
        q = [0; 0; 0];
        return;
    end
    C2 = max(-1, min(1, C2));
    theta2 = acos(C2);

    %calculate alpha and beta for theta1 configurations
    alpha = atan2(r, z - robot.L1);
    C1 = (robot.L2^2 + D2 - robot.L3^2) / (2 * robot.L2 * sqrt(D2));
    if(abs(C1) > 1)
        valid = false;
        q = [0; 0; 0];
        return;
    end
    C1 = max(-1, min(1, C1));
    beta = acos(C1);

    %all positionally accurate configurations
    Q = [
         phi        phi2          phi         phi2;
        alpha-beta  -alpha+beta  alpha+beta  alpha-beta;
        -theta2     theta2       theta2       -theta2
    ];

    %return configuration with valid angles
    for i = 1:4
        q = Q(1:3,i);
        if(verify_angles(q, robot))
            return;
        end
    end

    %no valid configurations
    valid = false;
    q = [0; 0; 0];
end