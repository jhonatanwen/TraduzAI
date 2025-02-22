import os
import threading
import time
import tkinter as tk
import warnings
from tkinter import filedialog

import pytesseract
from PIL import ImageGrab
from transformers.utils import logging

from modules.gui import GUI
from modules.ocr import process_image
from modules.translation import Translator

warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub")
logging.set_verbosity_error()

class TraduzAI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TraduzAI")
        self.translator = Translator()
        self.gui = GUI(
            self.root,
            on_select_image=self.load_image,
            on_screenshot=self.start_snip_mode,
            on_text_update=self.handle_text_update
        )
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.snip_active = False

    def handle_text_update(self, text):
        try:
            translated = self.translator.translate(text)
            self.gui.update_translation(translated)
        except Exception as e:
            print(f"Erro na tradução: {str(e)}")

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.process_file(file_path)

    def start_snip_mode(self):
        """Inicia o modo de espera para captura de área"""
        if not self.snip_active:
            self.snip_active = True
            self.root.iconify()  # Minimiza a janela
            threading.Thread(target=self.monitor_clipboard).start()

    def monitor_clipboard(self):
        """Monitora a área de transferência por 60 segundos"""
        start_time = time.time()
        while time.time() - start_time < 60:
            try:
                img = ImageGrab.grabclipboard()
                if img is not None:
                    img.save("screenshot_temp.png")
                    self.root.after(0, self.process_file, "screenshot_temp.png")
                    self.root.after(0, self.root.deiconify)  # Restaura a janela
                    break
            except Exception as e:
                print(f"Erro: {str(e)}")
            time.sleep(0.5)
        self.snip_active = False

    def process_file(self, path):
        try:
            original_text = process_image(path)
            translated_text = self.translator.translate(original_text)
            self.gui.update_display(path, original_text, translated_text)
        except Exception as e:
            print(f"Erro: {str(e)}")

    def on_close(self):
        if os.path.exists("screenshot_temp.png"):
            os.remove("screenshot_temp.png")
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    app = TraduzAI()
    app.run()