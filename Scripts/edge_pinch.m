function pinched_edges_image = edge_pinch(image_path, amount, output_path)
    % Carrega a imagem
    image = imread(image_path);
    [rows, cols, num_channels] = size(image);

    % Calcula o centro da imagem
    center_x = cols / 2;
    center_y = rows / 2;

    % Criação dos mapas de índices para o efeito de pinch nas bordas
    [X, Y] = meshgrid(1:cols, 1:rows);

    % Calcula as distâncias normalizadas ao centro da imagem
    distance_x = (X - center_x) / center_x;
    distance_y = (Y - center_y) / center_y;

    % Calcula um fator de escala baseado na distância e no amount
    scale_x = 1 - amount * distance_x .^ 2;
    scale_y = 1 - amount * distance_y .^ 2;

    % Ajusta as coordenadas dos pixels em direção ao centro
    X = center_x + (X - center_x) .* scale_x;
    Y = center_y + (Y - center_y) .* scale_y;

    % Inicializa a imagem de saída
    pinched_edges_image = zeros(rows, cols, num_channels, class(image));

    % Aplica a transformação
    for i = 1:rows
        for j = 1:cols
            new_x = round(X(i, j));
            new_y = round(Y(i, j));
            if (new_x >= 1 && new_x <= cols && new_y >= 1 && new_y <= rows)
                pinched_edges_image(i, j, :) = image(new_y, new_x, :);
            end
        end
    end

    % Salva a imagem resultante
    imwrite(pinched_edges_image, output_path);
end

