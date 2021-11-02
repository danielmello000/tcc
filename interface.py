# -*- coding: utf-8 -*-

import os
import tkinter
from tkinter import ttk, scrolledtext, filedialog
from ttkbootstrap import Style

class Interface(tkinter.Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title('Tratamento e Otimização de Datasets')
        self.style = Style('darkly')
        self.montar_interface()
        self.columns_dataset = []
        self.index_colunas_deletar = []
    
    def main(self):
        self.mainloop()
        
    def montar_interface(self):
        self.form = ttk.Frame(self)
        self.form.configure(padding=(20, 10))
        self.form.columnconfigure(1, weight=1)
        self.form.rowconfigure(8, weight=1)
        
        self.preencher_nulo = tkinter.IntVar(value=1, name='preencher_nulo')
        self.tratar_outliers = tkinter.IntVar(value=0, name='tratar_outliers')
        self.tratar_categoricos = tkinter.IntVar(value=0, name='tratar_categoricos')
        self.escalonar = tkinter.IntVar(value=0, name='escalonar')

        ttk.Label(self.form, text='Opções de tratamento').grid(row=0,column=0, pady=10)
        
        self.checkbox_nulos = ttk.Checkbutton(self.form, text="Preencher valores nulos", variable=self.preencher_nulo, 
                                              command=self.validar_opcoes_tratamento)
        self.checkbox_nulos.grid(row=1, column=0, sticky='ew', pady=(10, 5), padx=(0, 10))
        self.checkbox_outliers = ttk.Checkbutton(self.form, text="Deletar outliers", variable=self.tratar_outliers)
        self.checkbox_outliers.grid(row=2, column=0, sticky='ew', pady=5, padx=(0, 10))
        self.checkbox_encoder = ttk.Checkbutton(self.form, text="Converter atributos categóricos", variable=self.tratar_categoricos, 
                                                command=self.validar_opcoes_tratamento)
        self.checkbox_encoder.grid(row=3, column=0, sticky='ew', pady=5, padx=(0, 10))
        self.checkbox_escalonar = ttk.Checkbutton(self.form, text="Escalonar atributos", variable=self.escalonar)
        self.checkbox_escalonar.grid(row=4, column=0, sticky='ew', pady=(5, 10), padx=(0, 10))

        self.button_excluir_features = ttk.Button(self.form, text='Selecionar features a excluir', style='info.TButton', command=self.montar_checkbox_colunas)
        self.button_excluir_features.grid(row=5, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_procurar_dataset = ttk.Button(self.form, text='Procurar dataset...', style='info.TButton', command=self.procurar_dataset)
        self.button_procurar_dataset.grid(row=6, column=0, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_analisar = ttk.Button(self.form, text='Analisar', style='info.TButton', command=self.analisar)
        self.button_analisar.grid(row=6, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        self.button_processar = ttk.Button(self.form, text='Processar', style='info.TButton', command=self.processar)
        self.button_processar.grid(row=6, column=3, sticky='ew', pady=10, padx=(0, 10))
        
        ttk.Label(self.form, text='Saída').grid(row=7,column=0, pady=(10,5))
        self.log_box = scrolledtext.ScrolledText(self.form, width=100, height=10, state='disabled')
        self.log_box.grid(row=8, columnspan=4, sticky='n, s, e, w', pady=10, padx=(0, 10))
        
        self.button_limpar = ttk.Button(self.form, text='Limpar', style='info.TButton', command=self.limpar_log)
        self.button_limpar.grid(row=9, column=2, sticky='ew', pady=10, padx=(0, 10))
        
        self.gravar_log = ttk.Button(self.form, text='Salvar log', style='info.TButton', command=self.gravar_log)
        self.gravar_log.grid(row=9, column=3, sticky='ew', pady=10, padx=(0, 10))
        
        self.form.pack(fill='both', expand='yes')
        
        self.desabilitar_opcoes_tratamento()
        
    def montar_checkbox_colunas(self):
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
        
    def procurar_dataset(self):
        self.filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Selecione o arquivo",
                                          filetypes = (("Formatos aceitos",
                                                        ".csv .xlsx .data"),
                                                       ("all files",
                                                        "*.*")))
        if(self.filename):
            self.controller.receber_dataset(self.filename)
            
    def selecionar_colunas_excluir(self):
        self.index_colunas_deletar = list(self.list_box.curselection())
        print(self.index_colunas_deletar)
        self.validar_opcoes_tratamento()
        self.checkbox_window.destroy()
        
    def desabilitar_opcoes_tratamento(self):
        self.checkbox_nulos.configure(state = tkinter.DISABLED)
        self.checkbox_outliers.configure(state = tkinter.DISABLED)
        self.checkbox_encoder.configure(state = tkinter.DISABLED)
        self.checkbox_escalonar.configure(state = tkinter.DISABLED)
        self.button_excluir_features.configure(state = tkinter.DISABLED)
        self.button_analisar.configure(state = tkinter.DISABLED)
        self.button_processar.configure(state = tkinter.DISABLED)
    
    def habilitar_opcoes_tratamento(self):
        self.checkbox_nulos.configure(state = tkinter.NORMAL)
        self.checkbox_outliers.configure(state = tkinter.NORMAL)
        self.checkbox_encoder.configure(state = tkinter.NORMAL)
        self.button_excluir_features.configure(state = tkinter.NORMAL)
        self.button_analisar.configure(state = tkinter.NORMAL)
        self.button_processar.configure(state = tkinter.NORMAL)
        
    def validar_opcoes_tratamento(self):
        if self.preencher_nulo.get() == 0:
            self.tratar_outliers.set(0)
            self.checkbox_outliers.configure(state = tkinter.DISABLED)
            self.tratar_categoricos.set(0)
            self.checkbox_encoder.configure(state = tkinter.DISABLED)
            self.escalonar.set(0)
            self.checkbox_escalonar.configure(state = tkinter.DISABLED)
            
        else:
            self.checkbox_outliers.configure(state = tkinter.NORMAL)
            self.checkbox_encoder.configure(state = tkinter.NORMAL)
            
            if self.tratar_categoricos.get() == 0:
                self.escalonar.set(0)
                self.checkbox_escalonar.configure(state = tkinter.DISABLED)
            else:
                self.checkbox_escalonar.configure(state = tkinter.NORMAL)
    
    def analisar(self):
        self.button_excluir_features.configure(state = tkinter.DISABLED)
        self.button_analisar.configure(state = tkinter.DISABLED)
        self.button_processar.configure(state = tkinter.DISABLED)
        
        self.controller.analisar_dataset()
        
        self.button_excluir_features.configure(state = tkinter.NORMAL)
        self.button_analisar.configure(state = tkinter.NORMAL)
        self.button_processar.configure(state = tkinter.NORMAL)
        
    def processar(self):
        self.button_excluir_features.configure(state = tkinter.DISABLED)
        self.button_analisar.configure(state = tkinter.DISABLED)
        self.button_processar.configure(state = tkinter.DISABLED)
        
        self.controller.processar_dataset(self.preencher_nulo.get(), 
                                          self.tratar_outliers.get(), 
                                          self.tratar_categoricos.get(),
                                          self.escalonar.get())
        
        self.button_excluir_features.configure(state = tkinter.NORMAL)
        self.button_analisar.configure(state = tkinter.NORMAL)
        self.button_processar.configure(state = tkinter.NORMAL)
                
    def exibir_log(self, texto):
        self.log_box.configure(state = tkinter.NORMAL)
        self.log_box.insert(tkinter.INSERT, texto)
        self.log_box.insert(tkinter.INSERT, '\n')
        self.log_box.configure(state = tkinter.DISABLED)
        
    def limpar_log(self):
        self.log_box.configure(state = tkinter.NORMAL)
        self.log_box.delete('1.0', tkinter.END)
        self.log_box.configure(state = tkinter.DISABLED)    
                
    def gravar_log(self):
        f = open("log.txt", "w")
        f.write(self.log_box.get("1.0", tkinter.END))
        f.close()
        self.exibir_log('\nLog salvo em ' + os.getcwd() + '\log.txt')
