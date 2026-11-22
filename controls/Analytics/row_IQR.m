function iqr = row_IQR(data)
    iqr = row_PERCENTILE(data, 75.0) - row_PERCENTILE(data, 25.0);
end