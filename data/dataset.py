import pandas as pd

class Dataset:

    def __init__(self, path: str):
        self.dataset = pd.read_csv(path)

    def getDataset(self) -> pd.DataFrame:
        return self.dataset

    def setDataset(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def dropColumns(self, columns):
        self.dataset = self.dataset.drop(columns=columns)

    def save(self, path: str):
        self.dataset.to_csv(path, index=False)