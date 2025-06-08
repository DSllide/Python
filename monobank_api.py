from json import loads as jloads
from datetime import datetime
from requests import get

def timenow():
    return datetime.today().strftime("%B %d %H:%M:%S")

def get_currency():
    try:
        response = get("https://api.monobank.ua/bank/currency")
        data = response.text
        if "errorDescription" not in data:
            with open("currency.json", "w", encoding="utf-8") as f:
                f.write(data)
            print(f'{timenow()}: Done')
        else:
            print(f'{timenow()}: Error in response')
    except Exception as e:
        print(f'{timenow()}: Request failed — {e}')

def print_currency():
    try:
        with open("currency.json", "r", encoding="utf-8") as f:
            cur = jloads(f.read())

        res = 'Купівля/Продаж'

        for item in cur:
            if item["currencyCodeA"] == 840 and item["currencyCodeB"] == 980:
                res += f'\nUSD: {item["rateBuy"]}/{item["rateSell"]}'
            if item["currencyCodeA"] == 978 and item["currencyCodeB"] == 980:
                res += f'\nEUR: {item["rateBuy"]}/{item["rateSell"]}'

        return res if res != 'Купівля/Продаж' else 'Не знайдено курсів валют.'
    except Exception as e:
        return f'Помилка читання файлу: {e}'

get_currency()
print(print_currency())
