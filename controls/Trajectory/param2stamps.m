function time_stamps = param2stamps(time_parameterization_function)

    %check for appended 0, init time_stamps accordingly
    extra_index = 1;
    if(time_parameterization_function(end) == 0)
        extra_index = 0;
    end
    time_stamps = zeros(size(time_parameterization_function) + extra_index);

    %fill time_stamps 
    for i = 2:length(time_stamps)
        time_stamps(i) = time_stamps(i-1) + time_parameterization_function(i-1);
    end
end