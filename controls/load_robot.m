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
end