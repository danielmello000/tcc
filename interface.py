# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk, scrolledtext

from ttkbootstrap import Style


class View(tkinter.Tk):

    def __init__(self, controller):
        super().__init__()
        self.title('Tratamento e Otimização de Datasets')
        self.style = Style('darkly')
        self.form = Interface(self)
        self.form.pack(fill='both', expand='yes')
        
    def main(self):
        self.mainloop()

class Interface(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=(20, 10))
        self.columnconfigure(1, weight=1)
        self.rowconfigure(8, weight=1)

        # form variables
        self.name = tkinter.StringVar(value='', name='name')
        self.address = tkinter.StringVar(value='', name='address')
        self.phone = tkinter.StringVar(value='', name='phone')
        
        self.preencher_nulo = tkinter.IntVar(value=1, name='preencher_nulo')
        self.tratar_outliers = tkinter.IntVar(value=0, name='tratar_outliers')
        self.tratar_categoricos = tkinter.IntVar(value=0, name='tratar_categoricos')
        self.escalonar = tkinter.IntVar(value=0, name='escalonar')

        # form headers
        ttk.Label(self, text='Opções de tratamento').grid(row=0,column=0, pady=10)
        
        

        # create label/entry rows
        #for i, label in enumerate(['name', 'address', 'phone']):
        #    ttk.Label(self, text=label.title()).grid(row=i + 1, column=0, sticky='ew', pady=10, padx=(0, 10))
        #   ttk.Entry(self, textvariable=label).grid(row=i + 1, column=1, columnspan=2, sticky='ew')
        ttk.Checkbutton(self, text="Preencher valores nulos", variable=self.preencher_nulo).grid(row=1, column=0, sticky='ew', pady=(10, 5), padx=(0, 10))
        ttk.Checkbutton(self, text="Tratar outliers", variable=self.tratar_outliers).grid(row=2, column=0, sticky='ew', pady=5, padx=(0, 10))
        ttk.Checkbutton(self, text="Converter atributos categóricos", variable=self.tratar_categoricos).grid(row=3, column=0, sticky='ew', pady=5, padx=(0, 10))
        ttk.Checkbutton(self, text="Escalonar atributos", variable=self.escalonar).grid(row=4, column=0, sticky='ew', pady=(5, 10), padx=(0, 10))

        self.button_excluir_features = ttk.Button(self, text='Selecionar features a excluir', style='info.TButton', command=self.print_form_data)
        self.button_excluir_features.grid(row=5, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_procurar_dataset = ttk.Button(self, text='Procurar dataset...', style='info.TButton', command=self.print_form_data)
        self.button_procurar_dataset.grid(row=6, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_analisar = ttk.Button(self, text='Analisar', style='info.TButton', command=self.print_form_data)
        self.button_analisar.grid(row=6, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_processar = ttk.Button(self, text='Processar', style='info.TButton', command=self.print_form_data)
        self.button_processar.grid(row=6, column=3, sticky='ew', pady=10, padx=(0, 10))
        
        ttk.Label(self, text='Saída').grid(row=7,column=0, pady=(10,5))
        self.log_box = scrolledtext.ScrolledText(self, width=100, height=10).grid(row=8, columnspan=4, sticky='n, s, e, w', pady=10, padx=(0, 10))
        
        self.button_limpar = ttk.Button(self, text='Limpar', style='info.TButton', command=self.print_form_data)
        self.button_limpar.grid(row=9, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_processar = ttk.Button(self, text='Salvar como...', style='info.TButton', command=self.print_form_data)
        self.button_processar.grid(row=9, column=3, sticky='ew', pady=10, padx=(0, 10))

        # cancel button
        #self.cancel = ttk.Button(self, text='Cancel', style='danger.TButton', command=self.quit)
        #self.cancel.grid(row=6, column=1, sticky='ew')

    def print_form_data(self):
        print(self.name.get(), self.address.get(), self.phone.get())
        