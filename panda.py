import pandas as pd

df = pd.read_csv('bit28/28bit.csv')

print(df[df['available'] == 0].count())