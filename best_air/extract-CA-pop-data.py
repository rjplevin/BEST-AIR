import pandas as pd

input  = '/Volumes/Plevin1TB/BEST-AIR/data/pop-by-tract/censustract-00-10.csv'
output = '/Volumes/Plevin1TB/BEST-AIR/data/pop-by-tract/censustract-CA-2010.csv'

df = pd.read_csv(input, usecols=['GEOID', 'ST10', 'POP10'], dtype={'GEOID': str, 'ST10': str})
ca_df = df.query("ST10 == '06'")[['GEOID', 'POP10']]    # filter by CA state code ('06') and extract just 2 columns

# population values have commas that we need to remove to convert to int
ca_df['POP2010'] = ca_df.POP10.str.replace(',', '').astype(int)
ca_df.drop('POP10', axis='columns', inplace=True)

ca_df.to_csv(output, index=False)
