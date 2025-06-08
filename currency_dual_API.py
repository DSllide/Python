from fastapi import FastAPI, Query
from typing import List, Optional
from datetime import datetime
import requests

app = FastAPI(title="Currency API", description="API для отримання курсів валют з Monobank та PrivatBank")


currency_iso = {
    "UAH": 980, "USD": 840, "EUR": 978, "GBP": 826,
    "CNY": 156, "PLN": 985, "CHF": 756, "CZK": 203,
    "BGN": 975, "CAD": 124
}


def get_monobank_data():
    try:
        response = requests.get("https://api.monobank.ua/bank/currency", timeout=5)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    return []


@app.get("/monobank", summary="Курси валют з Monobank")
def get_currency_pairs(
        base: Optional[List[str]] = Query(default=None, description="Базові валюти (наприклад: USD, EUR)"),
        quote: Optional[List[str]] = Query(default=["UAH"], description="Валюти котирування")
):
    data = get_monobank_data()
    result = []

    base_codes = [currency_iso[b] for b in base if b in currency_iso] if base else None
    quote_codes = [currency_iso[q] for q in quote if q in currency_iso] if quote else None

    for entry in data:
        code_a = entry.get("currencyCodeA")
        code_b = entry.get("currencyCodeB")

        if base_codes and code_a not in base_codes:
            continue
        if quote_codes and code_b not in quote_codes:
            continue

        base_code = next((k for k, v in currency_iso.items() if v == code_a), str(code_a))
        quote_code = next((k for k, v in currency_iso.items() if v == code_b), str(code_b))

        result.append({
            "base": base_code,
            "quote": quote_code,
            "rateBuy": entry.get("rateBuy"),
            "rateSell": entry.get("rateSell"),
            "rateCross": entry.get("rateCross"),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "monobank"
        })

    return result or {"message": "Немає даних для вказаних валют"}


@app.get("/currency/privatbank", summary="Курси валют з PrivatBank")
def read_privatbank_currency(
        date: str = Query(default=datetime.today().strftime("%d.%m.%Y"), description="Дата у форматі DD.MM.YYYY")
):
    try:
        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return {"error": "Не вдалося отримати дані з PrivatBank"}

        data = response.json().get("exchangeRate", [])
        result = {}

        for item in data:
            currency = item.get("currency")
            if currency:
                result[currency] = {
                    "buy": item.get("purchaseRate"),
                    "sell": item.get("saleRate"),
                    "source": "privatbank",
                    "date": date
                }

        return result or {"message": "Немає валютних даних на цю дату"}

    except requests.exceptions.RequestException:
        return {"error": "Помилка з'єднання з API PrivatBank"}
