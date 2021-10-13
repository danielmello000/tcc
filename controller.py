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
            try:
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
                
            except Exception as e:
                self.enviar_log('\nOcorreu um erro ao ler o arquivo:')
                self.enviar_log(e)
                
    
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
        delete_outliers = TratamentoOutlier()
        encoder = TratamentoEncoder()
        tratamento_escala = TratamentoEscala()
        
        # dropando colunas
        self.dataset.drop(self.dataset.columns[self.view.index_colunas_deletar], axis=1, inplace = True)
        
        # dropando linhas e colunas completamente vazias
        try:
            self.dataset = null_imputer.eliminar_totalmente_vazios(self.dataset)
        except Exception as e:
            self.enviar_log('\nOcorreu um erro ao eliminar os registros e features totalmente vazios:')
            self.enviar_log(e)
        
        if tratar_nulos:    # Obrigatório para as demais operações
        
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
            try:
                self.dataset = encoder.executar_operacao(self.dataset)
            except Exception as e:
                self.enviar_log('\nOcorreu um erro ao efetuar o encoder de valores categóricos:')
                self.enviar_log(e)
            
            # imputando os valores nulos com o knn imputer
            try:
                self.dataset = null_imputer.executar_operacao(self.dataset)
            except Exception as e:
                self.enviar_log('\nOcorreu um erro ao imputar valores nulos:')
                self.enviar_log(e)
                    
            # detectando outliers
            if tratar_outliers:
                try:
                    self.dataset = delete_outliers.executar_operacao(self.dataset, encoder.ohe_cat_columns, encoder.other_columns)
                except Exception as e:
                    self.enviar_log('\nOcorreu um erro no tratamento de outliers:')
                    self.enviar_log(e)
            
            #revertendo o one hot encoder caso necessário
            if not transformar_categoricos:
                try:
                    self.dataset = encoder.desfazer_operacao(self.dataset)
                except Exception as e:
                    self.enviar_log('\nOcorreu um erro ao desfazer o encoder de valores categóricos:')
                    self.enviar_log(e)
            
            # normalização (escala de 0 a 1)
            if escalonar:
                try:
                    self.dataset = tratamento_escala.executar_operacao(self.dataset)
                except Exception as e:
                    self.enviar_log('\nOcorreu um erro ao efetuar o escalonamento:')
                    self.enviar_log(e)
        
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
            
        self.enviar_log('\nArquivo salvo em ' + os.getcwd() + '\processed_dataset.' + file_extension)
        
    def main(self):
        self.view.main()

if __name__ == '__main__':
    program = Controller()
    program.main()