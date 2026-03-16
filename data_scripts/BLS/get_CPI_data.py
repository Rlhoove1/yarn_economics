# got CPI data from here https://data.bls.gov/timeseries/CUUR0000SA0

import pandas as pd

# Load the CPI data, without nonense header and set months to be headers 
df = pd.read_excel('/content/CPI_retrived_march_5.xlsx',skiprows=10)
df.columns = df.iloc[0]
df = df.drop(0)
df = df.reset_index(drop=True)
