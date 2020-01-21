import pandas as pd

csv = '../csv/txt_data.csv'
df = pd.read_csv(csv)

# print(df['text'])
text = df['text']

string = ""
for article in text:
  string += article
  
print(string)
