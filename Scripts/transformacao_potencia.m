function transformacao_potencia(image_path, output_path, gamma)
    image = imread(image_path);
    gamma_corrected = imadjust(image, [], [], gamma);
    imwrite(gamma_corrected, output_path);
endfunction

