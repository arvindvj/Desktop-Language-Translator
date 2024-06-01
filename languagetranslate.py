import tkinter as tk
from tkinter import filedialog, messagebox
from translator import translate_document
import os

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translation App")
        
        self.label = tk.Label(root, text="Select a Word Document to Translate")
        self.label.pack(pady=10)
        
        self.input_btn = tk.Button(root, text="Select Input File", command=self.select_input_file)
        self.input_btn.pack(pady=5)
        
        self.output_btn = tk.Button(root, text="Select Output File", command=self.select_output_file)
        self.output_btn.pack(pady=5)

        self.src_lang_label = tk.Label(root, text="Select Source Language")
        self.src_lang_label.pack(pady=5)
        self.src_lang_var = tk.StringVar(value='en')
        self.src_lang_menu = tk.OptionMenu(root, self.src_lang_var, 'en', 'kn')
        self.src_lang_menu.pack(pady=5)

        self.dest_lang_label = tk.Label(root, text="Select Target Language")
        self.dest_lang_label.pack(pady=5)
        self.dest_lang_var = tk.StringVar(value='kn')
        self.dest_lang_menu = tk.OptionMenu(root, self.dest_lang_var, 'kn', 'en')
        self.dest_lang_menu.pack(pady=5)
        
        self.translate_btn = tk.Button(root, text="Translate", command=self.translate)
        self.translate_btn.pack(pady=20)
        
        self.log_btn = tk.Button(root, text="View Log", command=self.view_log)
        self.log_btn.pack(pady=5)
        
        self.input_file = None
        self.output_file = None
    
    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if self.input_file:
            messagebox.showinfo("Selected Input File", self.input_file)
    
    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")])
        if self.output_file:
            messagebox.showinfo("Selected Output File", self.output_file)
    
    def translate(self):
        if not self.input_file or not self.output_file:
            messagebox.showerror("Error", "Please select both input and output files.")
            return
        src_lang = self.src_lang_var.get()
        dest_lang = self.dest_lang_var.get()
        try:
            translate_document(self.input_file, self.output_file, src_lang=src_lang, dest_lang=dest_lang)
            messagebox.showinfo("Success", "Translation completed successfully!")
        except Exception as e:
            messagebox.showerror("Translation Failed", f"Translation failed: {str(e)}")

    def view_log(self):
        log_file = 'translation_errors.log'
        if os.path.exists(log_file):
            with open(log_file, 'r') as file:
                log_content = file.read()
            log_window = tk.Toplevel(self.root)
            log_window.title("Translation Log")
            log_text = tk.Text(log_window, wrap='word')
            log_text.insert('1.0', log_content)
            log_text.pack(expand=True, fill='both')
        else:
            messagebox.showinfo("Log", "No log file found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
