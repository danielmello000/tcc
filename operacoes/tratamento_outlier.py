# -*- coding: utf-8 -*-
from pyod.models.knn import KNN

class TratamentoOutlier:
    def dividir_colunas(self, dataset):
        datatype = dataset.dtypes
        cat_columns = datatype[(datatype == 'object') | (datatype == 'category')].index.tolist()
        other_columns = datatype[(datatype != 'object') & (datatype != 'category')].index.tolist()
        
        return cat_columns, other_columns
    
    # def executar_operacao(self, dataset):
    #     self.cat_columns, other_columns = self.dividir_colunas(dataset)
        
    #     # dividindo o dataframe entre features categóricas e numericas
    #     df_cat = dataset[self.cat_columns]
    #     df_others = dataset[other_columns]
        
    #     detector = KNN()
    #     detector.fit(df_others)
        
    #     previsoes = detector.labels_
    #     print('-- previsões outliers ---')
    #     print(previsoes)
    #     #print(detector.decision_scores_)
    #     #print(dataset)
        
    #     # pega os indices dos outliers
    #     indexes_outliers = [i for i,x in enumerate(previsoes) if x == 1]
    #     print("Índices dos registros identificados como outliers: ")
    #     print(indexes_outliers)
        
    #     # dropa os outliers
    #     dataset.drop(indexes_outliers, inplace = True)
        
    #     # resetando os indices das rows para não dar conflitos caso o ohe seja revertido
    #     dataset.reset_index(drop=True, inplace=True)
    #     return dataset
    
    def executar_operacao(self, dataset, ohe_cat_columns, other_columns):
        
        # dividindo o dataframe entre features categóricas e numericas
        df_cat = dataset[ohe_cat_columns]
        df_others = dataset[other_columns]
        
        detector = KNN()
        detector.fit(df_others)
        
        previsoes = detector.labels_
        print('-- previsões outliers ---')
        print(previsoes)
        #print(detector.decision_scores_)
        #print(dataset)
        
        # pega os indices dos outliers
        indexes_outliers = [i for i,x in enumerate(previsoes) if x == 1]
        print("Índices dos registros identificados como outliers: ")
        print(indexes_outliers)
        
        # dropa os outliers
        dataset.drop(indexes_outliers, inplace = True)
        return dataset