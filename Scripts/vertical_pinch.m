function pinched_image = vertical_pinch(image_path, amount, output_path)
    % Carrega a imagem
    image = imread(image_path);
    [rows, cols, num_channels] = size(image);

    % Criação dos mapas de índices para o efeito de pinch
    [X, Y] = meshgrid(1:cols, 1:rows);

    % Altera as coordenadas Y para criar o efeito de pinch
    Y = Y + amount * sin(pi * X / cols);

    % Inicializa a imagem de saída
    pinched_image = zeros(rows, cols, num_channels, class(image));

    % Aplica a transformação
    for i = 1:rows
        for j = 1:cols
            new_x = round(X(i, j));
            new_y = round(Y(i, j));
            if (new_x >= 1 && new_x <= cols && new_y >= 1 && new_y <= rows)
                pinched_image(i, j, :) = image(new_y, new_x, :);
            end
        end
    end

    % Salva a imagem resultante
    imwrite(pinched_image, output_path);
end

