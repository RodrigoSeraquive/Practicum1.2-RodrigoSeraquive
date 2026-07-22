import pandas as pd

df = pd.read_csv("data_raw/bce/crecimiento-anual-pib.csv")
print(df.columns.tolist())
print(df.head(10))
print(df.dtypes)
print(df.isnull().sum())