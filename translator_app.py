import cv2
import pytesseract
from langdetect import detect
from googletrans import Translator
from PIL import ImageGrab
import tkinter as tk
from tkinter import filedialog
from pynput import keyboard
import threading
import textwrap
import pyperclip

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
    clipboard_text = pyperclip.paste().strip()
    
    if clipboard_text:
        text = clipboard_text
        screenshot_path = "Clipboard"
    else:
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

        self.text = tk.Text(self.frame, width=100, height=20, wrap=tk.WORD)
        self.text.pack()
        self.text.configure(state='disabled')

    def add_translation(self, screenshot_path, translated_text):
        wrapped_text = textwrap.fill(translated_text, 80)
        entry = f"{screenshot_path}:\n{wrapped_text}\n\n"
        
        self.text.configure(state='normal')
        self.text.insert(tk.END, entry)
        self.text.see(tk.END)
        self.text.configure(state='disabled')

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

def hotkey_listener():
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    
    hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
    hotkey_thread.start()

    root.mainloop()
