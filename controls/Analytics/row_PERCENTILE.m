function value = row_PERCENTILE(data, percentile)
    % sorted_errors = [
    %     sort(data(1,:));
    %     sort(data(2,:));
    %     sort(data(3,:));
    % ];

    sorted_errors = zeros(size(data));
    for i = 1:size(data, 1)
        sorted_errors(i, :) = sort(data(i, :));
    end

    r = (percentile / 100) * (size(data, 2) - 1) + 1;
    ri = fix(r);
    rf = r - ri;

    if(r == ri)
        value = sorted_errors(:, ri);
    else
        value = sorted_errors(:, ri) + rf*(sorted_errors(:, ri+1) - sorted_errors(:, ri));
    end
end