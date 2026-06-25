import pandas as pd

df = pd.read_excel("data/raw_kraz.xlsx")
print(df.columns.tolist())