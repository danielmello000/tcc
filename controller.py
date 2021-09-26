# -*- coding: utf-8 -*-

import pandas as pd;
from operacoes import TratamentoNulo, TratamentoOutlier, TratamentoEscala, TratamentoEncoder
from interface import View

class Controller:
    def __init__(self):
        self.view = View(self)

    def gravar_dataset(self):
        self.dataset.to_csv('transformed_dataset.csv', index=False)
    
    def processar_dataset(self):
        colunas_deletar = []
        tratar_nulos = True        # necessário para todas as outras operações
        tratar_outliers = True     
        transformar_categoricos = True   # necessário para o escalonamento
        escalonar = False
        
        # instanciando os objetos das operações
        
        null_imputer = TratamentoNulo()
        delete_outliers = TratamentoOutlier();
        encoder = TratamentoEncoder()
        tratamento_escala = TratamentoEscala()
        
        # lendo o dataset
        #dataset = pd.read_csv('MOCK_DATA.csv')
        dataset = pd.read_csv('MOCK_DATA_sem_nome_null.csv')
        
        # dropando colunas
        dataset.drop(colunas_deletar, axis=1, inplace = True)
        
        # dropando registros que estão completamente vazios
        dataset.dropna(how = 'all', inplace = True)
        print(dataset)
        
        # pegando os nomes das colunas categóricas e numéricas
        datatype = dataset.dtypes
        cat_columns = datatype[(datatype == 'object') | (datatype == 'category')].index.tolist()
        other_columns = datatype[(datatype != 'object') & (datatype != 'category')].index.tolist()
        
        # dividindo o dataframe entre features categóricas e numericas
        df_cat = dataset[cat_columns]
        df_others = dataset[other_columns]
        
        # preenchendo os nulos da parte categórica com a moda
        df_cat = df_cat.fillna(df_cat.mode().iloc[0])
        
        # juntando o dataframe com as duas partes
        dataset = pd.concat([df_cat, df_others], axis=1)
    
        # transformando os valores categóricos em numéricos
        dataset = encoder.executar_operacao(dataset);
        
        # imputando os valores nulos com o knn imputer
        dataset = null_imputer.executar_operacao(dataset);
        
        # detectando outliers
        if tratar_outliers:
            dataset = delete_outliers.executar_operacao(dataset, encoder.ohe_cat_columns, encoder.other_columns);
        
        #revertendo o one hot encoder caso necessário
        if not transformar_categoricos:
            dataset = encoder.desfazer_operacao(dataset)
        
        # normalização (escala de 0 a 1)
        if escalonar:
            dataset = tratamento_escala.executar_operacao(dataset)
        
        print('---------- resultado final ---------------')
        print(dataset)
        self.dataset = dataset
        self.gravar_dataset()
        
    def main(self):
        #self.processar_dataset()
        self.view.main()

if __name__ == '__main__':
    program = Controller()
    program.main()