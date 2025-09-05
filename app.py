import streamlit as st
import pandas as pd
import random

#  SAMPLE DATA (replace with your email dataset later) 
emails = [
    {
        "sender": "john@example.com",
        "subject": "Cannot access my account",
        "body": "I tried logging in but it keeps saying invalid password.",
        "priority": "Urgent",
        "sentiment": "Negative",
        "date": "2025-09-01"
    },
    {
        "sender": "lisa@example.com",
        "subject": "Feature request",
        "body": "Can you add dark mode to your product? Would be awesome!",
        "priority": "Not Urgent",
        "sentiment": "Positive",
        "date": "2025-09-02"
    },
    {
        "sender": "mike@example.com",
        "subject": "Need help with setup",
        "body": "I don’t understand how to install the software. Please guide me.",
        "priority": "Urgent",
        "sentiment": "Neutral",
        "date": "2025-09-03"
    }
]

df = pd.DataFrame(emails)

#STREAMLIT PAGE SETTINGS 
st.set_page_config(page_title="AI Support Assistant", layout="wide")
st.title("📧 AI-Powered Communication Assistant")

# --- SUMMARY METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("📩 Total Emails", len(df))
col2.metric("⚡ Urgent", df[df["priority"]=="Urgent"].shape[0])
col3.metric("✅ Resolved", random.randint(1, len(df)))  # mock value

st.markdown("---")

# --- EMAIL DISPLAY ---
for i, row in df.iterrows():
    with st.container():
        st.markdown(
            f"""
            <div style="padding:15px; margin-bottom:15px; border-radius:12px;
                        background-color:#1E1E1E; color:white; box-shadow:0 4px 8px rgba(0,0,0,0.3);">
                <h4>{row['subject']}</h4>
                <p><b>From:</b> {row['sender']} | <b>Date:</b> {row['date']}</p>
                <p>{row['body']}</p>
                <p>
                    <span style="background-color:{'red' if row['priority']=='Urgent' else 'green'};
                                padding:4px 8px; border-radius:8px; color:white;">
                        {row['priority']}
                    </span>
                    &nbsp;
                    <span>
                        {"😊" if row['sentiment']=='Positive' else "😐" if row['sentiment']=='Neutral' else "😡"}
                        {row['sentiment']}
                    </span>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# --- CHARTS ---
st.subheader("📊 Analytics Overview")
colA, colB = st.columns(2)

with colA:
    st.bar_chart(df["priority"].value_counts())

with colB:
    st.bar_chart(df["sentiment"].value_counts())

