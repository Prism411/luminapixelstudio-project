function imagem_agucada = agucamento_bordas(imagem, output_path)
    kernel_laplaciano = [0 -1 0; -1 4 -1; 0 -1 0];
    imagem_agucada = imfilter(imagem, kernel_laplaciano, 'same');
    imwrite(imagem_agucada, output_path);
endfunction

