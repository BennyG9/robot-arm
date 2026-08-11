function robot = load_robot()

    config = jsondecode(fileread("../config/robot.json"));

    robot.name = config.name;

    robot.metadata = config.metadata;

    robot.L1 = config.links.L1;
    robot.L2 = config.links.L2;
    robot.L3 = config.links.L3;
    robot.l3 = config.joints.elbow.l;

    robot.base = config.joints.base;
    robot.shoulder = config.joints.shoulder;
    robot.elbow = config.joints.elbow;

    robot.base.min_angle = deg2rad(robot.base.min_angle);
    robot.base.max_angle = deg2rad(robot.base.max_angle);
    robot.shoulder.min_angle = deg2rad(robot.shoulder.min_angle);
    robot.shoulder.max_angle = deg2rad(robot.shoulder.max_angle);
    robot.elbow.min_angle = deg2rad(robot.elbow.min_angle);
    robot.elbow.max_angle = deg2rad(robot.elbow.max_angle);
end