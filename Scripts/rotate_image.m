function rotated_image = rotate_image(image, angle, output_path)
    rotated_image = imrotate(image, angle);
    imwrite(rotated_image, output_path);
endfunction

