function imagem_saida = convolucao_com_offset(imagem_path, kernel, offset, output_path)
    % Carrega a imagem e converte para escala de cinza
    imagem = imread(imagem_path);
    imagem_gray = rgb2gray(imagem);

    [altura, largura] = size(imagem_gray);
    [k_altura, k_largura] = size(kernel);
    pad_altura = floor(k_altura / 2);
    pad_largura = floor(k_largura / 2);

    % Inicializa a imagem de saída
    imagem_saida = zeros(altura, largura);

    % Aplica a operação de convolução
    for i = (1 + pad_altura):(altura - pad_altura)
        for j = (1 + pad_largura):(largura - pad_largura)
            conv_sum = 0;
            for m = 1:k_altura
                for n = 1:k_largura
                    conv_sum += imagem_gray(i + m - pad_altura - 1, j + n - pad_largura - 1) * kernel(m, n);
                end
            end
            conv_sum += offset;
            % Garante que os valores da imagem estão dentro dos limites [0, 255]
            imagem_saida(i, j) = min(max(conv_sum, 0), 255);
        end
    end

    % Salva a imagem resultante
    imwrite(uint8(imagem_saida), output_path);
end

