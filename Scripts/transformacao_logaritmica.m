function transformacao_logaritmica(image_path, output_path, c)
    image = double(imread(image_path));
    log_transformed = c * log(1 + image);
    imwrite(uint8(log_transformed), output_path);
endfunction

