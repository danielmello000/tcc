from pyod.models.knn import KNN

class TratamentoOutlier:

    def executar_operacao(self, dataset):
        
        detector = KNN()
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
    