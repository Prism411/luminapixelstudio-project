function alargamento_contraste(image_path, output_path)
    image = imread(image_path);
    contrast_stretched = imadjust(image, [0.39, 0.78], [0, 1]);
    imwrite(contrast_stretched, output_path);
endfunction

