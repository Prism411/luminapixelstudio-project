# ==============================================================================
# Nome do Projeto: LuminaPixelStudio
# Autor: Jáder Louis @Prism411, Nataly Tobias @natalytobias
# Data de Criação: 10/01/2024
#
# Estrutura do Projeto:
#   - interfaceMenu: O arquivo principal que executa o programa.
#   - imageProcesser: Módulo responsável pelas funções de processamento de Imagem.
#   - luminaProcessing/: Diretório que salva as imagens processadas.
#   - icons/: Guarda os Icones utilizados no projeto.
#   - docs/: Documentação do projeto.
#   - scripts/: Funções em octave que foram base para o aplicativo.
#   - imagensComparacao/: Deve ser ignorada, existem apenas para repassar informações da Q.2
#   - questao2: o modulo "questao2.py" deve ser ignorado pois é apenas para realizar a Q.2
#
# Notas Adicionais:
#   Aqui é o modulo responsavel por realizar a segunda questão do projeto.
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from imageProcesser import converter_para_cinza
from interfaceMenu import imageTransform


def convolucao_com_offset(imagem, kernel, offset):
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

    # Convertendo para o array do NumPy e exibindo a imagem
    imagem_saida_np = np.array(imagem_saida, dtype=np.uint8)
    plt.imshow(imagem_saida_np, cmap='gray')
    plt.show()

#definição de mascara de matriz do filtro de aguçamento
def sharpness_filter(c,d):
    return[
        [-c, -c, -c],
        [-c, 8*c + d, -c],
        [-c, -c, -c]
    ]

#definição de mascara primeira versão da matriz de filtro de relevo
def emboss_filter_one():
    return[
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, -1]
    ]

#definição de mascara da segunda versão da matriz de filtro de relevo
def emboss_filter_two():
    return[
        [0, 0, 2],
        [0, -1, 0],
        [-1, 0, 0]
    ]

#definição de mascara da matriz do filtro de detecção de bordas
def deteccao_bordas():
    return[
        [0, -1, 0],
        [-1, -4, -1],
        [0, -1, 0]
    ]

image =  imageTransform("luminaprocessing/image_1.png")
offset = 1
convolucao_com_offset(image, sharpness_filter(1,1), offset)
convolucao_com_offset(image, emboss_filter_one(), offset)
convolucao_com_offset(image, emboss_filter_two(), offset)
convolucao_com_offset(image, deteccao_bordas(), offset)
