# -*- coding: utf-8 -*-

import os
import pandas as pd;
from operacoes import TratamentoNulo, TratamentoOutlier, TratamentoEscala, TratamentoEncoder
from interface import Interface

class Controller:
    def __init__(self):
        self.view = Interface(self)
        
    def receber_dataset(self, filename):
        if filename:
            self.filename = filename
            file_extension = filename.split('.').pop()
            
            if file_extension == 'csv':
                self.dataset = pd.read_csv(filename)
            elif file_extension == 'xlsx':
                self.dataset = pd.read_excel(filename)
            else:
                self.enviar_log('Formato de arquivo inválido!')
                self.dataset = None
                
            self.original_dataset = self.dataset
                
            if self.dataset is not None:
                self.view.columns_dataset = self.dataset.columns.values
                self.enviar_log('Arquivo ' + filename + ' carregado com sucesso.')
                self.view.habilitar_opcoes_tratamento()
            else:
                self.view.columns_dataset = []
                
            self.view.index_colunas_deletar = []
    
    def enviar_log(self, msg):
        self.view.exibir_log(msg)
        
    def analisar_dataset(self):
        self.enviar_log('\nIniciando análise do dataset:\n')
        
        qt_rows = len(self.dataset.index)
        qt_columns = len(self.dataset.columns)
        
        qt_rows_missing = self.dataset.isnull().any(axis=1).sum()
        self.enviar_log(f'Dos {qt_rows} registros, {qt_rows_missing} possuem valores faltantes ' \
                        f'({round((qt_rows_missing / qt_rows) * 100, 2)}% do total)')
        
        qt_columns_missing = self.dataset.isnull().any(axis=0).sum()
        self.enviar_log(f'Das {qt_columns} features, {qt_columns_missing} possuem valores faltantes ' \
                        f'({round((qt_columns_missing / qt_columns) * 100, 2)}% do total)')

        self.enviar_log('\nInformações detalhadas das features:')
        
        columns = self.dataset.columns.values
        for col_name in columns:
            n_missing = self.dataset[col_name].isnull().sum()
            self.enviar_log(f'{col_name}: {n_missing} registros faltantes' \
                            f'({round((n_missing / qt_rows) * 100, 2)}% do total de registros)')

    def processar_dataset(self, tratar_nulos, tratar_outliers, transformar_categoricos, escalonar):
        
        # instanciando os objetos das operações
        
        null_imputer = TratamentoNulo()
        delete_outliers = TratamentoOutlier();
        encoder = TratamentoEncoder()
        tratamento_escala = TratamentoEscala()
        
        # dropando colunas
        self.dataset.drop(self.dataset.columns[self.view.index_colunas_deletar], axis=1, inplace = True)
        
        # dropando linhas e colunas completamente vazias
        self.dataset = self.null_imputer.eliminar_totalmente_vazios(self.dataset)
        
        # pegando os nomes das colunas categóricas e numéricas
        datatype = self.dataset.dtypes
        cat_columns = datatype[(datatype == 'object') | (datatype == 'category')].index.tolist()
        other_columns = datatype[(datatype != 'object') & (datatype != 'category')].index.tolist()
        
        # dividindo o dataframe entre features categóricas e numericas
        df_cat = self.dataset[cat_columns]
        df_others = self.dataset[other_columns]
        
        # preenchendo os nulos da parte categórica com a moda
        df_cat = df_cat.fillna(df_cat.mode().iloc[0])
         
        # juntando o dataframe com as duas partes
        self.dataset = pd.concat([df_cat, df_others], axis=1)       

        # transformando os valores categóricos em numéricos
        self.dataset = encoder.executar_operacao(self.dataset);
        
        # imputando os valores nulos com o knn imputer
        self.dataset = null_imputer.executar_operacao(self.dataset);
                
        # detectando outliers
        if tratar_outliers:
            self.dataset = delete_outliers.executar_operacao(self.dataset, encoder.ohe_cat_columns, encoder.other_columns);
        
        #revertendo o one hot encoder caso necessário
        if not transformar_categoricos:
            self.dataset = encoder.desfazer_operacao(self.dataset)
        
        # normalização (escala de 0 a 1)
        if escalonar:
            self.dataset = tratamento_escala.executar_operacao(self.dataset)
        
        print('---------- resultado final ---------------')
        print(self.dataset)
        self.gravar_dataset()
        
        self.dataset = self.original_dataset
        
    def gravar_dataset(self):
        file_extension = self.filename.split('.').pop()
        
        if file_extension == 'csv':
            self.dataset.to_csv('processed_dataset.csv', index=False)
        elif file_extension == 'xlsx':
            self.dataset.to_excel('processed_dataset.xlsx', index=False)
            
        self.enviar_log('Arquivo salvo em ' + os.getcwd() + '\processed_dataset.' + file_extension)
        
    def main(self):
        self.view.main()

if __name__ == '__main__':
    program = Controller()
    program.main()