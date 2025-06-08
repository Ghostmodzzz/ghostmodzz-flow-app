from openrouter import OpenRouter
from flask import current_app

def generate_budget_advice(paycheck, bills, settings):
    client = OpenRouter(api_key=current_app.config["OPENROUTER_API_KEY"])
    prompt = f"""
I have a paycheck of ${paycheck.amount} on {paycheck.date},
and upcoming bills: {', '.join(f'{b.name} (${b.amount}) on {b.date}' for b in bills)}.
Split the remainder: {settings['savings_pct']}% to savings, {settings['spend_pct']}% to spending.
Provide me a friendly summary.
"""
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
    return resp.choices[0].message.content
