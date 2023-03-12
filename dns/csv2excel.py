import pandas as pd
pd.read_csv('dns/dns.csv').to_excel('dns.xlsx', index=False)