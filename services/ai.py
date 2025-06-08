import requests
import json
from config import Config

def get_budget_recommendation(paychecks, bills):
    total_income = sum(p.amount for p in paychecks)
    total_bills = sum(b.amount for b in bills)
    prompt = f"My monthly income is {total_income} and my total bills are {total_bills}. What is your recommendation for budgeting?"

    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://ghostmodzz.com/",  # use your domain
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful budgeting assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return "Sorry, I couldn't generate a recommendation at the moment."
