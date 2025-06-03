import openai
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transactions(csv_path):
    df = pd.read_csv(csv_path)
    df['description'] = df['name'] + " - $" + df['amount'].astype(str)
    sample_text = "\n".join(df['description'].head(20))

    prompt = f"""
You are a personal finance assistant. Based on the following transactions, generate a weekly spending summary. This will be shown as a text so keep it concise.
For context, assume that the total salary of this person is $120K and she lives in new york city.


Show the heading and 2 numbers:
1. Total spending for the week
2. Top category & total spend in that category

Then have one sentence for these:
1. How much I should have spent that week
2. Suggested improvements
3. One compliment

Transactions:
{sample_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content