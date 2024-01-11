import tkinter as tk

class ImageDisplayWindow(tk.Toplevel):
    def __init__(self, parent, image):
        super().__init__(parent)
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
