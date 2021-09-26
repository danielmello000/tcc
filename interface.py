# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk, scrolledtext, filedialog

from ttkbootstrap import Style
from interface_teste import InterfaceTeste

class Interface(tkinter.Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title('Tratamento e Otimização de Datasets')
        self.style = Style('darkly')
        self.montar_interface()
        self.columns_dataset = []
        self.index_colunas_deletar = []
        
    def montar_interface(self):
        self.form = ttk.Frame(self)
        self.form.configure(padding=(20, 10))
        self.form.columnconfigure(1, weight=1)
        self.form.rowconfigure(8, weight=1)

        # form variables
        self.name = tkinter.StringVar(value='', name='name')
        self.address = tkinter.StringVar(value='', name='address')
        self.phone = tkinter.StringVar(value='', name='phone')
        
        self.preencher_nulo = tkinter.IntVar(value=1, name='preencher_nulo')
        self.tratar_outliers = tkinter.IntVar(value=0, name='tratar_outliers')
        self.tratar_categoricos = tkinter.IntVar(value=0, name='tratar_categoricos')
        self.escalonar = tkinter.IntVar(value=0, name='escalonar')

        # form headers
        ttk.Label(self.form, text='Opções de tratamento').grid(row=0,column=0, pady=10)
        
        

        # create label/entry rows
        #for i, label in enumerate(['name', 'address', 'phone']):
        #    ttk.Label(self, text=label.title()).grid(row=i + 1, column=0, sticky='ew', pady=10, padx=(0, 10))
        #   ttk.Entry(self, textvariable=label).grid(row=i + 1, column=1, columnspan=2, sticky='ew')
        ttk.Checkbutton(self.form, text="Preencher valores nulos", variable=self.preencher_nulo).grid(row=1, column=0, sticky='ew', pady=(10, 5), padx=(0, 10))
        ttk.Checkbutton(self.form, text="Tratar outliers", variable=self.tratar_outliers).grid(row=2, column=0, sticky='ew', pady=5, padx=(0, 10))
        ttk.Checkbutton(self.form, text="Converter atributos categóricos", variable=self.tratar_categoricos).grid(row=3, column=0, sticky='ew', pady=5, padx=(0, 10))
        ttk.Checkbutton(self.form, text="Escalonar atributos", variable=self.escalonar).grid(row=4, column=0, sticky='ew', pady=(5, 10), padx=(0, 10))

        self.button_excluir_features = ttk.Button(self.form, text='Selecionar features a excluir', style='info.TButton', command=self.montar_checkbox_colunas)
        self.button_excluir_features.grid(row=5, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_procurar_dataset = ttk.Button(self.form, text='Procurar dataset...', style='info.TButton', command=self.procurar_dataset)
        self.button_procurar_dataset.grid(row=6, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_analisar = ttk.Button(self.form, text='Analisar', style='info.TButton', command=self.print_form_data)
        self.button_analisar.grid(row=6, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_processar = ttk.Button(self.form, text='Processar', style='info.TButton', command=self.print_form_data)
        self.button_processar.grid(row=6, column=3, sticky='ew', pady=10, padx=(0, 10))
        
        ttk.Label(self.form, text='Saída').grid(row=7,column=0, pady=(10,5))
        self.log_box = scrolledtext.ScrolledText(self.form, width=100, height=10, state='disabled')
        self.log_box.grid(row=8, columnspan=4, sticky='n, s, e, w', pady=10, padx=(0, 10))
        
        self.button_limpar = ttk.Button(self.form, text='Limpar', style='info.TButton', command=self.print_form_data)
        self.button_limpar.grid(row=9, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_processar = ttk.Button(self.form, text='Salvar como...', style='info.TButton', command=self.print_form_data)
        self.button_processar.grid(row=9, column=3, sticky='ew', pady=10, padx=(0, 10))

        # cancel button
        #self.cancel = ttk.Button(self, text='Cancel', style='danger.TButton', command=self.quit)
        #self.cancel.grid(row=6, column=1, sticky='ew')
        
        self.form.pack(fill='both', expand='yes')
        
    def main(self):
        self.mainloop()
        
    def procurar_dataset(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Selecione o arquivo",
                                          filetypes = (("Formatos aceitos",
                                                        ".csv .xlsx"),
                                                       ("all files",
                                                        "*.*")))
        if(self.filename):
            self.controller.receber_dataset(self.filename)
        
    def processar(self):
        self.controller.processar_dataset()
        
    def exibir_log(self, texto):
        self.log_box.configure(state ='normal')
        self.log_box.insert(tkinter.INSERT, texto)
        self.log_box.configure(state ='disabled')    
        
    def montar_checkbox_colunas(self):
        #CheckboxWindow()
        #InterfaceTeste(self.controller)
        self.checkbox_window = tkinter.Toplevel(self)
        self.checkbox_window.title("Selecionar Features")
        form = ttk.Frame(self.checkbox_window)
        form.configure(padding=(20, 10))
        form.columnconfigure(1, weight=1)
        form.rowconfigure(0, weight=1)
        
        self.list_box =  tkinter.Listbox(form, height=10, selectmode=tkinter.MULTIPLE, width=40)
        for column_name in self.columns_dataset:
            self.list_box.insert(tkinter.END, column_name)
            
        for idx in self.index_colunas_deletar:
            self.list_box.select_set(idx)
            
        self.list_box.grid(row=0,columnspan=3,sticky='nesw')
        
        button_selecionar = ttk.Button(form, text='Selecionar', style='info.TButton', command=self.selecionar_colunas_excluir)
        button_selecionar.grid(row=1, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        button_cancelar = ttk.Button(form, text='Cancelar', style='info.TButton', command=self.checkbox_window.destroy)
        button_cancelar.grid(row=1, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        form.pack(fill='both', expand='yes')

    def selecionar_colunas_excluir(self):
        self.index_colunas_deletar = self.list_box.curselection()
        self.checkbox_window.destroy()
        

    def print_form_data(self):
        pass