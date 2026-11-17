function [planned_data, planned_time_param, executed_data, executed_timestamps] = get_trajectory_data(dir_path, test_index)

    %verify that desired test exists using metadata.json
    metadata_path = dir_path + "metadata.json";
    metadata = jsondecode(fileread(metadata_path));
    if(metadata.logged_tests < test_index)
        disp("ERROR: log does not exist");
        planned_data = null;
        executed_data = null;
        return;
    end

    %path to directory containing all trajectory data 
    test_dir_path = dir_path + "trajectory" + string(test_index) + "/";

    %data paths 
    planned_path = test_dir_path + "planned.csv";
    executed_path = test_dir_path + "executed.csv";

    %reading raw data from CSV files 
    planned_data_raw = readtable(planned_path);
    executed_data_raw = readtable(executed_path);
    
    %format data for planned trajectory
    planned_data = [
        deg2rad(planned_data_raw.base_deg), ...
        deg2rad(planned_data_raw.shoulder_deg), ...
        deg2rad(planned_data_raw.elbow_deg)
    ]';
    planned_time_param = planned_data_raw.dt';

    %format data for executed trajectory 
    executed_data = [
        deg2rad(executed_data_raw.base_deg), ...
        deg2rad(executed_data_raw.shoulder_deg), ...
        deg2rad(executed_data_raw.elbow_deg)
    ]';
    executed_timestamps = executed_data_raw.time_stamp';
end