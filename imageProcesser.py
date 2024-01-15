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

def reflect_image(image, axis):
    # axis = 0 para reflexão horizontal, 1 para vertical
    return cv2.flip(image, axis)

# Função para rotação (rotation)
def rotate_image(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)

    # Matriz de rotação
    M = cv2.getRotationMatrix2D(center, angle, scale)

    # Aplicando a rotação
    rotated_image = cv2.warpAffine(image, M, (w, h))
    return rotated_image

def vertical_pinch(image, amount):
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
    return pinched_image

def edge_pinch(image, amount):
    rows, cols = image.shape[:2]
    # Criação do mapa de coordenadas para o pinch nas bordas
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            # Altera as coordenadas para criar o efeito de pinch nas bordas
            offset_x = abs(cols/2 - j) / (cols/2) * amount
            offset_y = abs(rows/2 - i) / (rows/2) * amount
            map_x[i, j] = j + offset_x
            map_y[i, j] = i + offset_y

    # Aplicando a transformação
    pinched_edges_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return pinched_edges_image

def field_based_warping(image, field):
    rows, cols = image.shape[:2]
    # Criação do mapa de coordenadas para o warping baseado em campos
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            # Altera as coordenadas com base no campo de vetores
            map_x[i, j] = j + field[i, j][0]
            map_y[i, j] = i + field[i, j][1]

    # Aplicando a transformação
    warped_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return warped_image

# Note que para a função field_based_warping, você precisará fornecer um 'campo' apropriado,
# que é um array de vetores indicando como cada pixel deve ser movido.
def vertical_pinch(image, amount):
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
    return pinched_image

def edge_pinch(image, amount):
    rows, cols = image.shape[:2]
    # Criação do mapa de coordenadas para o pinch nas bordas
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            # Altera as coordenadas para criar o efeito de pinch nas bordas
            offset_x = abs(cols/2 - j) / (cols/2) * amount
            offset_y = abs(rows/2 - i) / (rows/2) * amount
            map_x[i, j] = j + offset_x
            map_y[i, j] = i + offset_y

    # Aplicando a transformação
    pinched_edges_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return pinched_edges_image

def field_based_warping(image, field):
    rows, cols = image.shape[:2]
    # Criação do mapa de coordenadas para o warping baseado em campos
    map_x = np.zeros((rows, cols), dtype=np.float32)
    map_y = np.zeros((rows, cols), dtype=np.float32)

    for i in range(rows):
        for j in range(cols):
            # Altera as coordenadas com base no campo de vetores
            map_x[i, j] = j + field[i, j][0]
            map_y[i, j] = i + field[i, j][1]

    # Aplicando a transformação
    warped_image = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return warped_image

# Note que para a função field_based_warping, você precisará fornecer um 'campo' apropriado,
# que é um array de vetores indicando como cada pixel deve ser movido.
def plot_histogram(image):
    hist, bins = np.histogram(image, bins=256, range=(0, 256))
    plt.figure()
    plt.title("Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.plot(hist, color="black")
    plt.xlim([0, 256])
    plt.show()