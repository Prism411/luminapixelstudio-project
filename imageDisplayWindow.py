import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

import cv2
import numpy as np
from PIL import ImageTk, Image
import customtkinter
from imageProcesser import dissolve_cruzado, dissolve_cruzado_nao_uniforme, redimensionar_imagem, negativo, \
    alargamento_contraste, limiarizacao, transformacao_potencia, transformacao_logaritmica, scale_image, \
    realce_contraste_adaptativo, histogram_equalization, expand_histogram_auto, reflect_image, rotate_image, \
    rotate_image2, field_based_warping, edge_pinch, vertical_pinch, aplicar_filtro_media, aplicar_filtro_mediana, \
    aplicar_sobel, agucamento_bordas, high_boost, convolucao_com_offset, shear_image


class ImageDisplayWindow(customtkinter.CTkToplevel):

    def __init__(self, parent, imagepath, image):

        super().__init__(parent)

        # Definir o modo de aparência e o tema de cor
        customtkinter.set_appearance_mode("dark")  # Outras opções: "light", "System"
        customtkinter.set_default_color_theme("dark-blue")  # Outras opções de temas disponíveis na documentação

        self.imagepath = imagepath
        self.title("Imagem Selecionada")
        self.geometry("920x720")  # Tamanho da nova janela
        self.resizable(False, False)  # Bloqueie a capacidade de redimensionar a janela
        self.configure(bg="#202225")

        # Configurações para redimensionamento e moldura
        canvas_width, canvas_height = 256, 256
        frame_width = 10
        frame_color = "black"

        # Cria um Canvas para a imagem
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg="gray")
        self.canvas.place(x=(920 - canvas_width) // 2, y=(20))

        # Calcula as posições para a imagem e a moldura
        image_width = image.width()
        image_height = image.height()
        x_position = (canvas_width - image_width) // 2
        y_position = (canvas_height - image_height) // 2

        # Desenha a moldura no Canvas
        self.canvas.create_rectangle(
            x_position - frame_width,
            y_position - frame_width,
            x_position + image_width + frame_width,
            y_position + image_height + frame_width,
            outline=frame_color, width=frame_width * 2
        )

        # Coloca a imagem no Canvas
        self.canvas.create_image(x_position, y_position, image=image, anchor='nw')
        # Mantém uma referência à imagem
        self.image = image

        # Botão para selecionar uma imagem
        self.select_image_button = tk.Button(self, text="Selecionar Cruzada", command=self.select_image)
        self.select_image_button.pack()
        self.select_image_button.place(x=400, y=320)

        # Variável para rastrear a escolha do usuário
        self.selected_operation = tk.StringVar(value="None")
        self.operationReso = tk.StringVar(value="None")

        # Botões de opção para Dissolve Cruzado
        self.dissolve_cruzado_button = tk.Radiobutton(self, text="Dissolve Cruzado", variable=self.selected_operation, value="Dissolve Cruzado")
        self.dissolve_cruzado_button.pack()
        self.dissolve_cruzado_button.place(x=340, y=294)

        # Botões de opção para Dissolve Cruzado Não-Uniforme
        self.dissolve_cruzado_nao_uniforme_button = tk.Radiobutton(self, text="Dissolve Cruzado N.U.", variable=self.selected_operation, value="Dissolve Cruzado N.U.")
        self.dissolve_cruzado_nao_uniforme_button.pack()
        self.dissolve_cruzado_nao_uniforme_button.place(x=460, y=294)

        # Combobox para selecionar um valor alpha
        self.alpha_values = ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]
        self.alpha_combobox = ttk.Combobox(self, values=self.alpha_values)
        self.alpha_combobox.set("0.5")  # Defina o valor padrão como 0.5
        self.alpha_combobox.pack()
        self.alpha_combobox.place(x=550, y=320)
        selected_alpha = self.alpha_combobox.get()
        print(f"Valor selecionado em alpha_combobox: {selected_alpha}")

        # Cria um widget para exibir a imagem selecionada
        self.selected_image_label = tk.Label(self, text="imagem", fg="#202225", bg="#202225")
        self.selected_image_label.pack()
        self.selected_image_label.place(x=630, y=20)

        # Variável para rastrear a escolha do usuário
        self.selected_operation = tk.StringVar()
        self.selected_operation.set("Transformação de Intensidade:")  # Defina o valor inicial

        # Combobox para selecionar uma operação
        self.operations_combobox = ttk.Combobox(self, textvariable=self.selected_operation)
        self.operations_combobox['values'] = (
            "Alargamento de Contraste",
            "Negativo",
            "Limiarização",
            "Transformação de Potência",
            "Transformação Logarítmica"
        )
        self.operations_combobox.pack()
        self.operations_combobox.place(x=200, y=360)
        self.operations_combobox.bind("<<ComboboxSelected>>", self.show_value_input)

        # Rótulo para descrever o campo de entrada de valor
        self.value_label = tk.Label(self, text="Valor:")
        self.value_label.pack()
        self.value_label.place(x=330, y=360)

        # Campo de entrada para o valor
        self.value_entry = tk.Entry(self)
        self.value_entry.pack()
        self.value_entry.place(x=370, y=360)

        # Inicialmente oculta o campo de entrada e o rótulo
        self.value_entry.place_forget()
        self.value_label.place_forget()
        output_path = "luminaprocessing/resultado.png"
        # Adicione o botão Processar
        self.process_button = tk.Button(self, text="Processar", command=self.process_image)
        self.process_button.pack()
        self.process_button.place(x=600, y=360)


        # Adicione o botão Equalização
        self.equal_button = tk.Button(self, text="Equalização Histograma", command=self.equali_hist)
        self.equal_button.pack()
        self.equal_button.place(x=200, y=390)
        # Crie um rótulo para a palavra "Ganho"
        label = tk.Label(self, text="Ganho:")
        label.pack()
        label.place(x=490, y=392)
        #Label de Valor para Ganho
        self.gain_entry = tk.Entry(self)
        self.gain_entry.pack()
        self.gain_entry.place(x=550, y=392)
        # Adicione o botão expansão
        self.expansion_button = tk.Button(self, text="Expansão Histograma", command=self.expansion_hist)
        self.expansion_button.pack()
        self.expansion_button.place(x=350, y=390)


        # Crie um rótulo para a palavra "Constante C"
        label = tk.Label(self, text="Constante C:")
        label.pack()
        label.place(x=200, y=422)
        #Label de Valor para Constante C
        self.c_constant_entry = tk.Entry(self)
        self.c_constant_entry.pack()
        self.c_constant_entry.place(x=280, y=422)
        # Crie um rótulo para a palavra "Vizinhança NxN"
        label = tk.Label(self, text="Vizinhança NxN:")
        label.pack()
        label.place(x=410, y=422)
        #Label de Valor para Vizinhança NxN
        self.nxn_entry = tk.Entry(self)
        self.nxn_entry.pack()
        self.nxn_entry.place(x=510, y=422)
        # Adicione o botão controleConstraste
        self.expansion_button = tk.Button(self, text="Controle Contraste", command=self.ctrl_contraste)
        self.expansion_button.pack()
        self.expansion_button.place(x=640, y=420)
        # Botao de Aviso de Desempenho
        # Crie um rótulo para a Resolução Y"
        label = tk.Label(self, text="Pode demorar um pouco!",fg="red")
        label.pack()
        label.place(x=760, y=420)

        # Combobox para selecionar uma operação
        self.operationSC = tk.StringVar()
        self.reso_combobox = ttk.Combobox(self, textvariable=self.operationSC)
        self.reso_combobox['values'] = ("Scaling", "Cisalhamento")
        self.reso_combobox.pack()
        self.reso_combobox.place(x=200, y=450)
        self.reso_combobox.bind("<<ComboboxSelected>>", self.reso_operation)  # Remova os parênteses

        # Crie um rótulo para a Resolução X"
        label = tk.Label(self, text="Resolucão X:")
        label.pack()
        label.place(x=345, y=450)
        #Label de Valor para Resolucao X
        self.resX_entry = tk.Entry(self)
        self.resX_entry.pack()
        self.resX_entry.place(x=420, y=450)
        # Crie um rótulo para a Resolução Y"
        label = tk.Label(self, text="Resolucão Y:")
        label.pack()
        label.place(x=550, y=450)
        #Label de Valor para Resolucao Y
        self.resY_entry = tk.Entry(self)
        self.resY_entry.pack()
        self.resY_entry.place(x=625, y=450)
        # Crie um rótulo para o aviso de perigo
        label = tk.Label(self, text="Cuidado ao usar valores > 1.0", fg="red")
        label.pack()
        label.place(x=755, y=450)

    # Refletir Imagem
    # Variável para rastrear a escolha do usuário
        self.selOPR = tk.StringVar(value="None")
        self.operationReso = tk.StringVar(value="None")
        # Botões de opção para Inverte Horizontal
        self.invertH = tk.Radiobutton(self, text="Inverte Horizontal", variable=self.selOPR,value="ih",command=self.invert_operation)
        self.invertH.pack()
        self.invertH.place(x=20, y=50)

        # Botões de opção para Inverte Vertical
        self.invertV= tk.Radiobutton(self, text="Inverte Vertical",variable=self.selOPR,value="iv",command=self.invert_operation)
        self.invertV.pack()
        self.invertV.place(x=160, y=50)
    #Fim de Refletir a Imagem



    #Rotação
        # Crie um rótulo para a palavra "Rotaçao da Imagem"
        label = tk.Label(self, text="Angulo para Rotaçao")
        label.pack()
        label.place(x=20, y=80)
        #Label de Valor para Rotação
        self.rot_entry = tk.Entry(self)
        self.rot_entry.pack()
        self.rot_entry.place(x=20, y=110)
        # Adicione o botão Rotacao
        self.rot_button = tk.Button(self, text="Rotacionar", command=self.rota_operation)
        self.rot_button.pack()
        self.rot_button.place(x=150, y=80)
        # Adicione o botão Rotacao 2
        self.rot2_button = tk.Button(self, text="Rotacionar 2", command=self.rota_operation2)
        self.rot2_button.pack()
        self.rot2_button.place(x=150, y=110)
        # Crie um rótulo para o aviso de perigo
        label = tk.Label(self, text="Rotacao 2 é a rotação com Interpolação Bilinear\n PODE DEMORAR DEPENDENDO DO PC!", fg="red")
        label.pack()
        label.place(x=20, y=140)
        #FIM DA ROTAÇÃO##################################



        #######começo Warping e Pinch##############################################
        # Variável para rastrear a escolha do usuário
        self.selected_opr_pinch_warp = tk.StringVar()
        self.selected_opr_pinch_warp.set("Escolha Warp/Pinch!")
        # Combobox para selecionar uma operação
        self.opr_warp_pinch_combobox = ttk.Combobox(self, textvariable=self.selected_opr_pinch_warp)
        self.opr_warp_pinch_combobox['values'] = (
            "Pínch Vertical",
            "Pinch nas Bordas",
            "Warping Baseado em Campo"
        )
        self.opr_warp_pinch_combobox.pack()
        self.opr_warp_pinch_combobox.place(x=200, y=480)
        self.opr_warp_pinch_combobox.bind("<<ComboboxSelected>>", self.show_value_input)
        # Crie um rótulo para a palavra "Quantidade"
        label = tk.Label(self, text="Quantidade")
        label.pack()
        label.place(x=350, y=480)
        #Label de Valor de entrada para Amount
        self.amountWarpingPinch_entry = tk.Entry(self)
        self.amountWarpingPinch_entry.pack()
        self.amountWarpingPinch_entry.place(x=430, y=480)
        # Adicione o botão Processar
        self.warpingPinch_button = tk.Button(self, text="Processar", command=self.warpingPinch_operation)
        self.warpingPinch_button.pack()
        self.warpingPinch_button.place(x=560, y=480)
        #FIM DO WARPING E DO PINCH##########################################


        ##COMEÇO DA FILTRAGEM LINEAR EN NAO LINEAR MEDIA E MEDIANA######################
        # Variável para rastrear a escolha do usuário
        self.selected_filter = tk.StringVar()
        self.selected_filter.set("Escolha tipo de Filtro!")
        # Combobox para selecionar uma operação
        self.opr_warp_pinch_combobox = ttk.Combobox(self, textvariable= self.selected_filter)
        self.opr_warp_pinch_combobox['values'] = (
            "Filtro Media",
            "Filtro Mediana",
        )
        self.opr_warp_pinch_combobox.pack()
        self.opr_warp_pinch_combobox.place(x=200, y=510)
        # Crie um rótulo para a palavra "Tamanho do Kernel"
        label = tk.Label(self, text="Tamanho do Kernel")
        label.pack()
        label.place(x=350, y=510)
        #Label de Valor de entrada para KernelSize
        self.kernel_entry = tk.Entry(self)
        self.kernel_entry.pack()
        self.kernel_entry.place(x=470, y=510)
        # botao para realizar a operacao em si
        self.filter_button = tk.Button(self, text="Processar", command=self.filter_operation)
        self.filter_button.pack()
        self.filter_button.place(x=600, y=510)
        # Crie um rótulo para o aviso de perigo
        label = tk.Label(self, text="Mediana é Intensiva de CPU, Cuidado!", fg="red")
        label.pack()
        label.place(x=670, y=510)
        #Fim da Media e Mediana#############################

        ##Comeco da Deteccao de bordas############################
        self.sobel_button = tk.Button(self, text="Gradiente de Sobel;", command=self.sobel_operation)
        self.sobel_button.pack()
        self.sobel_button.place(x=200, y=540)
        ##Fim da Deteccao de Bordas#########################################
        ##Agucamento de bordas#############################################
        self.agcBordas_button = tk.Button(self, text="Aguçamento de Bordas;", command=self.algc_operation)
        self.agcBordas_button.pack()
        self.agcBordas_button.place(x=320, y=540)
        ##Fim do agucamento de bordas#############################################
        ##High Boost#######################################################################
        # Crie um rótulo para a palavra "Tamanho do Kernel"
        label = tk.Label(self, text="Valor de K:")
        label.pack()
        label.place(x=550, y=540)
        # Label de Valor de entrada para HighBoost
        self.high_boost_entry = tk.Entry(self)
        self.high_boost_entry.pack()
        self.high_boost_entry.place(x=620, y=540)
        # Botao de entrada para HighBoost
        self.highboost_button = tk.Button(self, text="Processar HighBoost", command=self.highboost_operation)
        self.highboost_button.pack()
        self.highboost_button.place(x=750, y=540)

        # Botao de entrada para Inserir Matriz HxN
        self.filter_button = tk.Button(self, text="Inserir Matriz H (N x M)", command=self.inserir_matriz)
        self.filter_button.pack()
        self.filter_button.place(x=200, y=570)

        # Crie um rótulo para a palavra "OFFSET"
        label = tk.Label(self, text="Valor de OffSet:")
        label.pack()
        label.place(x=350, y=570)

        # Label de Valor de entrada para OFFSET
        self.offset_entry = tk.Entry(self)
        self.offset_entry.pack()
        self.offset_entry.place(x=450, y=570)
        self.matriz = None

        # Botao de entrada para processar
        self.convo_button = tk.Button(self, text="Processar Convolução", command=self.convo_operation)
        self.convo_button.pack()
        self.convo_button.place(x=580, y=570)





    def convo_operation(self):
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte  de RGB para BGR
        output_path = "luminaprocessing/resultado.png"
        kernel = np.array(self.matriz)
        offset = int(self.offset_entry.get())
        convolucao_com_offset(imageInput, kernel, offset, output_path)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência
###COMEÇA FUNÇOES DE CONTROLE AQUI############################################################
    def inserir_matriz(self):
        # Criar uma nova janela
        self.janela_matriz = tk.Toplevel(self)
        self.janela_matriz.title("Inserir Matriz")

        # Entradas para as dimensões da matriz (n x m)
        self.entrada_n = tk.Entry(self.janela_matriz, width=5)
        self.entrada_n.grid(row=0, column=1)
        self.entrada_m = tk.Entry(self.janela_matriz, width=5)
        self.entrada_m.grid(row=1, column=1)

        tk.Label(self.janela_matriz, text="Linhas (n):").grid(row=0, column=0)
        tk.Label(self.janela_matriz, text="Colunas (m):").grid(row=1, column=0)

        # Botão para criar as entradas da matriz
        botao_criar = tk.Button(self.janela_matriz, text="Criar Matriz", command=self.criar_campos_matriz)
        botao_criar.grid(row=2, column=1)

        # Lista para armazenar as entradas (widgets Entry)
        self.entradas_matriz = []

    def criar_campos_matriz(self):
        # Limpando entradas anteriores
        for linha in self.entradas_matriz:
            for entrada in linha:
                entrada.destroy()
        self.entradas_matriz.clear()

        try:
            n = int(self.entrada_n.get())
            m = int(self.entrada_m.get())
            max_altura, max_largura = 3, 3  #
            if n > max_altura or m > max_largura:
                messagebox.showwarning("Tamanho Inválido",
                                       f"O tamanho do kernel deve ser no máximo {max_altura}x{max_largura}.")
                return
        except ValueError:
            messagebox.showerror("Entrada Inválida", "Por favor, insira números inteiros para as dimensões.")
            return

        # Criando campos de entrada para a matriz
        for i in range(n):
            linha = []
            for j in range(m):
                entrada = tk.Entry(self.janela_matriz, width=5)
                entrada.grid(row=i + 3, column=j)
                linha.append(entrada)
            self.entradas_matriz.append(linha)

        # Botão para obter os valores da matriz
        botao_obter = tk.Button(self.janela_matriz, text="Obter Matriz", command=self.obter_valores_matriz)
        botao_obter.grid(row=n + 3, columnspan=m)

    def obter_valores_matriz(self):
        try:
            self.matriz = [[float(entrada.get()) for entrada in linha] for linha in self.entradas_matriz]
            print("Matriz:", self.matriz)
        except ValueError:
            print("Por favor, insira apenas números.")
            self.matriz = None

    def highboost_operation(self):
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte  de RGB para BGR
        output_path = "luminaprocessing/resultado.png"
        k = int(serlf.high_boost_entry.get())
        if k >= 256:
            k = 255
        high_boost(imageInput, k, output_path)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência
    def algc_operation(self):
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte  de RGB para BGR
        output_path = "luminaprocessing/resultado.png"
        agucamento_bordas(imageInput, output_path)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência
    def sobel_operation(self):
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte  de RGB para BGR
        output_path = "luminaprocessing/resultado.png"
        aplicar_sobel(imageInput, output_path)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência
    def filter_operation(self):
        opr = str(self.selected_filter.get())
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        output_path = "luminaprocessing/resultado.png"
        kernel_size = int(self.kernel_entry.get())
        if opr == "Filtro Media":
            aplicar_filtro_media(imageInput, kernel_size, output_path)
            pass
        if opr == "Filtro Mediana":
            aplicar_filtro_mediana(imageInput, kernel_size,output_path)
            pass
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def warpingPinch_operation(self):
        opr = str(self.selected_opr_pinch_warp.get())
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        output_path = "luminaprocessing/resultado.png"

        if opr == "Pínch Vertical":
            amount = int(self.amountWarpingPinch_entry.get())
            vertical_pinch(imageInput, amount, output_path)
        if opr == "Pinch nas Bordas":
            amount = float(self.amountWarpingPinch_entry.get())
            edge_pinch(imageInput, amount, output_path)
        if opr == "Warping Baseado em Campo":
            amount = int(self.amountWarpingPinch_entry.get())
            rows, cols = imageInput.shape[:2]
            field = [[[0, 0] for _ in range(cols)] for _ in range(rows)]
            center_x, center_y = cols / 2, rows / 2
            for i in range(rows):
                for j in range(cols):
                    distance_to_center = np.sqrt((center_x - j) ** 2 + (center_y - i) ** 2)
                    scale = (1 - distance_to_center / max(center_x, center_y)) * amount
                    field[i][j] = [scale * (center_x - j), scale * (center_y - i)]
            field_based_warping(imageInput, field, output_path)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def rota_operation2(self):
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        angle = int(self.rot_entry.get())
        output_path = "luminaprocessing/resultado.png"
        rotate_image2(imageInput, angle, output_path, center=None, scale=1.0)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência
    def rota_operation(self):
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        angle = int(self.rot_entry.get())
        output_path = "luminaprocessing/resultado.png"
        rotate_image(imageInput, angle, output_path, center=None, scale=1.0)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência
    def invert_operation(self):
        output_path = self.imagepath
        operation = str(self.selOPR.get())
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        if operation == "iv":
            reflect_image(imageInput, 1, output_path)

        if operation == "ih":
            reflect_image(imageInput, 0, output_path)


        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def reso_operation(self, event):
        operation = self.operationSC.get()
        scale_x, scale_y = float(self.resX_entry.get()), float(self.resY_entry.get())
        # Converter a imagem do Tkinter (PhotoImage) para o formato do OpenCV
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        output_path = "luminaprocessing/resultado.png"

        if operation == "Scaling":
            scale_image(imageInput, scale_x, scale_y, output_path)
        if operation == "Cisalhamento": #Cisalhamento
            shear_image(imageInput, scale_x, scale_y, output_path)

        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def ctrl_contraste(self):
        #realce_contraste_adaptativo(imagem, c, tamanho_kernel, output_path)
        tamanho_kernel = int(self.nxn_entry.get())
        c = float(self.c_constant_entry.get())
        output_path = "luminaprocessing/resultado.png"
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        result = realce_contraste_adaptativo(imageInput, c, tamanho_kernel)
        imagem_final = Image.fromarray(np.array(result, dtype=np.uint8))
        imagem_final.save(output_path)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def equali_hist(self):
        output_path = "luminaprocessing/resultado.png"
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        histogram_equalization(imageInput, output_path,True)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def expansion_hist(self):
        output_path = "luminaprocessing/resultado.png"
        gain = int(self.gain_entry.get())
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        expand_histogram_auto(imageInput,gain,output_path,True)
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência


        print("teste")
    def process_image(self):
        # Obtém a operação selecionada e o valor, se necessário
        operation = self.selected_operation.get()
        value = self.value_entry.get() if self.value_entry['state'] != 'disabled' else None
        output_path = "luminaprocessing/resultado.png"
        # Chama a função correspondente baseada na operação selecionada
        if operation == "Negativo":
            negativo(self.imagepath, output_path)
        elif operation == "Alargamento de Contraste":
            alargamento_contraste(self.imagepath, output_path)
        elif operation == "Limiarização":
            limiarizacao(self.imagepath, output_path, float(value))
        elif operation == "Transformação de Potência":
            transformacao_potencia(self.imagepath, output_path, float(value))
        elif operation == "Transformação Logarítmica":
            transformacao_logaritmica(self.imagepath, output_path, float(value))
            # Carregue e exiba a imagem selecionada
        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência para evitar que a imagem seja coletada pelo garbage collector
    def show_value_input(self, event):
        selected_operation = self.selected_operation.get()

        # Condições para mostrar ou ocultar o campo de entrada de valor
        if selected_operation in ("Limiarização", "Transformação de Potência", "Transformação Logarítmica"):
            self.value_entry.place(x=450, y=360)
            self.value_label.place(x=390, y=360)
            self.value_entry.configure(state='normal')
        else:
            self.value_entry.place_forget()
            self.value_label.place_forget()
            self.value_entry.delete(0, 'end')

        # Atualiza o rótulo do valor com base na operação selecionada
        if selected_operation == "Limiarização":
            self.value_label.config(text="Threshold:")
        elif selected_operation == "Transformação de Potência":
            self.value_label.config(text="Gamma:")

        elif selected_operation == "Transformação Logarítmica":
            self.value_label.config(text="C:")
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            self.selected_image_path = file_path
            print(f"Caminho da imagem selecionada: {self.selected_image_path}")

            # Verifique a pasta "luminaprocessing" e conte quantos arquivos de imagem já existem
            processing_folder = "luminaprocessing"
            if not os.path.exists(processing_folder):
                os.makedirs(processing_folder)

            existing_files = os.listdir(processing_folder)
            num_existing_files = len([f for f in existing_files if f.startswith("image_")])

            # Crie um novo nome de arquivo para a imagem com base no número atual de arquivos
            new_filename = os.path.join(processing_folder, f"image_{num_existing_files}.png")

            # Copie o arquivo de imagem selecionado para a pasta de processamento com o novo nome
            shutil.copy(self.selected_image_path, new_filename)

            print(f"Imagem copiada para: {new_filename}")

            #dependendo da opcao a new filename ira rodar a funcao
            dissolve_cruzado(self.imagepath, file_path, new_filename,float(self.alpha_combobox.get()))
            #ou
            dissolve_cruzado_nao_uniforme(self.imagepath, file_path, new_filename,float(self.alpha_combobox.get()))

            # Carregue e exiba a imagem selecionada
            self.selected_image = Image.open(new_filename)
            self.selected_image = self.selected_image.resize((256, 256))
            self.selected_image = ImageTk.PhotoImage(self.selected_image)
            self.selected_image_label.config(image=self.selected_image)
            self.selected_image_label.image = self.selected_image  # Mantenha uma referência para evitar que a imagem seja coletada pelo garbage collector
        pass


