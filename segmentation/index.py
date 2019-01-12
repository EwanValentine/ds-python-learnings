import pandas as pd
import warnings
import datetime as dt
NOW = dt.datetime(2011, 12, 10)


"""
Customer segmentation
"""

warnings.filterwarnings('ignore')

# Load excel data into a 'data frame'
df = pd.read_excel("online.xlsx")
df.head()

df1 = df

# Get rid of duplicate countries
none_unique = df1.Country.nunique()

# Get unique countries?
unique = df1.Country.unique()

# Get all customers from the UK
df1 = df1.loc[df1['Country'] == 'United Kingdom']

# Check whether there are 0 values in each column
df1.isnull().sum(axis=0)

df1 = df1[pd.notnull(df1['CustomerID'])]
df1.Quantity.min()

# Remove negative values from quantity col
df1 = df1[(df1['Quantity'] > 0)]
df1.shape
df1.info()

# Check unique values for each column
def unique_counts(df1):
   for i in df1.columns:
       count = df1[i].nunique()
       print(i, ": ", count)

unique_counts(df1)

# Add a column for the total
df1['TotalPrice'] = df1['Quantity'] * df1['UnitPrice']

# Convert invoice date to datetime
df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])

# Find out the first order date
df1['InvoiceDate'].min()

# Find the most recent order date
df1['InvoiceDate'].max()

# Group by CustomerID, aggregate by invoice date, invoice no and total price
rfmTable = df1.groupby('CustomerID').agg({
  'InvoiceDate': lambda x: (NOW - x.max()).days,
  'InvoiceNo': lambda x: len(x),
  'TotalPrice': lambda x: x.sum(),
})

# Convert InvoiceDate to int, for some reason? 
rfmTable['InvoiceDate'] = rfmTable['InvoiceDate'].astype(int)

# Rename the columns to more user friendly column names
rfmTable.rename(columns={
  'InvoiceDate': 'recency',
  'InvoiceNo': 'frequency',
  'TotalPrice': 'monetary_value'
}, inplace=True)

rfmTable.head()

first_customer = df1[df1['CustomerID'] == 12346.0]
first_customer

quantiles = rfmTable.quantile(q=[0.25, 0.5, 0.75])
quantiles = quantiles.to_dict()

segmented_rfm = rfmTable

def RScore(x, p, d):
  if x <= d[p][0.25]:
    return 1
  elif x <= d[p][0.50]:
    return 2
  elif x <= d[p][0.75]:
    return 3
  else:
    return 4

def FMScore(x, p, d):
  if x <= d[p][0.25]:
    return 4
  elif x <= d[p][0.50]:
    return 3
  elif x <= d[p][0.75]:
    return 2
  else:
    return 1

segmented_rfm['r_quantile'] = segmented_rfm['recency'].apply(RScore, args=('recency', quantiles,))
segmented_rfm['f_quantile'] = segmented_rfm['frequency'].apply(FMScore, args=('frequency', quantiles,))
segmented_rfm['monetary_value'] = segmented_rfm['monetary_value'].apply(FMScore, args=('monetary_value', quantiles,))

segmented_rfm['RFMScore'] = segmented_rfm.r_quantile.map(str)
+ segmented_rfm.f_quantile.map(str)
+ segmented_rfm.r_quantile.map(str)

segmented_rfm.head()

segmented_rfm[segmented_rfm['RFMScore'] == '111'].sort_values(
    'monetary_value', ascending=False).head(10)
