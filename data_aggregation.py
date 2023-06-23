import pandas as pd

baguette_prices = pd.read_csv('datasets/baguette.csv', delimiter=';')
baguette = baguette_prices.drop(columns='Codes')

camambert_prices = pd.read_csv('datasets/camambert.csv', delimiter=';')
camambert = camambert_prices.drop(columns='Codes')

wine = pd.read_csv('datasets/vin.csv', delimiter=';')

food_dataframe = pd.merge(wine, camambert, on='period')
food_dataframe = pd.merge(food_dataframe, baguette, on='period')

food_dataframe = food_dataframe[0:-1]

# giving different weights
food_dataframe["vin_baguette_fromage_index"] = food_dataframe["wine_price"].astype(float) / 30 \
    + food_dataframe["camambert_price"].astype(float) / 10 \
    + food_dataframe["baguette_price"].astype(float) / 3

food_dataframe.dropna(inplace=True)

vin_baguette_fromage_index = food_dataframe.drop(columns=['wine_price', 'camambert_price', 'baguette_price'])


def quarter_replacement_for_index(date_value):
    replacements = {
        '02': 'T1',
        '05': 'T2',
        '08': 'T3',
        '11': 'T4'
    }
    if date_value.split('-')[1] in replacements.keys():
        return date_value.split('-')[0] + replacements[date_value.split('-')[1]]
    return '0'


vin_baguette_fromage_index['period'] = vin_baguette_fromage_index['period'].apply(quarter_replacement_for_index)
vin_baguette_fromage_index = vin_baguette_fromage_index[vin_baguette_fromage_index['period'] != '0']

gdp = pd.read_csv('datasets/GDP.csv', delimiter=';')[['PIB', 'period']]

merged_df = gdp.merge(vin_baguette_fromage_index, on='period', how='left')

politics = pd.read_csv('datasets/politique.csv', delimiter=';')
politics = politics[['period', 'axe_politique']]
politics['period'] = politics['period'].apply(quarter_replacement_for_index)
politics = politics[politics['period'] != '0']

merged_df = merged_df.merge(politics)
print(merged_df)