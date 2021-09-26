# -*- coding: utf-8 -*-
import pandas as pd;
from sklearn.impute import KNNImputer

class TratamentoNulo:
    dataset = None
    
    def executar_operacao(self, dataset):
        imputer = KNNImputer()
        columns = dataset.columns.values
        dataset_nan_filled = imputer.fit_transform(dataset)
        dataframe_nan_filled = pd.DataFrame(dataset_nan_filled, columns=columns)
        return dataframe_nan_filled
    
    def transformar(self, dataset):
        imputer = KNNImputer()
        columns = dataset.columns.values
        dataset_nan_filled = imputer.fit_transform(dataset)
        dataframe_nan_filled = pd.DataFrame(dataset_nan_filled, columns=columns)
        return dataframe_nan_filled