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
    
    def eliminar_totalmente_vazios(self, dataset):
        # dropando colunas completamente vazias
        qt_cols = len(dataset.columns)
        dataset.dropna(how='all', axis=1, inplace=True)
        self.qt_deleted_cols = qt_cols - len(dataset.columns)
        
        # dropando registros que estão completamente vazios
        qt_rows = len(dataset.index)
        dataset.dropna(how = 'all', inplace = True)
        self.qt_deleted_rows = qt_rows - len(dataset.index)
        
        return dataset
