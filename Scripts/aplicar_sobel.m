function magnitude = aplicar_sobel(imagem, output_path)
    [grad_x, grad_y] = imgradientxy(imagem, 'sobel');
    magnitude = sqrt(grad_x .^ 2 + grad_y .^ 2);
    imwrite(uint8(magnitude), output_path);
endfunction
