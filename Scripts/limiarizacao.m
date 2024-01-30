function limiarizacao(image_path, output_path, threshold)
    image = imread(image_path);
    thresholded = im2bw(image, threshold / 255);
    imwrite(thresholded, output_path);
endfunction

