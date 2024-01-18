import customtkinter
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image

def slider_event(value):
    print(value)

def checkbox_event():
    print("checkbox toggled, current value:", check_slide_var.get())

class ProcesserWindow(customtkinter.CTkToplevel):

    def __init__(self,parent, filepath, image):
        super().__init__(parent)
        self.filepath = filepath
        self.my_image = None  # Atributo para armazenar o CTkImage
        self.image = image

    def start(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        root = customtkinter.CTk()
        root.geometry("800x650")
        root.resizable(False, False)

        font = ("calibri", 18)

        root.selected_image_label = tk.Label(root, text="imagem")
        root.selected_image_label.pack()
        root.selected_image_label.place(x=500, y=20)

        root.selected_image = Image.open(self.filepath)
        root.selected_image = root.selected_image.resize((256, 256))
        root.selected_image = ImageTk.PhotoImage(root.selected_image)
        root.selected_image_label.config(image=root.selected_image)
        root.selected_image_label.image = root.selected_image  # Mantenha uma referência

        #my_image = customtkinter.CTkImage(light_image=Image.open(self.filepath), size=(200, 200))
        #image_label = customtkinter.CTkLabel(root, image=self.image, text="")  # display image with a CTkLabel
        #image_label.place(x=70, y=15)

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
def checkbox_event():
    print("checkbox toggled, current value:", check_slide_var.get())


