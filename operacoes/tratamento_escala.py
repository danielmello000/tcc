# -*- coding: utf-8 -*-
import pandas as pd;
from sklearn.preprocessing import MinMaxScaler

class TratamentoEscala:
    dataset = None
    
    def executar_operacao(self, dataset):
        columns = dataset.columns.values
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(dataset)
        dataset = pd.DataFrame(scaled, columns=columns)
        return dataset
        