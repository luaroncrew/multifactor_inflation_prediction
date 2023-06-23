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
    try:
        if date_value.split('-')[1] in replacements.keys():
            return date_value.split('-')[0] + replacements[date_value.split('-')[1]]
        return '0'
    except Exception as e:
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


cpi_change = pd.read_csv('datasets/CPI.csv', delimiter='  ')
cpi_change['Date'] = pd.to_datetime(cpi_change['Date'])
cpi_change['period'] = cpi_change['Date'].astype(str).apply(quarter_replacement_for_index)
cpi_change = cpi_change[['period', 'cpi_change']]
merged_df = merged_df.merge(cpi_change).drop_duplicates(subset='period', keep='first')

energy_prices = pd.read_csv('datasets/gaz.csv', delimiter=';')
energy_prices['period'] = energy_prices['period'].apply(quarter_replacement_for_index)
energy_prices = energy_prices[['period', 'gas_price']]

merged_df = merged_df.merge(energy_prices, on='period')

tourists = pd.read_csv('datasets/tourisme.csv', delimiter=',')
tourists = tourists.T
tourists['period'] = tourists.index
tourists['period'] = tourists['period'].apply(quarter_replacement_for_index)
tourists = tourists[tourists['period'] != '0']


def modify_tourists(value: str):
    try:
        if len(value.split()) > 1:
            number = value.split()[0]
            return int(number)
        return 0
    except Exception as e:
        return 0


tourists['tourists_number'] = tourists[0].apply(modify_tourists)
tourists = tourists[['period', 'tourists_number']]

merged_df = merged_df.merge(tourists, on='period')

treasury = pd.read_csv('datasets/cac40.csv')
treasury['CAC40'] = treasury['Open']
treasury['period'] = treasury['Date'].astype(str).apply(quarter_replacement_for_index)
treasury = treasury[treasury['period'] != '0']
treasury = treasury[['CAC40', 'period']]

merged_df = merged_df.merge(treasury, on='period')

dette = pd.read_csv('datasets/dette.csv')
dette = dette.T
dette['period'] = dette.index
dette['dette'] = dette[0]
dette = dette[['period', 'dette']]

merged_df = merged_df.merge(dette, on='period')

unemployment = pd.read_csv('datasets/chomage.csv', delimiter=';')

merged_df = merged_df.merge(unemployment, on='period')

inflation = pd.read_csv('datasets/inflation.csv')
merged_df = merged_df.merge(inflation, on='period')

merged_df.to_csv('big_inflation_dataset.csv')
