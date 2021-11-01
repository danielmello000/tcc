from pyod.models.knn import KNN

class TratamentoOutlier:

    def executar_operacao(self, dataset, ohe_cat_columns, other_columns):
        
        if other_columns:
            # Pegando a parte numérica do dataset
            df_others = dataset[other_columns]
            
            detector = KNN()
            detect_only_numeric = False
            if detect_only_numeric:
                detector.fit(df_others)
            else:
                detector.fit(dataset)
            
            previsoes = detector.labels_

            # pega os indices dos outliers
            indexes_outliers = [i for i,x in enumerate(previsoes) if x == 1]
            
            self.qt_outliers = len(indexes_outliers)
            
            # dropa os outliers
            dataset.drop(indexes_outliers, inplace = True)
            
            # resetando os indices das rows para não dar conflitos caso o ohe seja revertido
            dataset.reset_index(drop=True, inplace=True)
            
        return dataset
    
    
    