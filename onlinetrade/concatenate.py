import pandas as pd

df1 = pd.read_csv('data/result.csv')
df2 = pd.read_csv('result.csv')

df1 = pd.concat([df1, df2], ignore_index=True)

df1.to_csv('data/result.csv', index=False)