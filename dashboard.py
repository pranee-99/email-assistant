# dashboard.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Support Email Dashboard")
df = pd.read_csv("data/processed_support_emails.csv")

st.title("Support Email Dashboard")
st.markdown("**Overview**")
st.metric("Total emails", len(df))
st.write("Priority counts:")
st.write(df['priority'].value_counts())

st.markdown("## Urgent Emails")
urgent = df[df['priority']=='Urgent']
st.table(urgent[['sender','subject','sentiment','phones','alt_emails','draft_reply']].head(20))

st.markdown("## Edit draft reply")
index = st.number_input("Email row index", min_value=0, max_value=len(df)-1, value=0)
st.write(df.loc[index, ['sender','subject','body','sentiment','priority']])
edited = st.text_area("Draft reply", df.loc[index,'draft_reply'], height=200)
if st.button("Save draft to CSV"):
    df.at[index,'draft_reply'] = edited
    df.to_csv("data/processed_support_emails.csv", index=False)
    st.success("Draft saved to data/processed_support_emails.csv")


