import csv
import os
from datetime import datetime

AUDIT_FILE = 'data/summary_audit.csv'

def log_summary(start_date, end_date, transaction_count, total_spent, summary_text, csv_path):
    fieldnames = ['timestamp', 'start_date', 'end_date', 'transaction_count', 'total_spent', 'summary_text', 'raw_path']

    os.makedirs('data', exist_ok=True)
    file_exists = os.path.isfile(AUDIT_FILE)

    with open(AUDIT_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'start_date': start_date,
            'end_date': end_date,
            'transaction_count': transaction_count,
            'total_spent': total_spent,
            'summary_text': summary_text.strip().replace('\n', ' '),
            'raw_path': csv_path
        })