import os
import shutil
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk

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
            toplevel = ToplevelWindow(self, file_path)

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, master, file_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.geometry("800x650")
        self.resizable(False, False)
        self.title("Image Preview")
        customtkinter.set_appearance_mode("dark")
        font = ("calibri", 18)
        my_image = customtkinter.CTkImage(light_image=Image.open(file_path),
                                          size=(200, 200))
        image_label = customtkinter.CTkLabel(self, image=my_image, text="")
        image_label.place(x=50,y=15)

        sliderLabel = customtkinter.CTkLabel(self, text="Rotação", fg_color="transparent", font=font)
        sliderLabel.place(x=374, y=47)
        slider = customtkinter.CTkSlider(self, from_=-360, to=360, command=slider_event)
        slider.place(x=300, y=70)
        global check_slide_var
        check_slide_var = customtkinter.StringVar(value="on")
        checkbox_slide_var = customtkinter.CTkCheckBox(self, text="Modo I.B.", command=checkbox_event,
                                                      variable=check_slide_var, onvalue="on", offvalue="off")
        checkbox_slide_var.place(x=300, y=85)

def checkbox_event():
    print("checkbox toggled, current value:", check_slide_var.get())
def slider_event(value):
    print(value)
app = App()
app.mainloop()
