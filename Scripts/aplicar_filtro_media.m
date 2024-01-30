function imagem_filtrada = aplicar_filtro_media(imagem, kernel_size)
    kernel = ones(kernel_size) / kernel_size^2;
    imagem_filtrada = filter2(kernel, imagem);
endfunction
