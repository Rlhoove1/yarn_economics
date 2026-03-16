# NOT seasonaly adjusted 
#retrieved from BLS  https://data.bls.gov/dataViewer/view/timeseries/LNU03000000 
df = pd.read_csv('/content/unemp.csv')

#take the last 3 chars of Label
df["Month"] = df["Label"].str[-3:]

#make months as colnames, year as row names and ony keep Value 
df_wide = df.pivot(index="Year", columns="Month", values="Value")

df_wide.to_csv("unemployment_not_seasonaly_adj.csv")
