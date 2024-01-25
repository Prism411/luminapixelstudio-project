import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from PIL import Image, ImageTk

from imageDisplayWindow import ImageDisplayWindow


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LuminaPixel Studio")
        self.geometry("800x600")  # Defina o tamanho da janela como 800x600
        self.resizable(False, False)  # Bloqueie a capacidade de redimensionar a janela

        # Carregue a imagem
        image = Image.open("icons/iconRemoveBG.png")
        image.thumbnail((512, 512))  # Redimensione a imagem conforme necessário
        self.icon = ImageTk.PhotoImage(image)
        # Defina cores para o modo dark com um esquema de cores mais moderno
        self.configure(bg="#202225")

        #Carrega a Imagem Principal
        self.image_label = tk.Label(self, image=self.icon, bg="#202225")
        self.image_label.pack()
        self.selected_image = None

        # Exiba a imagem de informação no canto superior direito
        info_image = Image.open("icons/info.png")
        info_image = info_image.resize((32, 32))  # Redimensione a imagem
        info_icon = ImageTk.PhotoImage(info_image)
        self.info_button = tk.Button(self, image=info_icon, command=self.show_info, bg="#202225")
        self.info_button.image = info_icon
        self.info_button.place(x=750, y=10)  # Posicione o botão no canto superior direito

        # Exiba a imagem de contato e crie um botão personalizado com uma cor de fundo para contato
        contact_image = Image.open("icons/contact.png")
        contact_image = contact_image.resize((32, 32))  # Redimensione a imagem
        contact_icon = ImageTk.PhotoImage(contact_image)

        self.contact_button = tk.Button(self, image=contact_icon, command=self.show_contact, bg="#202225")
        self.contact_button.image = contact_icon
        self.contact_button.place(x=750, y=60)  # Posicione o botão logo abaixo do botão de informações

        # Use o tema estilo "clam" para botões em modo dark
        style = ttk.Style(self)
        style.configure("TButton", foreground="black", background="#5865F2", font=("Helvetica", 14))

        self.selected_image = None

        self.image_processing_button = ttk.Button(self, text="Selecionar Imagem", command=self.select_image)
        self.image_processing_button.pack()



    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((512, 512))
            self.selected_image = ImageTk.PhotoImage(image)
            self.show_selected_image(file_path)

            # Verifique a pasta "luminaprocessing" e conte quantos arquivos de imagem já existem
            processing_folder = "luminaprocessing"
            if not os.path.exists(processing_folder):
                os.makedirs(processing_folder)
            existing_files = os.listdir(processing_folder)
            num_existing_files = len([f for f in existing_files if f.startswith("image_")])
            # Crie um novo nome de arquivo para a imagem com base no número atual de arquivos
            new_filename = os.path.join(processing_folder, f"image_{num_existing_files}.png")
            # Copie o arquivo de imagem selecionado para a pasta de processamento com o novo nome
            shutil.copy(file_path, new_filename)

            print(f"Imagem copiada para: {new_filename}")
    def show_selected_image(self,file_path):
        if self.selected_image:
            # Keep a reference to the PhotoImage object to prevent garbage collection.
            self.processed_image = ImageTk.PhotoImage(Image.open(file_path))
            # Open a new window to display the centered image
            image_window = ImageDisplayWindow(self, file_path, image=self.processed_image)
            #p = ProcesserWindow(self,file_path,image = self.processed_image)
           # p.start()
            image_window.grab_set()
    def process_images(self):
        # Implemente a lógica para processamento de imagens aqui
        pass

    def show_info(self):
        info_text = """Este é o LuminaPixel Studio, um aplicativo de processamento de imagens. Você pode usar este aplicativo para realizar várias operações em imagens, como redimensionamento, filtragem e muito mais."""
        simpledialog.messagebox.showinfo("Informações", info_text)
        pass

    def show_contact(self):
        contact_text = """Aplicativo criado por Jáder Louis e Nataly Tobias com a Orientação do Professor Dr. Lucas Marques da Cunha, Universidade Federal de Rondônia do Departamento de Ciencia da Computação (DACC), em Janeiro de 2024.
           """
        simpledialog.messagebox.showinfo("Contato", contact_text)

def limpar_pasta_luminaprocessing():
    processing_folder = "luminaprocessing"
    if os.path.exists(processing_folder):
        for filename in os.listdir(processing_folder):
            file_path = os.path.join(processing_folder, filename)
            try:
                if os.path.isfile(file_path):
                    pass
                    #os.remove(file_path)
            except Exception as e:
                print(f"Erro ao excluir o arquivo {file_path}: {e}")

if __name__ == "__main__":
    limpar_pasta_luminaprocessing()
    app = MainMenu()
    app.mainloop()
