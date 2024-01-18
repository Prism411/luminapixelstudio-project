import math

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


def dissolve_cruzado(image_path1, image_path2, output_path, alpha):
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
    contrast_stretched = Image.eval(image, lambda x: (x - 100) * 255 / (
                200 - 100) if 100 <= x <= 200 else 0 if x < 100 else 255)
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

    # Convertendo a lista de listas para um array do NumPy
    imagem_cinza_np = np.array(imagem_cinza, dtype=np.uint8)
    return imagem_cinza_np



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


import numpy as np
from PIL import Image
import os


def shear_image(image, shear_x, shear_y, output_path):
    print("entrou na shear Image")
    rows, cols = image.shape[:2]
    sheared_image = np.zeros_like(image)

    for i in range(rows):
        for j in range(cols):
            new_x = j + shear_x * i
            new_y = i + shear_y * j
            if 0 <= new_x < cols and 0 <= new_y < rows:
                sheared_image[int(new_y), int(new_x)] = image[i, j]

    # Convertendo para o tipo de dados correto, se necessário
    sheared_image = sheared_image.astype(np.uint8)

    # Verifique se o diretório existe, se não, crie-o
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    # Tente salvar a imagem
    try:
        Image.fromarray(sheared_image).save(output_path)
        cv2.imwrite(output_path, sheared_image)
        print(f"Imagem salva com sucesso em: {output_path}")
    except Exception as e:
        print(f"Erro ao salvar a imagem: {e}")
    print("teste")
    return sheared_image


# Restante do seu código...


def reflect_image(image, axis, output_path):
    height = len(image)
    width = len(image[0]) if height > 0 else 0

    # Refletir a imagem
    if axis == 0:  # Reflexão horizontal
        reflected_image = [row[::-1] for row in image]  # Compreensão de lista
    elif axis == 1:  # Reflexão vertical
        # Criar uma lista com espaço para cada linha
        reflected_image = [None] * height
        for i in range(height):
            reflected_image[i] = image[height - 1 - i]

    # Converter para um array do NumPy
    np_image = np.array(reflected_image, dtype=np.uint8)

    # Salvar a imagem
    cv2.imwrite(output_path, np_image)

    return np_image


# Função para rotação (rotation)
def bilinear_interpolate(im, x, y):
    x0, y0 = int(x), int(y)
    x1, y1 = min(x0 + 1, im.shape[1] - 1), min(y0 + 1, im.shape[0] - 1)

    # Calculando os coeficientes
    a = x - x0
    b = y - y0

    # Interpolação
    return (im[y0, x0] * (1 - a) * (1 - b) + im[y0, x1] * a * (1 - b) +
            im[y1, x0] * (1 - a) * b + im[y1, x1] * a * b)

def rotate_image2(image, angle, output_path, center=None, scale=1.0):
    image = converter_para_cinza(image)  # Converte para escala de cinza
    h, w = image.shape[:2]

    # Se nenhum centro for fornecido, usa o centro da imagem
    if center is None:
        center_x, center_y = w // 2, h // 2
    else:
        center_x, center_y = center

    # Convertendo o ângulo em radianos
    angle_rad = math.radians(angle)

    # Criando a imagem rotacionada
    rotated_image = np.zeros_like(image)

    for y in range(h):
        for x in range(w):
            # Calculando as novas coordenadas com base no centro e no ângulo
            new_x = (x - center_x) * math.cos(angle_rad) + (y - center_y) * math.sin(angle_rad) + center_x
            new_y = -(x - center_x) * math.sin(angle_rad) + (y - center_y) * math.cos(angle_rad) + center_y

            # Verificando se as novas coordenadas estão dentro dos limites da imagem original
            if 0 <= new_x < w and 0 <= new_y < h:
                rotated_image[y, x] = bilinear_interpolate(image, new_x, new_y)

    # Salvando a imagem rotacionada
    Image.fromarray(rotated_image).save(output_path)
    return rotated_image

def rotate_image(image, angle, output_path, center=None, scale=1.0):
    h, w = image.shape[:2]
    image = converter_para_cinza(image)
    # Se nenhum centro for fornecido, usa o centro da imagem
    if center is None:
        center_x, center_y = w // 2, h // 2
    else:
        center_x, center_y = center

    # Convertendo o ângulo em radianos
    angle_rad = math.radians(angle)

    # Calculando os componentes da matriz de rotação
    cos_a = math.cos(angle_rad) * scale
    sin_a = math.sin(angle_rad) * scale

    # Criando a nova imagem
    rotated_image = np.zeros_like(image)

    for y in range(h):
        for x in range(w):
            # Aplicando a transformação de rotação para cada pixel
            new_x = cos_a * (x - center_x) - sin_a * (y - center_y) + center_x
            new_y = sin_a * (x - center_x) + cos_a * (y - center_y) + center_y

            # Verificando se as novas coordenadas estão dentro dos limites da nova imagem
            if 0 <= new_x < w and 0 <= new_y < h:
                rotated_image[int(new_y), int(new_x)] = image[y, x]

    # Salvando a imagem rotacionada
    Image.fromarray(rotated_image).save(output_path)
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
            scale_x = 1 - amount * distance_x ** 2
            scale_y = 1 - amount * distance_y ** 2

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

    for i in range(altura):
        for j in range(largura):
            for c in range(canais):
                # Extraia a janela em torno do pixel (i, j)
                janela = imagem_padded[i:i + kernel_size, j:j + kernel_size, c]

                # Calcule a mediana na mão
                valor_mediana = calcular_mediana(janela)
                imagem_filtrada[i, j, c] = valor_mediana

    # Salvar a imagem filtrada
    Image.fromarray(imagem_filtrada).save(output_path)
    return imagem_filtrada
def calcular_mediana(janela):
    # Achate a janela e ordene os valores
    valores_ordenados = np.sort(janela.flatten())
    # Calcule o índice da mediana
    meio = len(valores_ordenados) // 2

    # Se o número de elementos for ímpar, retorne o valor do meio
    if len(valores_ordenados) % 2 != 0:
        return valores_ordenados[meio]
    # Se for par, retorne a média dos dois valores centrais
    else:
        return (valores_ordenados[meio - 1] + valores_ordenados[meio]) / 2


def aplicar_filtro_media(imagem, kernel_size, output_path):
    pad_size = kernel_size // 2
    altura, largura, canais = imagem.shape

    # Padding na imagem para lidar com as bordas
    imagem_padded = np.pad(imagem, [(pad_size, pad_size), (pad_size, pad_size), (0, 0)], mode='constant', constant_values=0)
    imagem_filtrada = np.zeros_like(imagem)

    # Fator de normalização para o kernel
    fator_normalizacao = kernel_size ** 2

    for i in range(altura):
        for j in range(largura):
            for c in range(canais):
                # Extraia a janela em torno do pixel (i, j)
                janela = imagem_padded[i:i + kernel_size, j:j + kernel_size, c]

                # Calcule a média dos valores da janela
                valor_medio = np.sum(janela) / fator_normalizacao
                imagem_filtrada[i, j, c] = valor_medio

    # Salvar a imagem filtrada
    Image.fromarray(imagem_filtrada).save(output_path)
    return imagem_filtrada


import numpy as np
import cv2
from PIL import Image

def aplicar_sobel(imagem, output_path):
    # Converter para escala de cinza se for uma imagem colorida
    if imagem.ndim == 3:
        imagem = np.dot(imagem[..., :3], [0.2989, 0.5870, 0.1140])

    # Definindo os kernels de Sobel
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # Inicializando as matrizes de gradiente
    altura, largura = imagem.shape
    grad_x = np.zeros_like(imagem)
    grad_y = np.zeros_like(imagem)

    # Aplicando os kernels de Sobel
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            soma_x = soma_y = 0
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    soma_x += sobel_x[ki + 1][kj + 1] * imagem[i + ki, j + kj]
                    soma_y += sobel_y[ki + 1][kj + 1] * imagem[i + ki, j + kj]
            grad_x[i, j] = soma_x
            grad_y[i, j] = soma_y

    # Calculando a magnitude do gradiente
    magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
    magnitude = np.uint8(magnitude / magnitude.max() * 255)

    # Salvando a imagem resultante com OpenCV
    cv2.imwrite(output_path, magnitude)

    return magnitude


#converter_para_cinza(imagem)
def agucamento_bordas(imagem, output_path):
    imagem_gray = converter_para_cinza(imagem)
    altura, largura = imagem_gray.shape
    imagem_agucada = np.zeros_like(imagem_gray)

    # Kernel Laplaciano
    kernel_laplaciano = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]

    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            soma = 0
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    soma += imagem_gray[i + ki, j + kj] * kernel_laplaciano[ki + 1][kj + 1]

            # Adicionando as bordas detectadas de volta à imagem original
            valor_agucado = imagem_gray[i, j] + soma
            # Garantindo que os valores estejam dentro dos limites [0, 255]
            imagem_agucada[i, j] = min(max(valor_agucado, 0), 255)

    # Salvando a imagem resultante
    Image.fromarray(imagem_agucada).save(output_path)

    return imagem_agucada


def high_boost(imagem, k, output_path):
    imagem_gray = converter_para_cinza(imagem)
    altura, largura = len(imagem_gray), len(imagem_gray[0])
    imagem_boosted = [[0 for _ in range(largura)] for _ in range(altura)]

    # Kernel Laplaciano
    kernel_laplaciano = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]

    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            soma_laplaciana = 0
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    soma_laplaciana += imagem_gray[i + ki][j + kj] * kernel_laplaciano[ki + 1][kj + 1]

            # Aplicar o high boost
            valor_boosted = imagem_gray[i][j] + k * soma_laplaciana

            # Verificar os limites e ajustar se necessário
            if valor_boosted < 0:
                valor_boosted = 0
            elif valor_boosted > 255:
                valor_boosted = 255

            imagem_boosted[i][j] = valor_boosted

    # Convertendo de volta para o array do NumPy para salvar a imagem
    imagem_boosted_np = np.array(imagem_boosted, dtype=np.uint8)
    Image.fromarray(imagem_boosted_np).save(output_path)
    return imagem_boosted_np


def convolucao_com_offset(imagem, kernel, offset, output_path):
    # Converte a imagem para escala de cinza para simplificar a convolução.
    imagem_gray = converter_para_cinza(imagem)
    k_altura, k_largura = len(kernel), len(kernel[0])
    pad_altura, pad_largura = k_altura // 2, k_largura // 2

    # Inicializa a imagem de saída
    altura, largura = len(imagem_gray), len(imagem_gray[0])
    imagem_saida = [[0] * largura for _ in range(altura)]

    # Aplica a operação de convolução
    for i in range(pad_altura, altura - pad_altura):
        for j in range(pad_largura, largura - pad_largura):
            conv_sum = 0
            for m in range(k_altura):
                for n in range(k_largura):
                    conv_sum += (imagem_gray[i + m - pad_altura][j + n - pad_largura] *
                                 kernel[m][n])
            conv_sum += offset
            # Garante que os valores da imagem estão dentro dos limites [0, 255]
            conv_sum = max(min(conv_sum, 255), 0)
            imagem_saida[i][j] = conv_sum

    # Convertendo de volta para o array do NumPy para salvar a imagem
    imagem_saida_np = np.array(imagem_saida, dtype=np.uint8)
    Image.fromarray(imagem_saida_np).save(output_path)

    return imagem_saida_np