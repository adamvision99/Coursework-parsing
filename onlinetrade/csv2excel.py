import pandas as pd
pd.read_csv('data/result.csv').to_excel('data/result.xlsx', index=False)