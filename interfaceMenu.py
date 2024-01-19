import os
import shutil
import tkinter
from tkinter import filedialog
import customtkinter
import cv2
import numpy as np
from PIL import Image, ImageTk

from imageProcesser import rotate_image, rotate_image2, reflect_image, dissolve_cruzado, dissolve_cruzado_nao_uniforme


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x650")
        self.title("CTk example")
        customtkinter.set_appearance_mode("dark")

        # Botão para selecionar imagem
        self.button = customtkinter.CTkButton(self, text="Selecionar Imagem", command=self.button_click)
        self.button.place(x=355, y=450)

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
            toplevel = ToplevelWindow(self, new_filename)

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, file_path, *args, **kwargs): #colocar o master aqui
        super().__init__( *args, **kwargs) #colocar o master aqui tambem
        self.geometry("800x650")
        self.resizable(False, False)
        self.title("Image Preview")
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
            pass
        else:
            reflect_image(image, 0, self.file_path)
            self.atualiza_imagem(self.file_path)
            pass

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





app = ToplevelWindow(file_path=r"C:\Users\jader\Desktop\estudos\ProcessamentoProva\luminaprocessing\real (35).png")
app.mainloop()