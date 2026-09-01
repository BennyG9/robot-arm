function angles = clamp_angles(q, robot)
    joints = [robot.base, robot.shoulder, robot.elbow];
    angles = q;
    for i = 1:length(q)
        joint = joints(i);
        if(q(i) < joint.min_angle)
            angles(i) = joint.min_angle;
        elseif(q(i) > joint.max_angle)
            angles(i) = joint.max_angle;
        end
    end
end