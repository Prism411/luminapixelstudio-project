import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk

import cv2
import numpy as np
from PIL import ImageTk, Image

from imageProcesser import dissolve_cruzado, dissolve_cruzado_nao_uniforme, redimensionar_imagem, negativo, \
    alargamento_contraste, limiarizacao, transformacao_potencia, transformacao_logaritmica, scale_image, shear_image


class ImageDisplayWindow(tk.Toplevel):
    def __init__(self, parent, imagepath, image):
        super().__init__(parent)
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
        #Label de Valor para Expansão
        self.expansion_entry = tk.Entry(self)
        self.expansion_entry.pack()
        self.expansion_entry.place(x=550, y=392)
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

        # Combobox para selecionar uma operação
        self.operationReso = tk.StringVar()
        self.reso_combobox = ttk.Combobox(self, textvariable=self.operationReso)
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

    def reso_operation(self, event):
        operation = self.operationReso.get()
        scale_x, scale_y = float(self.resX_entry.get()), float(self.resY_entry.get())
        # Converter a imagem do Tkinter (PhotoImage) para o formato do OpenCV
        imagePIL = Image.open(self.imagepath)  # Use o caminho do arquivo da imagem original
        imageInput = np.array(imagePIL)  # Converte para array do NumPy
        imageInput = cv2.cvtColor(imageInput, cv2.COLOR_RGB2BGR)  # Converte de RGB para BGR
        output_path = "luminaprocessing/resultado.png"

        if operation == "Scaling":
            scale_image(imageInput, scale_x, scale_y, output_path)
        elif operation == "Cisalhamento":
            shear_image(imageInput, scale_x, scale_y, output_path)

        self.selected_image = Image.open(output_path)
        self.selected_image = self.selected_image.resize((256, 256))
        self.selected_image = ImageTk.PhotoImage(self.selected_image)
        self.selected_image_label.config(image=self.selected_image)
        self.selected_image_label.image = self.selected_image  # Mantenha uma referência

    def ctrl_contraste(self):
        #realce_contraste_adaptativo(imagem, c, tamanho_kernel, output_path)
        pass
    def equali_hist(self):
        print("teste")
    def expansion_hist(self):
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


