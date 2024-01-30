function imagem_filtrada = aplicar_filtro_mediana(imagem, kernel_size)
    imagem_filtrada = medfilt2(imagem, [kernel_size kernel_size]);
endfunction
