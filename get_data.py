import pandas as pd
import urllib.request, json
import requests
from datetime import datetime
import random

# reading url
json_file = dict()
with urllib.request.urlopen("https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json") as url:
    json_file = json.loads(url.read().decode())

# Get data from json file
data = json_file["securities"]['data']
# Get columns' name from json file
cols = list((json_file["securities"]["columns"]))
# Create DataFrame from the data and the columns
df = pd.DataFrame(data, columns=cols, dtype=None, copy=False)
good_column = ['SECID', 'SHORTNAME', 'PREVWAPRICE', 'YIELDATPREVWAPRICE', 'COUPONVALUE', 'NEXTCOUPON', 'FACEVALUE',
               'ISIN', 'COUPONPERIOD', 'FACEUNIT', 'BUYBACKPRICE', 'LOTVALUE', 'BUYBACKDATE']

for column in cols:
    if not (column in good_column):
        df = df.drop(column, 1)

df = df.dropna()

unique_names = list(set(df['SHORTNAME'].tolist()))[0:10]

mask = df['SHORTNAME'].isin(unique_names)
df = df[mask]
df.to_csv('dataset.csv', encoding='utf-8')
print(df)
# pd.set_option("display.max_columns",None)

chosen_bond = unique_names[random.randint(0, 9)] # User chooses in Telegram
print(chosen_bond)
current_bond = df[df["SHORTNAME"] == chosen_bond]
end_profit = float(current_bond["BUYBACKPRICE"]) - float(
    current_bond["PREVWAPRICE"])  # рассчитываем прибыль после выкупа облигации
end_profit = end_profit * 0.87 if end_profit > 0 else end_profit * 1  # учтем налог на прибыль
pd.set_option("display.max_columns", None)
days_befor_payback = int((datetime.strptime(str(current_bond['BUYBACKDATE'][current_bond.index[0]]),us
                                            "%Y-%m-%d") - datetime.strptime(str(datetime.now().date()),
                                                                            "%Y-%m-%d")).days)
from math import floor
price= current_bond["PREVWAPRICE"][current_bond.index[0]]
print(price)
print(type(price))
num_coupons = floor(days_befor_payback / current_bond["COUPONPERIOD"][current_bond.index[0]])
сoupon_profit = current_bond["COUPONVALUE"][current_bond.index[0]] * num_coupons
total_profit=end_profit + сoupon_profit
print(total_profit)
