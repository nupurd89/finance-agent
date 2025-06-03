import streamlit as st
import pandas as pd

# === Load summary and transactions ===
st.set_page_config(page_title="Finance GPT", layout="centered")
st.title("💰 Personal Finance AI Assistant")

st.header("📄 Weekly AI Summary")
try:
    with open("data/summary.txt", "r") as f:
        summary = f.read()
    st.success(summary)
except FileNotFoundError:
    st.warning("Summary not found. Run main.py to generate a new one.")

st.header("📊 Transactions")
try:
    df = pd.read_csv("data/transactions.csv")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.warning("Transactions file not found. Run main.py to generate it.")

# === Ask GPT follow-up questions ===
st.header("💬 Ask a follow-up question")
question = st.text_input("What do you want to know about your finances?")

if question:
    try:
        from chatbot import ask_agent
        response = ask_agent(question)
        st.markdown(f"**🤖 GPT Response:** {response}")
    except Exception as e:
        st.error(f"Error calling GPT: {e}")
