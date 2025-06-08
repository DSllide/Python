from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path="monobank.env")

app = FastAPI()


MONOBANK_API = os.getenv("MONOBANK_API")
INVEST_RATE = float(os.getenv("INVEST_RATE", 0.05))


def get_usd_exchange_rate():
    try:
        response = requests.get(MONOBANK_API)
        data = response.json()


        if not isinstance(data, list):
            raise HTTPException(
                status_code=500,
                detail=f"Expected list, got {type(data).__name__}. Response: {data}"
            )


        for item in data:
            if item["currencyCodeA"] == 840 and item["currencyCodeB"] == 980:
                return item.get("rateBuy") or item.get("rateCross")

        raise HTTPException(status_code=404, detail="USD to UAH rate not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exchange rate error: {str(e)}")

def calculate_investment(monthly_amount: float, months: int = 12):
    total = 0
    for _ in range(months):
        total = (total + monthly_amount) * (1 + INVEST_RATE / 12)
    return round(total, 2)


@app.get("/calculate")
def calculate(rent: float, food: float, other: float, salary: float):
    expenses = rent + food + other
    remaining = salary - expenses

    if remaining < 0:
        return {"message": "Витрати перевищують зарплату", "дефіцит": abs(remaining)}

    usd_rate = get_usd_exchange_rate()
    remaining_usd = round(remaining / usd_rate, 2)
    investment_total = calculate_investment(remaining)

    return {
        "total_expenses": expenses,
        "remaining_uah": remaining,
        "usd_rate": usd_rate,
        "remaining_usd": remaining_usd,
        "investment_after_year": investment_total
    }
