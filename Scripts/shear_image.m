function sheared_image = shear_image(image_path, shear_x, shear_y, output_path)
    % Carrega a imagem
    image = imread(image_path);
    [rows, cols, num_channels] = size(image);

    % Cria uma nova imagem com fundo preto
    sheared_image = zeros(rows, cols, num_channels, "uint8");

    % Aplica a transformação de cisalhamento
    for i = 1:rows
        for j = 1:cols
            new_x = j + shear_x * i;
            new_y = i + shear_y * j;
            if (new_x >= 1 && new_x <= cols && new_y >= 1 && new_y <= rows)
                sheared_image(new_y, new_x, :) = image(i, j, :);
            end
        end
    end

    % Salva a imagem cisalhada
    imwrite(sheared_image, output_path);
    fprintf('Imagem salva com sucesso em: %s\n', output_path);
end

