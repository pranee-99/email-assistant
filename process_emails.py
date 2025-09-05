# process_emails.py
import pandas as pd, re
phone_re = re.compile(r'(\+?\d[\d \-]{7,}\d)')
email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

positive_words = {"thank","thanks","great","good","happy","excellent","resolved","appreciate","love"}
negative_words = {"help","error","issue","problem","not working","can't","cannot","fail","frustrat","angry","bad","complain","refund","cancel"}
urgent_words = {"urgent","immediately","asap","can't access","cannot access","critical","down","important","refund","suspend","blocked"}

def extract_contacts(text):
    phones = phone_re.findall(str(text))
    emails = email_re.findall(str(text))
    return phones, list(set(emails))

def classify_sentiment(text):
    text_l = str(text).lower()
    pos = sum(1 for w in positive_words if w in text_l)
    neg = sum(1 for w in negative_words if w in text_l)
    if pos > neg: return "Positive"
    if neg > pos: return "Negative"
    return "Neutral"

def classify_priority(text):
    text_l = str(text).lower()
    for kw in urgent_words:
        if kw in text_l: return "Urgent"
    return "Not urgent"

# Load CSV (update path if needed)
df = pd.read_csv("data/Sample_Support_Emails_Dataset.csv")

# Guess columns
body_col = next((c for c in df.columns if 'body' in c.lower() or 'message' in c.lower()), df.columns[0])
subject_col = next((c for c in df.columns if 'subject' in c.lower() or 'title' in c.lower()), df.columns[0])
from_col = next((c for c in df.columns if 'from' in c.lower() or 'sender' in c.lower() or c.lower()=='email'), df.columns[0])

processed = pd.DataFrame()
processed['sender'] = df[from_col].astype(str)
processed['subject'] = df[subject_col].astype(str)
processed['body'] = df[body_col].astype(str)

processed['phones'], processed['alt_emails'] = zip(*processed['body'].apply(lambda t: extract_contacts(t)))
processed['sentiment'] = processed['body'].apply(classify_sentiment)
processed['priority'] = processed['body'].apply(classify_priority)

def make_name(email):
    m = email_re.findall(email)
    if m:
        return m[0].split('@')[0].replace('.', ' ').title()
    return "Customer"

processed['sender_name'] = processed['sender'].apply(make_name)

def draft_reply(row):
    name = row['sender_name']
    if row['priority']=='Urgent' or row['sentiment']=='Negative':
        opening = f"Hi {name},\n\nI'm sorry you're facing this issue — thanks for letting us know."
    else:
        opening = f"Hi {name},\n\nThanks for reaching out!"
    action = "\n\nCould you please provide order id or screenshot? We'll investigate immediately."
    closing = "\n\nBest regards,\nSupport Team"
    return opening + action + closing

processed['draft_reply'] = processed.apply(draft_reply, axis=1)
processed.to_csv("data/processed_support_emails.csv", index=False)
print("Saved data/processed_support_emails.csv")
