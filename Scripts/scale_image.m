function scaled_image = scale_image(image, scale_x, scale_y, output_path)
    scaled_image = imresize(image, [scale_x, scale_y]);
    imwrite(scaled_image, output_path);
endfunction
