import pandas as pd;
from sklearn.preprocessing import OneHotEncoder

class TratamentoEncoder:
    dataset = None
    
    def dividir_colunas(self, dataset):
        datatype = dataset.dtypes
        cat_columns = datatype[(datatype == 'object') | (datatype == 'category')].index.tolist()
        other_columns = datatype[(datatype != 'object') & (datatype != 'category')].index.tolist()
        
        return cat_columns, other_columns
    
    def executar_operacao(self, dataset):
        self.cat_columns, self.other_columns = self.dividir_colunas(dataset)
        
        # dividindo o dataframe entre features categóricas e numericas
        df_cat = dataset[self.cat_columns]
        df_others = dataset[self.other_columns]
        
        # aplicando one hot encoder na parte categórica e remontando o resultado em um dataframe
        self.ohe = OneHotEncoder(sparse=False)
        result = self.ohe.fit_transform(df_cat.astype(str))
        self.ohe_cat_columns = self.ohe.get_feature_names(self.cat_columns)
        df_cat_ohe = pd.DataFrame(result, columns=self.ohe_cat_columns)
        
        # juntando o dataframe com as duas partes
        dataset = pd.concat([df_cat_ohe, df_others], axis=1)
        
        return dataset
    
    def desfazer_operacao(self, dataset):
        
        df_cat = dataset[self.ohe_cat_columns]
        df_others = dataset[self.other_columns]
        dt_cat_reversed = self.ohe.inverse_transform(df_cat)
        df_cat_reversed = pd.DataFrame(dt_cat_reversed, columns=self.cat_columns)
        reversed_dataset = pd.concat([df_cat_reversed, df_others], axis=1)
        return reversed_dataset
    
    
    