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
#   Aqui é a função main do aplicativo, junto com o proprio frontend.
#   Para impedir o computador do usuario de se auto-destruir, foi adicionado uma precaução na função de scalling.
# ==============================================================================

import os
import shutil
import tkinter
import customtkinter
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog

from imageProcesser import rotate_image, rotate_image2, reflect_image, dissolve_cruzado, dissolve_cruzado_nao_uniforme, \
    negativo, alargamento_contraste, limiarizacao, transformacao_potencia, transformacao_logaritmica, \
    expand_histogram_auto, histogram_equalization, realce_contraste_adaptativo, scale_image, shear_image, edge_pinch, \
    vertical_pinch, field_based_warping, aplicar_filtro_media, aplicar_filtro_mediana, agucamento_bordas, aplicar_sobel, \
    high_boost, convolucao_com_offset


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x650")
        self.resizable(False, False)
        self.title("Lumina Pixel Studio")
        customtkinter.set_appearance_mode("dark")
        font = ("calibri",24)
        self.my_frame = customtkinter.CTkFrame(self, width=400, height=150)
        #C:\Users\jader\Desktop\estudos\ProcessamentoProva\icons\iconRemoveBG.png
        # Use place for positioning only
        self.my_frame.place(x=210, y=415)
        # Botão para selecionar imagem
        self.button = customtkinter.CTkButton(self, text="Selecionar Imagem", command=self.button_click,font=font)
        self.button.place(x=310, y=470)
        self.prcpImage = customtkinter.CTkImage(dark_image=Image.open("icons/iconRemoveBG.png"),
                                          size=(312, 312))
        self.image_label = customtkinter.CTkLabel(self, image=self.prcpImage, text="")
        self.image_label.place(x=256,y=0)
        self.folderImage = customtkinter.CTkImage(dark_image=Image.open("icons/folder2.png"),
                                          size=(32, 32))
        self.contactImage = self.button = customtkinter.CTkImage(dark_image=Image.open("icons/contact.png"),
                                          size=(32, 32))
        self.infoImage = self.button = customtkinter.CTkImage(dark_image=Image.open("icons/info.png"),
                                          size=(32, 32))
        self.folder_button =  self.button = customtkinter.CTkButton(self, text="", command=self.folder_button_operation, image=self.folderImage,fg_color="transparent")
        self.folder_button.place(x = 125,y=325)

        self.contact_button =  self.button = customtkinter.CTkButton(self, text="", command=self.contact_button_operation, image=self.contactImage,fg_color="transparent")
        self.contact_button.place(x = 340,y=325)

        self.info_button = self.button = customtkinter.CTkButton(self, text="", command=self.info_image_operation,
                                                                    image=self.infoImage,fg_color="transparent")
        self.info_button.place(x=540, y=325)

    def info_image_operation(self):
        info_text = """Este é o LuminaPixel Studio, um aplicativo de processamento de imagens. Você pode usar este aplicativo para realizar várias operações em imagens, como redimensionamento, filtragem e muito mais."""
        simpledialog.messagebox.showinfo("Informações", info_text)
    def contact_button_operation(self):
        contact_text = """Aplicativo criado por Jáder Louis e Nataly Tobias com a Orientação do Professor Dr. Lucas Marques da Cunha, Universidade Federal de Rondônia do Departamento de Ciencia da Computação (DACC), em Janeiro de 2024.
                   """
        simpledialog.messagebox.showinfo("Contato", contact_text)
    def folder_button_operation(self):
        os.startfile("luminaprocessing")
    def button_click(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((512, 512))
            self.selected_image = ImageTk.PhotoImage(image)

            # Processamento da imagem
            processing_folder = "luminaprocessing"
            if not os.path.exists(processing_folder):
                os.makedirs(processing_folder)
            existing_files = os.listdir(processing_folder)
            num_existing_files = len([f for f in existing_files if f.startswith("image_")])
            new_filename = os.path.join(processing_folder, f"image_{num_existing_files}.png")
            shutil.copy(file_path, new_filename)
            print(f"Imagem copiada para: {new_filename}")

            # Abrir a janela Toplevel
            toplevel = ToplevelWindow(new_filename)

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, file_path, *args, **kwargs): #colocar o master aqui
        super().__init__( *args, **kwargs) #colocar o master aqui tambem
        self.geometry("800x650")
        self.resizable(False, False)
        self.title("Lumina Pixel Studio - Image Preview")
        self.file_path = file_path
        customtkinter.set_appearance_mode("dark")
        self.font = ("calibri", 18)
        # Create a frame with width and height specified in the constructor
        self.my_frame = customtkinter.CTkFrame(self, width=750, height=425)
        # Use place for positioning only
        self.my_frame.place(x=25, y=220)
        self.my_image = customtkinter.CTkImage(light_image=Image.open(self.file_path),
                                          size=(200, 200))
        self.image_label = customtkinter.CTkLabel(self, image=self.my_image, text="")
        self.image_label.place(x=50,y=15)

        self.sliderLabel = customtkinter.CTkLabel(self, text="Rotação", fg_color="transparent", font=self.font)
        self.sliderLabel.place(x=374, y=47)
        self.slider = customtkinter.CTkSlider(self, from_=-360, to=360, command=self.slider_event)
        self.slider.place(x=300, y=70)
        self.slideReader = int(self.slider.get())
        global check_slide_var
        check_slide_var = customtkinter.StringVar(value="on")
        self.checkbox_slide_var = customtkinter.CTkCheckBox(self, text="Modo I.B.", command=self.checkbox_event,
                                                      variable=check_slide_var, onvalue="on", offvalue="off")
        self.checkbox_slide_var.place(x=300, y=85)

        self.rot_button = customtkinter.CTkButton(self, text="Rotacionar", command=self.rot_buttonOperation)
        self.rot_button.place(x=355, y=150)
        # Radio Button para Rotação
        self.radio_var = tkinter.IntVar(value=0)
        self.radiobutton_1 = customtkinter.CTkRadioButton(self, text="Rotacionar Vertical",
                                                     command=self.radiobutton_event, variable=self.radio_var, value=1)
        self.radiobutton_2 = customtkinter.CTkRadioButton(self, text="Rotacionar Horizontal",
                                                     command=self.radiobutton_event, variable=self.radio_var, value=2)
        self.radiobutton_2.place(x=260,y = 30)
        self.radiobutton_1.place(x=420,y=30)
        #fim do radio Button para Rotação



        #Começo do radio Button CRUZADO
        self.cruzadoRadio = tkinter.IntVar(value=0)
        self.cruzadoRadio1 = customtkinter.CTkRadioButton(self.my_frame, text="Dissolver Cruzado",
                                                     command=self.cruzadoButton_event, variable=self.cruzadoRadio, value=1)
        self.cruzadoRadio2 = customtkinter.CTkRadioButton(self.my_frame, text="Dissolver Cruzado N.U.",
                                                     command=self.cruzadoButton_event, variable=self.cruzadoRadio, value=2)
        self.cruzadoRadio1.place(x=5,y = 5)
        self.cruzadoRadio2.place(x=200,y=5)

        self.rot_button = customtkinter.CTkButton(self.my_frame, text="Selecionar Cruzada", command=self.cruzadoButton_operation)
        self.rot_button.place(x=580, y=5)

        self.cruzadocombobox_var = customtkinter.StringVar(value="option 2")
        self.cruzadocombobox = customtkinter.CTkComboBox(self.my_frame, values=["0.1", "0.2","0.3","0.4","0.5", "0.6","0.7", "0.8",
                                                                    "0.9", "1.0"],
                                             command=self.cruzadoCombobox_callback, variable=self.cruzadocombobox_var)
        self.cruzadocombobox_var.set("0.5")
        self.cruzadocombobox.place(x=400,y=5)
        #FIM DA TRANSFORMAÇÃO DE INTENSIDADE CONFIG


        ##COMEÇA AQUI TRANSFORMAÇÃO DE INTENSIDADE CONFIG
        # Variável para rastrear a escolha do usuário
        self.selected_operation = customtkinter.StringVar()
        self.selected_operation.set("Transformação de Intensidade:")  # Defina o valor inicial

        # Combobox para selecionar uma operação
        self.operations_combobox = customtkinter.CTkComboBox(self.my_frame, values=["Alargamento de Contraste", "Negativo",
                                                                                    "Limiarização", "Transformação de Potência",
                                                                                    "Transformação Logarítmica"],command=self.show_value_input,variable =self.selected_operation)


        self.operations_combobox.pack()
        self.operations_combobox.place(x=5, y=40)
        self.operations_combobox.bind("<<ComboboxSelected>>", self.show_value_input)
        # Rótulo para descrever o campo de entrada de valor
        self.value_label = customtkinter.CTkLabel(self.my_frame, text="Valor:")
        self.value_label.pack()
        self.value_label.place(x=330, y=360)
        # Campo de entrada para o valor
        self.value_entry = customtkinter.CTkEntry(self.my_frame)
        self.value_entry.pack()
        self.value_entry.place(x=370, y=360)
        # Inicialmente oculta o campo de entrada e o rótulo
        self.value_entry.place_forget()
        self.value_label.place_forget()
        self.value_button = customtkinter.CTkButton(self.my_frame, text = "Processar!",command= self.value_operation)
        self.value_button.place(x= 360,y=40)
        ##OPERACOES DO HISTOGRAMA AQUI

        self.equalHist_button = customtkinter.CTkButton(self.my_frame, text="Equalizar Histograma", command=self.equalHist_operation)
        self.equalHist_button.place(x=5,y=80)

        self.expandHist_button = customtkinter.CTkButton(self.my_frame, text="Expandir Histograma",
                                                        command=self.expandHist_operation)
        self.expandHist_button.place(x=150, y=80)
        self.gain_label = customtkinter.CTkLabel(self.my_frame, text="Ganho:")
        self.gain_label.place(x=300,y=80)
        self.gain_entry = customtkinter.CTkEntry(self.my_frame)
        self.gain_entry.place(x=350,y=80)


        #Controle de Contraste
        self.C_label = customtkinter.CTkLabel(self.my_frame, text="C:")
        self.C_label.place(x=5,y=120)
        self.C_entry = customtkinter.CTkEntry(self.my_frame)
        self.C_entry.place(x=20,y=120)

        self.kernel_label = customtkinter.CTkLabel(self.my_frame, text="Tamanho Kernel:")
        self.kernel_label.place(x=170,y=120)

        self.kernel_entry = customtkinter.CTkEntry(self.my_frame)
        self.kernel_entry.place(x=270,y=120)

        self.ctrlContraste_button = customtkinter.CTkButton(self.my_frame, text="Controle Contraste",
                                                        command=self.ctrlContraste_operation)
        self.ctrlContraste_button.place(x=500, y=120)
        ## FIM DO CONTROLE DE CONTRASTE

        ##Inicio das Resoluçao
        # Variável para rastrear a escolha do usuário
        self.resoselected_operation = customtkinter.StringVar()
        self.reso_combobox = customtkinter.CTkComboBox(self.my_frame,
                                                             values=["Cisalhamento", "Scalling"],
                                                             variable=self.resoselected_operation)
        self.reso_combobox.place(x=5,y=160)
        self.x_label = customtkinter.CTkLabel(self.my_frame, text="Aumento em X:")
        self.x_label.place(x=150,y=160)

        self.x_entry = customtkinter.CTkEntry(self.my_frame)
        self.x_entry.place(x=240,y=160)

        self.y_label = customtkinter.CTkLabel(self.my_frame, text="Aumento em Y:")
        self.y_label.place(x=380,y=160)

        self.y_entry = customtkinter.CTkEntry(self.my_frame)
        self.y_entry.place(x=470,y=160)

        self.reso_button = customtkinter.CTkButton(self.my_frame, text="Processar Resolução",
                                                            command=self.reso_Operation)
        self.reso_button.place(x=610,y=160)
        #FIM DAS RESO_OPERATIONS

        ### PPW pinch pinch warp aqui
        ##INCIO
        self.ppw_operation = customtkinter.StringVar()
        self.ppw_operation.set("Selecionar Modo!")
        self.ppw_combobox = customtkinter.CTkComboBox(self.my_frame,
                                                       values=["Pínch Vertical", "Pinch nas Bordas","Warping Baseado em Campo"],
                                                       variable=self.ppw_operation)
        self.ppw_combobox.place(x=5,y=200)

        self.ppw_label = customtkinter.CTkLabel(self.my_frame, text="Quantidade:")
        self.ppw_label.place(x=150, y=200)

        self.ppw_entry = customtkinter.CTkEntry(self.my_frame)
        self.ppw_entry.place(x=220, y=200)

        self.ppw_button = customtkinter.CTkButton(self.my_frame, text="Processar Resolução",
                                                   command=self.ppw_Operation)
        self.ppw_button.place(x=370,y=200)
        ##Fim do ppw aqui

        ##Inicio dos filtros
       #"Filtro Media",
       # "Filtro Mediana",
        self.selectedfiltro_operation = customtkinter.StringVar()
        self.selectedfiltro_operation.set("Selecionar Modo!")
        self.filtro_combobox = customtkinter.CTkComboBox(self.my_frame,
                                                  values=["Filtro Media", "Filtro Mediana"],
                                                  variable=self.selectedfiltro_operation)
        self.filtro_combobox.place(x=5,y=240)

        self.kernelFilter_label = customtkinter.CTkLabel(self.my_frame, text="Tamanho do Kernel:")
        self.kernelFilter_label.place(x=150, y=240)

        self.kernelFilter_entry = customtkinter.CTkEntry(self.my_frame)
        self.kernelFilter_entry.place(x=270, y=240)

        self.filtro_button = customtkinter.CTkButton(self.my_frame, text="Processar Filtro",
                                                  command=self.filtro_operation)
        self.filtro_button.place(x=5, y=240)

        ##FILTROS ABAIXO

        self.sobel_button = customtkinter.CTkButton(self.my_frame, text="Gradiente de Sobel",
                                                  command=self.sobel_operation)
        self.sobel_button.place(x=5, y=280)

        self.algcBordas_button = customtkinter.CTkButton(self.my_frame, text="Aguçamento de Bordas",
                                                  command=self.algcBordas_operation)
        self.algcBordas_button.place(x=147, y=280)

        self.k_label = customtkinter.CTkLabel(self.my_frame, text="Valor de K:")
        self.k_label.place(x=300, y=280)

        self.k_entry = customtkinter.CTkEntry(self.my_frame)
        self.k_entry.place(x=363, y=280)

        self.highboost_button = customtkinter.CTkButton(self.my_frame, text="Processar HighBoost",
                                                    command=self.highboost_button)
        self.highboost_button.place(x=510,y=280)

        ##Fim dos Filtros
        ##Inicio da Convolução
        self.inserirMatriz_button = customtkinter.CTkButton(self.my_frame, text="Inserir Matriz (N x M)",
                                                    command=self.inserir_matriz)
        self.inserirMatriz_button.place(x=5,y=320)
        self.convoOffset_label = customtkinter.CTkLabel(self.my_frame, text="Valor de K:")
        self.convoOffset_label.place(x=150, y=320)

        self.convoOffset_entry = customtkinter.CTkEntry(self.my_frame)
        self.convoOffset_entry.place(x=220, y=320)

        self.convo_button = customtkinter.CTkButton(self.my_frame, text="Processar Convolução",
                                                        command=self.convo_operation)
        self.convo_button.place(x=510, y=320)

    def convo_operation(self):
        image = imageTransform(self.file_path)
        kernel = np.array(self.matriz)
        offset = int(self.convoOffset_entry.get())
        convolucao_com_offset(image, kernel, offset, self.file_path)
        self.atualiza_imagem(self.file_path)
        pass

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
    def highboost_button(self):
        imageInput = imageTransform(self.file_path)
        k = int(self.k_entry.get())
        if k>256:
            k = 255
        high_boost(imageInput, k, self.file_path)
        self.atualiza_imagem(self.file_path)
        pass
    def algcBordas_operation(self):
        imageInput = imageTransform(self.file_path)
        agucamento_bordas(imageInput, self.file_path)
        self.atualiza_imagem(self.file_path)
        pass
    def sobel_operation(self):
        imageInput = imageTransform(self.file_path)
        aplicar_sobel(imageInput, self.file_path)
        self.atualiza_imagem(self.file_path)
        pass
    def filtro_operation(self):
        image = imageTransform(self.file_path)
        opr = str(self.selectedfiltro_operation.get())
        kernel_size = int(self.kernelFilter_entry.get())
        if opr == "Filtro Media":
            aplicar_filtro_media(image, kernel_size, self.file_path)
        if opr == "Filtro Mediana":
            aplicar_filtro_mediana(image, kernel_size, self.file_path)
        self.atualiza_imagem(self.file_path)

    def ppw_Operation(self):
        image = imageTransform(self.file_path)
        opr = str(self.ppw_operation.get())
        if opr == "Pínch Vertical":
            amount = int(self.ppw_entry.get())
            vertical_pinch(image, amount, self.file_path)
        if opr == "Pinch nas Bordas":
            amount = float(self.ppw_entry.get())
            edge_pinch(image, amount, self.file_path)
        if opr == "Warping Baseado em Campo":
            amount = int(self.ppw_entry.get())
            rows, cols = image.shape[:2]
            field = [[[0, 0] for _ in range(cols)] for _ in range(rows)]
            center_x, center_y = cols / 2, rows / 2
            for i in range(rows):
                for j in range(cols):
                    distance_to_center = np.sqrt((center_x - j) ** 2 + (center_y - i) ** 2)
                    scale = (1 - distance_to_center / max(center_x, center_y)) * amount
                    field[i][j] = [scale * (center_x - j), scale * (center_y - i)]
            field_based_warping(image, field, self.file_path)
        self.atualiza_imagem(self.file_path)


    def reso_Operation(self):
        opr = str(self.resoselected_operation.get())
        image = imageTransform(self.file_path)
        scale_x = float(self.x_entry.get())
        scale_y = float(self.y_entry.get())
        if scale_x > 2 and opr == "Scalling":
            messagebox.showwarning("CUIDADO", "Cuidado ao Usar Valores Maiores que 1!\nisto é um aumento de proporção na resolução!")
        if scale_y > 2 and opr == "Scalling":
            messagebox.showwarning("CUIDADO", "Cuidado ao Usar Valores Maiores que 1!\nisto é um aumento de proporção na resolução!")
        if opr == "Cisalhamento":
            shear_image(image, scale_x, scale_y, self.file_path)
        if opr == "Scalling":
            if scale_x > 10: #Medida de Segurança
                scale_x = 1
            if scale_y > 10: #Medida de Segurança
                scale_y = 1
            scale_image(image, scale_x, scale_y, self.file_path)
        self.atualiza_imagem(self.file_path)


    def ctrlContraste_operation(self):
        image = imageTransform(self.file_path)
        c = int(self.C_entry.get())
        tamanho_kernel = int(self.kernel_entry.get())
        result = realce_contraste_adaptativo(image, c, tamanho_kernel)
        imagem_final = Image.fromarray(np.array(result, dtype=np.uint8))
        imagem_final.save(self.file_path)
        self.atualiza_imagem(self.file_path)

    def expandHist_operation(self):
        gain = self.gain_entry.get().strip()
        if not gain:
            messagebox.showerror("Erro", "Por favor, insira um valor para o ganho.")
        else:
            try:
                gain = int(gain)
                image = imageTransform(self.file_path)
                expand_histogram_auto(image, gain, self.file_path, True)
                self.atualiza_imagem(self.file_path)
            except ValueError:
                messagebox.showerror("Erro", "O ganho deve ser um número inteiro.")

        pass
    def equalHist_operation(self):
        gain = int(self.gain_entry.get())
        image = imageTransform(self.file_path)
        histogram_equalization(image, self.file_path, True)
        self.atualiza_imagem(self.file_path)
        pass

  ##COMEÇO DAS FUNÇÕES DE CONTROLE AQUI###########################################################
    def value_operation(self):
        selected_operation = str(self.selected_operation.get())# Obtém a operação selecionada e o valor, se necessário
        operation = self.selected_operation.get()
        value = self.value_entry.get()
        # Chama a função correspondente baseada na operação selecionada
        if operation == "Negativo":
            negativo(self.file_path, self.file_path)
        elif operation == "Alargamento de Contraste":
            alargamento_contraste(self.file_path, self.file_path)
        elif operation == "Limiarização":
            limiarizacao(self.file_path, self.file_path, float(value))
        elif operation == "Transformação de Potência":
            transformacao_potencia(self.file_path, self.file_path, float(value))
        elif operation == "Transformação Logarítmica":
            transformacao_logaritmica(self.file_path, self.file_path, float(value))
        self.atualiza_imagem(self.file_path)

    def show_value_input(self, event):
        selected_operation = str(self.selected_operation.get())

        # Condições para mostrar ou ocultar o campo de entrada de valor
        if selected_operation in ("Limiarização", "Transformação de Potência", "Transformação Logarítmica"):
            self.value_entry.place(x=210, y=40)
            self.value_label.place(x=150, y=40)
            self.value_entry.configure(state='normal')
            print("mostrar")
        else:
            self.value_entry.place_forget()
            self.value_label.place_forget()
            self.value_entry.delete(0, 'end')

        # Atualiza o rótulo do valor com base na operação selecionada
        if selected_operation == "Limiarização":
            self.value_label.configure(text="Threshold:")
        elif selected_operation == "Transformação de Potência":
            self.value_label.configure(text="Gamma:")

        elif selected_operation == "Transformação Logarítmica":
            self.value_label.configure(text="C:")

    def cruzadoButton_operation(self):

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

            if int(self.cruzadoRadio.get()) == 1:
                dissolve_cruzado(self.file_path, new_filename, file_path, float(self.cruzadocombobox_var.get()))
            if int(self.cruzadoRadio.get()) == 2:
                dissolve_cruzado_nao_uniforme(self.file_path, new_filename, file_path,
                                              float(self.cruzadocombobox_var.get()))
            self.atualiza_imagem(file_path)
    def cruzadoButton_event(self):
        pass
    def cruzadoCombobox_callback(self,choice):
        pass
    def radiobutton_event(self):
        operacao = int(self.radio_var.get())
        image = imageTransform(self.file_path)
        if operacao == 1:
            reflect_image(image, 1, self.file_path)
            self.atualiza_imagem(self.file_path)
        else:
            reflect_image(image, 0, self.file_path)
            self.atualiza_imagem(self.file_path)


    def rot_buttonOperation(self):
        image = imageTransform(self.file_path)
        angulo = int(self.slider.get())
        print(self.slideReader)
        if self.checkbox_event():
            rotate_image2(image,angulo,self.file_path, center=None, scale=1.0)
            self.atualiza_imagem(self.file_path)
        else:
            rotate_image(image, angulo,self.file_path, center=None, scale=1.0)## Sem Interpolação Bilinear
            self.atualiza_imagem(self.file_path)
        return


    def checkbox_event(self):
        return bool(check_slide_var.get())
    def slider_event(self,value):
        return int(value)

    def atualiza_imagem(self,filepath):
        self.result_image = customtkinter.CTkImage(light_image=Image.open(filepath),
                                          size=(200, 200))
        self.result_image_label = customtkinter.CTkLabel(self, image=self.result_image, text="")
        self.result_image_label.place(x=570,y=15)


def imageTransform(filepath):
    imagePIL = Image.open(filepath)  # Use o caminho do arquivo da imagem original
    imageInput = np.array(imagePIL)  # Converte para array do NumPy
    imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte  de RGB para BGR
    return imageInput





app = App()
app.mainloop()