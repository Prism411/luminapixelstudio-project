import customtkinter
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image

def slider_event(value):
    print(value)

def checkbox_event():
    print("checkbox toggled, current value:", check_slide_var.get())

class ProcesserWindow:
    def __init__(self, filepath):
        self.filepath = filepath
        self.my_image = None  # Atributo para armazenar o CTkImage

    def start(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        root = customtkinter.CTk()
        root.geometry("800x650")
        root.resizable(False, False)

        frame = customtkinter.CTkFrame(master=root, corner_radius=10, width=770, height=415, fg_color="#211e2b")
        frame.place(x=15, y=225)

        # Carregar a imagem e criar o CTkImage
        my_image = customtkinter.CTkImage(light_image=Image.open(self.filepath), size=(200, 200))
        image_label = customtkinter.CTkLabel(root, image=self.im, text="")  # display image with a CTkLabel
        image_label.place(x=70,y=15)
        self.my_image = my_image

        # Configurar o Canvas e adicionar a imagem
        canvas_width, canvas_height = 200, 200
        canvas1 = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="gray")
        canvas1.place(x=70, y=15)
        x = canvas_width // 2
        y = canvas_height // 2
        canvas1.create_image(x, y, image=my_image.tk_image, anchor='center')  # Use o CTkImage

        root.canvas2 = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="gray")
        root.canvas2.place(x=550, y=15)  # Posicionamento do Canvas
        font = ("calibri", 18)

        sliderLabel = customtkinter.CTkLabel(root, text="Rotação", fg_color="transparent", font=font)
        sliderLabel.place(x=374, y=47)
        slider = customtkinter.CTkSlider(root, from_=-360, to=360, command=slider_event)
        slider.place(x=300, y=70)
        global check_slide_var
        check_slide_var = customtkinter.StringVar(value="on")
        checkbox_slide_var = customtkinter.CTkCheckBox(root, text="Modo I.B.", command=checkbox_event,
                                                      variable=check_slide_var, onvalue="on", offvalue="off")
        checkbox_slide_var.place(x=300, y=85)

        root.mainloop()

def startingProcesser(filepath):
    p = ProcesserWindow(filepath)
    p.start()
def checkbox_event():
    print("checkbox toggled, current value:", check_slide_var.get())