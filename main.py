from plaid_utils import get_access_token, fetch_transactions
from gpt_summary import summarize_transactions
from audit_logger import log_summary
import datetime
import time

start = datetime.date.today() - datetime.timedelta(days=30)
end = datetime.date.today()

access_token = get_access_token()
print("Got access token")
print("Waiting for Plaid sandbox to simulate data...")
time.sleep(3)  # 3–5 seconds is usually enough
df = fetch_transactions(access_token, start, end)

print("test")

summary = summarize_transactions('data/transactions.csv')
print(summary)

#saves summary
with open("data/summary.txt", "w") as f:
    f.write(summary)

#creates backing transaction file
total_spent = df['amount'].sum()
transaction_count = len(df)

log_summary(
    start_date=start,
    end_date=end,
    transaction_count=transaction_count,
    total_spent=round(total_spent, 2),
    summary_text=summary,
    csv_path="data/transactions.csv"
)