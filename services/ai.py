import requests
from config import Config

def get_budget_recommendation(paychecks, bills):
    # Prepare prompt
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a budgeting assistant."},
            {"role": "user", "content": f"Paychecks: {[(p.date.isoformat(), p.amount) for p in paychecks]}, Bills: {[(b.name, b.date.isoformat(), b.amount) for b in bills]}"}
        ]
    }
    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}"
    }
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    return "Unable to get recommendation at this time."
