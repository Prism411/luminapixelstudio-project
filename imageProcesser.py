from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.ndimage import generic_filter
def redimensionar_imagem(image_path, novo_tamanho):
    # Abra a imagem
    imagem = Image.open(image_path)

    # Redimensione a imagem para o novo tamanho
    imagem_redimensionada = imagem.resize(novo_tamanho)

    return imagem_redimensionada
def dissolve_cruzado(image_path1, image_path2, output_path,alpha):
    # Redimensione as imagens para terem o mesmo tamanho
    novo_tamanho = (800, 600)  # Substitua pelo tamanho desejado
    image1 = redimensionar_imagem(image_path1, novo_tamanho)
    image2 = redimensionar_imagem(image_path2, novo_tamanho)

    # Crie uma imagem de saída com o mesmo tamanho das imagens de entrada
    output_image = Image.new("RGB", image1.size)

    # Itere através de cada pixel e aplique a operação de Dissolve Cruzado uniforme
    for x in range(image1.width):
        for y in range(image1.height):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))
            blended_pixel = (
                int(alpha * pixel1[0] + (1 - alpha) * pixel2[0]),
                int(alpha * pixel1[1] + (1 - alpha) * pixel2[1]),
                int(alpha * pixel1[2] + (1 - alpha) * pixel2[2])
            )
            output_image.putpixel((x, y), blended_pixel)

    # Salve a imagem resultante
    output_image.save(output_path)

def dissolve_cruzado_nao_uniforme(image_path1, image_path2, output_path, alpha):
    # Redimensione as imagens para terem o mesmo tamanho
    novo_tamanho = (800, 600)  # Substitua pelo tamanho desejado
    image1 = redimensionar_imagem(image_path1, novo_tamanho)
    image2 = redimensionar_imagem(image_path2, novo_tamanho)

    # Crie uma imagem de saída com o mesmo tamanho das imagens de entrada
    output_image = Image.new("RGB", image1.size)


    # Itere através de cada pixel e aplique a operação de Dissolve Cruzado uniforme
    for x in range(image1.width):
        for y in range(image1.height):
            pixel1 = image1.getpixel((x, y))
            pixel2 = image2.getpixel((x, y))
            blended_pixel = (
                int(alpha * pixel1[0] + (1 - alpha) * pixel2[0]),
                int(alpha * pixel1[1] + (1 - alpha) * pixel2[1]),
                int(alpha * pixel1[2] + (1 - alpha) * pixel2[2])
            )
            output_image.putpixel((x, y), blended_pixel)

    # Salve a imagem resultante
    output_image.save(output_path)

def negativo(image_path, output_path):
    image = Image.open(image_path)
    negative_image = Image.eval(image, lambda x: 255 - x)
    negative_image.save(output_path)

def alargamento_contraste(image_path, output_path):
    image = Image.open(image_path)
    contrast_stretched = Image.eval(image, lambda x: (x - 100) * 255 / (200 - 100) if 100 <= x <= 200 else 0 if x < 100 else 255)
    contrast_stretched.save(output_path)

def limiarizacao(image_path, output_path, threshold):
    image = Image.open(image_path)
    thresholded = Image.eval(image, lambda x: 0 if x < threshold else 255)
    thresholded.save(output_path)

def transformacao_potencia(image_path, output_path, gamma):
    image = Image.open(image_path)
    gamma_corrected = Image.eval(image, lambda x: int(255 * (x / 255) ** gamma))
    gamma_corrected.save(output_path)

def transformacao_logaritmica(image_path, output_path, c):
    image = Image.open(image_path)
    log_transformed = Image.eval(image, lambda x: int(c * np.log(1 + x)))
    log_transformed.save(output_path)

import matplotlib.pyplot as plt

def expand_histogram_auto(image, gain, output_path, show_histogram):
    # Aplica a expansão do histograma de forma automática
    expanded_image = np.copy(image)
    expanded_image = expanded_image * gain
    expanded_image[expanded_image < 0] = 0
    expanded_image[expanded_image > 255] = 255
    imagem_processada_uint8 = expanded_image.astype(np.uint8)
    cv2.imwrite(output_path, imagem_processada_uint8)

    if show_histogram:
        plt.hist(imagem_processada_uint8.ravel(), bins=256, range=(0, 256))
        plt.title("Histograma - Expansão Automática")
        plt.show()

    return expanded_image



def histogram_equalization(image, output_path, show_histogram):
    # Calcula o histograma da imagem
    hist, _ = np.histogram(image, bins=256, range=(0, 256))

    # Calcula a função de distribuição acumulada (CDF) do histograma
    cdf = hist.cumsum()

    # Normaliza a CDF para o intervalo [0, 255]
    cdf_normalized = ((cdf - cdf.min()) * 255) / (cdf.max() - cdf.min())

    # Aplica a equalização do histograma à imagem
    equalized_image = cdf_normalized[image]
    imagem_processada_uint8 = equalized_image.astype(np.uint8)
    cv2.imwrite(output_path, imagem_processada_uint8)

    if show_histogram:
        plt.hist(imagem_processada_uint8.ravel(), bins=256, range=(0, 256))
        plt.title("Histograma - Equalização")
        plt.show()

    return equalized_image


#####################################################################################################################
def converter_para_cinza(imagem):
    altura, largura = len(imagem), len(imagem[0])
    imagem_cinza = [[0 for _ in range(largura)] for _ in range(altura)]

    for i in range(altura):
        for j in range(largura):
            vermelho, verde, azul = imagem[i][j]
            cinza = int(0.299 * vermelho + 0.587 * verde + 0.114 * azul)
            imagem_cinza[i][j] = cinza

    return imagem_cinza

def calcular_media(bairro):
    soma = sum(bairro)
    return soma / len(bairro)

def calcular_desvio_padrao(bairro, media):
    soma_diferencas_quadradas = sum((x - media) ** 2 for x in bairro)
    return (soma_diferencas_quadradas / len(bairro)) ** 0.5

def aplicar_kernel(imagem, tamanho_kernel, funcao_filtro):
    altura, largura = len(imagem), len(imagem[0])
    imagem_saida = [[0 for _ in range(largura)] for _ in range(altura)]

    offset = tamanho_kernel // 2

    for i in range(offset, altura - offset):
        for j in range(offset, largura - offset):
            bairro = [imagem[i + x][j + y] for x in range(-offset, offset + 1) for y in range(-offset, offset + 1)]
            imagem_saida[i][j] = funcao_filtro(bairro)

    return imagem_saida

def realce_contraste_adaptativo(imagem, c, tamanho_kernel):
    def funcao_filtro(bairro):
        media_local = calcular_media(bairro)
        desvio_padrao_local = calcular_desvio_padrao(bairro, media_local)
        pixel_central = bairro[len(bairro) // 2]

        if desvio_padrao_local != 0:
            return int(media_local + c * (pixel_central - media_local) / desvio_padrao_local)
        else:
            return pixel_central

    # Primeiro, converte a imagem para escala de cinza
    imagem_cinza = converter_para_cinza(imagem)

    # Depois, aplica o realce de contraste adaptativo
    imagem_processada = aplicar_kernel(imagem_cinza, tamanho_kernel, funcao_filtro)
    return imagem_processada

#######################################################################################################



# Função para mudança de escala (scaling)
def scale_image(image, scale_x, scale_y, output_path):
    height, width = image.shape[:2]
    # Calculando o novo tamanho com base nos fatores de escala
    new_width = int(width * scale_x)
    new_height = int(height * scale_y)
    # Redimensionando a imagem
    scaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    # Salvando a imagem transformada
    cv2.imwrite(output_path, scaled_image)
    return scaled_image

def shear_image(image, shear_x, shear_y, output_path):
    rows, cols = image.shape[:2]

    # Matriz de transformação para cisalhamento
    M = np.float32([[1, shear_x, 0],
                    [shear_y, 1, 0],
                    [0, 0, 1]])

    # Aplicando a transformação
    sheared_image = cv2.warpPerspective(image, M, (cols, rows))
    cv2.imwrite(output_path, sheared_image)  # Salvando a imagem transformada
    return sheared_image
##############################################################################################

def reflect_image(image, axis, output_path):
    height = len(image)
    width = len(image[0]) if height > 0 else 0

    reflected_image = []

    # Refletir a imagem
    if axis == 0:  # Reflexão horizontal
        for row in image:
            reflected_row = row[::-1]
            reflected_image.append(reflected_row)
    elif axis == 1:  # Reflexão vertical
        reflected_image = image[::-1]

    # Converter para um array do NumPy
    np_image = np.array(reflected_image, dtype=np.uint8)

    # Salvar a imagem
    cv2.imwrite(output_path, np_image)

    return reflected_image

# Função para rotação (rotation)
def bilinear_interpolate(image, x, y):
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, image.shape[1] - 1), min(y1 + 1, image.shape[0] - 1)

    A = image[y1, x1]
    B = image[y1, x2]
    C = image[y2, x1]
    D = image[y2, x2]

    wa = (x2 - x) * (y2 - y)
    wb = (x - x1) * (y2 - y)
    wc = (x2 - x) * (y - y1)
    wd = (x - x1) * (y - y1)

    return wa*A + wb*B + wc*C + wd*D
def rotate_image2(image, angle, output_path, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    # Se nenhum centro for fornecido, usa o centro da imagem
    if center is None:
        center_x, center_y = w // 2, h // 2
    else:
        center_x, center_y = center

    # Matriz de rotação
    M = cv2.getRotationMatrix2D((center_x, center_y), angle, scale)

    # Cria uma nova imagem com o mesmo tamanho da original
    rotated_image = np.zeros_like(image)

    for y in range(h):
        for x in range(w):
            # Aplicar a transformação de rotação para cada pixel
            new_x = (M[0, 0] * x + M[0, 1] * y + M[0, 2])
            new_y = (M[1, 0] * x + M[1, 1] * y + M[1, 2])

            ## Verifica se as novas coordenadas estão dentro dos limites da nova imagem
            if 0 <= new_x < w - 1 and 0 <= new_y < h - 1:
                rotated_image[y, x] = bilinear_interpolate(image, new_x, new_y)
    cv2.imwrite(output_path, rotated_image)
    return rotated_image

def rotate_image(image, angle,output_path, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    # Se nenhum centro for fornecido, usa o centro da imagem
    if center is None:
        center_x, center_y = w // 2, h // 2
    else:
        center_x, center_y = center

    # Matriz de rotação
    M = cv2.getRotationMatrix2D((center_x, center_y), angle, scale)

    # Cria uma nova imagem com o mesmo tamanho da original
    rotated_image = np.zeros_like(image)

    for y in range(h):
        for x in range(w):
            # Aplicar a transformação de rotação para cada pixel
            new_x = (M[0, 0] * x + M[0, 1] * y + M[0, 2])
            new_y = (M[1, 0] * x + M[1, 1] * y + M[1, 2])

            # Verifica se as novas coordenadas estão dentro dos limites da nova imagem
            if 0 <= new_x < w and 0 <= new_y < h:
                rotated_image[int(new_y), int(new_x)] = image[y, x]
    cv2.imwrite(output_path, rotated_image)
    return rotated_image

def vertical_pinch(image, amount, output_path):
    rows, cols = image.shape[:2]
    # Criação do mapa de coordenadas para o pinch vertical
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            # Altera a coordenada y para criar o efeito de pinch
            map_x[i, j] = j
            map_y[i, j] = i + amount * np.sin(np.pi * j / cols)

    # Aplicando a transformação
    pinched_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(output_path, pinched_image)
    return pinched_image

import numpy as np
import cv2

import numpy as np
import cv2

def edge_pinch(image, amount, output_path):
    rows, cols = image.shape[:2]
    center_x, center_y = cols / 2, rows / 2
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            # Calcula a distância normalizada do pixel ao centro da imagem
            distance_x = (j - center_x) / center_x
            distance_y = (i - center_y) / center_y

            # Calcula um fator de escala baseado na distância e no amount
            scale_x = 1 - amount * distance_x**2
            scale_y = 1 - amount * distance_y**2

            # Aplica o fator de escala para ajustar os pixels em direção ao centro
            map_x[i, j] = center_x + (j - center_x) * scale_x
            map_y[i, j] = center_y + (i - center_y) * scale_y

    # Aplica a transformação de warping
    pinched_edges_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(output_path, pinched_edges_image)
    return pinched_edges_image


def field_based_warping(image, field, output_path):
    # Obtém o número de linhas e colunas da imagem
    rows, cols = image.shape[:2]

    # Inicializa os mapas de coordenadas para o warping
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    # Assegura que 'field' é uma matriz 2D com elementos sendo vetores (listas ou tuplas) de dois elementos
    for i in range(rows):
        for j in range(cols):
            displacement = field[i][j]  # Obtem o vetor de deslocamento para a posição (i, j)
            map_x[i, j] = j + displacement[0]  # Deslocamento em x
            map_y[i, j] = i + displacement[1]  # Deslocamento em y

    warped_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(output_path, warped_image)
    return warped_image

def aplicar_filtro_mediana(imagem, kernel_size, output_path):
    pad_size = kernel_size // 2
    altura, largura, canais = imagem.shape
    imagem_padded = np.pad(imagem, [(pad_size, pad_size), (pad_size, pad_size), (0, 0)], mode='edge')
    imagem_filtrada = np.zeros_like(imagem)

    # Preparando janelas para cada pixel
    janelas = np.lib.stride_tricks.as_strided(
        imagem_padded,
        shape=(altura, largura, kernel_size, kernel_size, canais),
        strides=imagem_padded.strides[:2] + imagem_padded.strides[:2] + imagem_padded.strides[2:]
    )

    # Calculando a mediana em todas as janelas de uma só vez
    medianas = np.median(janelas, axis=(2, 3))

    # Atribuindo os valores de mediana à imagem filtrada
    imagem_filtrada[:, :, :] = medianas

    cv2.imwrite(output_path, imagem_filtrada)
    return imagem_filtrada


def aplicar_filtro_media(imagem, kernel_size, output_path):
    kernel = np.ones((kernel_size, kernel_size), dtype=float) / (kernel_size**2)
    imagem_filtrada = np.zeros_like(imagem)

    for canal in range(imagem.shape[2]):
        imagem_filtrada[:, :, canal] = cv2.filter2D(imagem[:, :, canal], -1, kernel)

    cv2.imwrite(output_path, imagem_filtrada)
    return imagem_filtrada

def aplicar_sobel(imagem, output_path):
    # Converter para escala de cinza se for uma imagem colorida
    if imagem.ndim == 3:
        imagem = np.dot(imagem[...,:3], [0.2989, 0.5870, 0.1140])

    # Definindo os kernels de Sobel
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # Inicializando as matrizes de gradiente
    grad_x = np.zeros_like(imagem)
    grad_y = np.zeros_like(imagem)

    # Aplicando os kernels de Sobel
    for i in range(1, imagem.shape[0] - 1):
        for j in range(1, imagem.shape[1] - 1):
            regiao = imagem[i-1:i+2, j-1:j+2]
            grad_x[i, j] = np.sum(sobel_x * regiao)
            grad_y[i, j] = np.sum(sobel_y * regiao)

    # Calculando a magnitude do gradiente
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    magnitude = np.uint8(magnitude / np.max(magnitude) * 255)

    # Salvando a imagem resultante com OpenCV
    cv2.imwrite(output_path, magnitude)

    return magnitude