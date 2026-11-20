function errors = norm_errors_alp(path1, param1, path2, param2)
   
    %get vector errors 
    vector_errors = vector_errors_alp(path1, param1, path2, param2);
   
    %calculate norm errors from vector errors 
    errors = vecnorm(vector_errors, 2, 1);
end