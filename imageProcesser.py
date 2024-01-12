from PIL import Image
import numpy as np
import cv2
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

def expand_histogram_auto(image, gain):
    # Aplica a expansão do histograma de forma automática
    expanded_image = np.copy(image)
    expanded_image = expanded_image * gain
    expanded_image[expanded_image < 0] = 0
    expanded_image[expanded_image > 255] = 255
    return expanded_image.astype(np.uint8)


def histogram_equalization(image):
    # Calcula o histograma da imagem
    hist, _ = np.histogram(image, bins=256, range=(0, 256))

    # Calcula a função de distribuição acumulada (CDF) do histograma
    cdf = hist.cumsum()

    # Normaliza a CDF para o intervalo [0, 255]
    cdf_normalized = ((cdf - cdf.min()) * 255) / (cdf.max() - cdf.min())

    # Aplica a equalização do histograma à imagem
    equalized_image = cdf_normalized[image]

    return equalized_image.astype(np.uint8)


def realce_contraste_adaptativo(imagem, c, tamanho_kernel):
    """
    Aplica realce de contraste adaptativo a uma imagem usando a fórmula exata fornecida.

    Parâmetros:
    - imagem: matriz numpy da imagem
    - c: parâmetro constante não negativo que controla a intensidade do aumento de contraste
    - tamanho_kernel: tamanho do bairro n x n para calcular a média e o desvio padrão

    Retorna:
    - imagem_processada: imagem após a aplicação do realce de contraste adaptativo
    """
    # Função a ser aplicada para cada bairro de pixels
    def funcao_filtro(bairro):
        # Calcular a média local e o desvio padrão
        media_local = np.mean(bairro)
        desvio_padrao_local = np.std(bairro)

        # Pixel central no bairro
        pixel_central = bairro[tamanho_kernel ** 2 // 2]

        # Aplicar a fórmula de realce de contraste
        if desvio_padrao_local != 0:
            return media_local + c * (pixel_central - media_local) / desvio_padrao_local
        else:
            return pixel_central

    # Converter imagem em escala de cinza se ainda não estiver
    if len(imagem.shape) > 2:
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        imagem_cinza = imagem

    # Aplicar a função de filtro a cada pixel usando uma janela móvel (kernel)
    imagem_processada = generic_filter(imagem_cinza, funcao_filtro, size=(tamanho_kernel, tamanho_kernel))

    return imagem_processada.astype(np.uint8)