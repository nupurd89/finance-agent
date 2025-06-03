import os
import datetime
import pandas as pd
from dotenv import load_dotenv

from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.webhook_type import WebhookType
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.item_webhook_update_request import ItemWebhookUpdateRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid import Configuration, ApiClient, Environment
from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest


# Load environment variables
load_dotenv()

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")

# Initialize the Plaid API client
configuration = Configuration(
    host=Environment.Sandbox,
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET
    }
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def get_access_token():
    # Step 1: Create sandbox public token
    request = SandboxPublicTokenCreateRequest(
        institution_id="ins_109508",
        initial_products=[Products("transactions")]
    )
    response = client.sandbox_public_token_create(request)
    public_token = response.public_token

    # Step 2: Exchange for access token
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    access_token = exchange_response.access_token

    # Step 3: Set a dummy webhook for this item
    webhook_update_request = ItemWebhookUpdateRequest(
        access_token=access_token,
        webhook="https://webhook.example.com"
    )
    client.item_webhook_update(webhook_update_request)

    # Step 4: Trigger webhook to simulate transaction data
    webhook_request = SandboxItemFireWebhookRequest(
        access_token=access_token,
        webhook_code="DEFAULT_UPDATE",
		webhook_type=WebhookType("TRANSACTIONS") 
    )
    client.sandbox_item_fire_webhook(webhook_request)

    return access_token


def fetch_transactions(access_token, start_date, end_date):
    """
    Fetches transactions using Plaid Transactions API.
    """
    options = TransactionsGetRequestOptions(count=100)
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options=options
    )
    response = client.transactions_get(request)
    transactions = response.transactions

    # Convert to DataFrame
    df = pd.DataFrame([t.to_dict() for t in transactions])
    
    # Save to CSV for later GPT use
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/transactions.csv", index=False)
    return df