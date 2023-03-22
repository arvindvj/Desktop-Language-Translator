import cv2
import pytesseract
from langdetect import detect
from googletrans import Translator
from PIL import ImageGrab
import tkinter as tk
from tkinter import filedialog
from pynput import keyboard

# Configure tesseract path
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract' # Update this path according to your tesseract installation path

def capture_screen():
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.png')
    return 'screenshot.png'

def ocr_image(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    return text

def detect_language(text):
    return detect(text)

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def on_hotkey():
    screenshot_path = capture_screen()
    text = ocr_image(screenshot_path)
    language = detect_language(text)

    if language != 'en':
        translated_text = translate_text(text)
    else:
        translated_text = text

    app.add_translation(screenshot_path, translated_text)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Translator")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.listbox = tk.Listbox(self.frame, width=100, height=20)
        self.listbox.pack()

    def add_translation(self, screenshot_path, translated_text):
        entry = f"{screenshot_path}: {translated_text}"
        self.listbox.insert(tk.END, entry)
        self.listbox.see(tk.END)

COMBINATION = {keyboard.Key.cmd, keyboard.Key.ctrl, keyboard.KeyCode.from_char('t')}
current_keys = set()

def on_key_press(key):
    if key in COMBINATION:
        current_keys.add(key)
        if all(k in current_keys for k in COMBINATION):
            on_hotkey()

def on_key_release(key):
    if key in current_keys:
        current_keys.remove(key)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        root.mainloop()
        listener.join()
