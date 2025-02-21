import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class GUI:
    def __init__(self, root, on_select_image, on_screenshot):
        self.root = root
        self.on_select_image = on_select_image
        self.on_screenshot = on_screenshot
        self.setup_ui()

    def setup_ui(self):
        # Configuração principal do grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Área da Imagem
        self.img_frame = ttk.LabelFrame(main_frame, text=" Visualização da Imagem ", width=320)
        self.img_frame.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=5, pady=5)

        self.img_label = ttk.Label(self.img_frame)
        self.img_label.pack(fill="both", expand=True)

        # Área de Tradução
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Botões
        self.btn_frame = ttk.Frame(text_frame)
        self.btn_frame.pack(pady=10, fill="x")

        self.btn_select_img = self.create_image_button(
            "assets/btn_select_image.png",
            self.on_select_image
        )
        self.btn_select_img.pack(side=tk.LEFT, padx=5)

        self.btn_screenshot_img = self.create_image_button(
            "assets/btn_screenshot.png",
            self.on_screenshot
        )
        self.btn_screenshot_img.pack(side=tk.LEFT, padx=5)

        # Áreas de Texto
        self.original_text = self.create_text_area(text_frame, "Texto Original (JP)")
        self.translated_text = self.create_text_area(text_frame, "Texto Traduzido (PT-BR)")

        # Configuração de pesos
        main_frame.grid_columnconfigure(0, weight=4)
        main_frame.grid_columnconfigure(1, weight=6)
        main_frame.grid_rowconfigure(0, weight=1)

    def create_image_button(self, image_path, command):
        img = Image.open(image_path)
        img = img.resize((32, 32), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        btn = ttk.Label(self.btn_frame, image=photo)
        btn.image = photo
        btn.bind("<Button-1>", lambda e: command())
        return btn

    def create_text_area(self, parent, title):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=5)

        lbl = ttk.Label(frame, text=title, font=("Arial", 10, "bold"))
        lbl.pack(anchor="w")

        text_widget = tk.Text(
            frame,
            wrap=tk.WORD,
            font=("Arial", 9),
            height=15,
            width=40,
            bg="#F8F9FA",
            relief="flat"
        )
        text_widget.pack(fill="both", expand=True)
        return text_widget

    def update_display(self, img_path, original, translated):
        # Atualizar imagem
        img = Image.open(img_path)
        img.thumbnail((300, 400))
        self.photo = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.photo)

        # Atualizar textos
        self.update_text(self.original_text, original)
        self.update_text(self.translated_text, translated)

    def update_text(self, text_widget, content):
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)