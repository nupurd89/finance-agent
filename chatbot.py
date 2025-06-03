# chatbot.py

import os
import openai
import json
import pandas as pd

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Load user context
with open("user_context.json") as f:
    context = json.load(f)

# Load recent transactions
try:
    df = pd.read_csv("data/transactions.csv")
    recent_txn_preview = df[['date', 'name', 'amount']].sort_values(by="date", ascending=False).head(5).to_csv(index=False)
except FileNotFoundError:
    recent_txn_preview = "No transaction data found."

#Load previous summary
try:
    with open("data/summary.txt") as f:
        latest_summary = f.read()
except FileNotFoundError:
    latest_summary = "No summary found. You may need to run the sync script first."

# Set up OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_agent(user_input):
    system_prompt = f"""
You are a personal finance assistant helping the user stay on top of their money.

User profile:
- Monthly income: ${context['monthly_income']}
- Fixed expenses: ${context['fixed_expenses']}

Recent spending summary (GPT-generated):
{latest_summary}

Most recent transactions:
{recent_txn_preview }

Be concise, friendly, and practical. Answer based on the user's financial profile and spending behavior.
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("💸 Welcome to your finance assistant. Ask me anything about your spending, savings, or goals!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("💬 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        answer = ask_agent(user_input)
        print(f"🤖 GPT: {answer}\n")