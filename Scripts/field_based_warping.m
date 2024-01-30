function warped_image = field_based_warping(image_path, field, output_path)
    % Carrega a imagem
    image = imread(image_path);
    [rows, cols, num_channels] = size(image);

    % Inicializa os mapas de coordenadas para o warping
    map_x = zeros(rows, cols);
    map_y = zeros(rows, cols);

    % Assegura que 'field' é uma matriz de células com elementos sendo vetores de dois elementos
    if !iscell(field) || size(field, 1) != rows || size(field, 2) != cols
        error('Field deve ser uma matriz de células com o mesmo tamanho da imagem.');
    end

    % Aplica o campo de deslocamento
    for i = 1:rows
        for j = 1:cols
            displacement = field{i, j};  % Obtem o vetor de deslocamento
            map_x(i, j) = j + displacement(1);  % Deslocamento em x
            map_y(i, j) = i + displacement(2);  % Deslocamento em y
        end
    end

    % Inicializa a imagem de saída
    warped_image = zeros(rows, cols, num_channels, class(image));

    % Aplica a transformação
    for i = 1:rows
        for j = 1:cols
            new_x = round(map_x(i, j));
            new_y = round(map_y(i, j));
            if (new_x >= 1 && new_x <= cols && new_y >= 1 && new_y <= rows)
                warped_image(i, j, :) = image(new_y, new_x, :);
            end
        end
    end

    % Salva a imagem resultante
    imwrite(warped_image, output_path);
end

