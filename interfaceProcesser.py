import customtkinter


class imageEditor(customtkinter.CTk):
    def __init__(self,filepath):
        super().__init__()
        self.geometry("800x600")
        self.title("CTk example")

        # add widgets to app
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=10)

    # add methods to app
    def button_click(self):
        print("button click")

