# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Text
from tkinter import scrolledtext
from ttkbootstrap import Style

class Interface:
    
    def __init__(self, controller):
        self.controller = controller
        self.montar_interface()
        
    def montar_interface(self):
        self._make_window()
        self._make_frame()
        
    def _make_window(self):
        self.style = Style(theme='litera')
        self.root = self.style.master
        self.root.title("Otimizador Datasets")
        
    def _make_frame(self):
        
        
        # style.configure("BW.TLabel", foreground="blue", background="gray")
        self.frame = ttk.Frame(self.root)
        self.frame.place(relwidth=1, relheight=1)
        
        c1 = ttk.Button(self.frame, text = "Procurar dataset...", 
                        style="primary.TButton")
        c1.pack()
        
        self.button1 = ttk.Button(self.frame, text="Teste", command= self._enviar,
                                  style='danger.Outline.TButton', )
        self.button1.pack()
        
        
        
        self.log_box = scrolledtext.ScrolledText(self.frame, width=30, height=8)
        self.log_box.configure(state ='disabled')
        self.log_box.pack()
        
    def _enviar(self):
        self.controller.testePassagem()
        
    def exibir_log(self, texto):
        self.log_box.configure(state ='normal')
        self.log_box.insert(tk.INSERT, texto)
        self.log_box.configure(state ='disabled')
        
    def main(self):
        self.root.mainloop()