import openrouter
from config import Config

def get_budget_recommendation(paychecks, bills):
    total_income = sum([p.amount for p in paychecks])
    total_bills = sum([b.amount for b in bills])
    savings_goal = total_income * 0.20

    client = openrouter.Client(api_key=Config.OPENROUTER_API_KEY)

    prompt = f"""
    I have an income of ${total_income} and bills totaling ${total_bills}.
    Recommend a budget plan including savings, expenses, and fun money.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        budget_plan = response.choices[0].message.content
        return budget_plan
    except Exception as e:
        return "Unable to generate budget at the moment."
