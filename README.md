# Email Assistant (MVP)
How to run:
1. Create and activate venv:
   - Windows: python -m venv .venv && .venv\Scripts\Activate.ps1
   - macOS/Linux: python3 -m venv .venv && source .venv/bin/activate
2. Install: pip install -r requirements.txt
3. Put CSV file at: data/Sample_Support_Emails_Dataset.csv
4. Run processor: python process_emails.py
5. Run dashboard: streamlit run dashboard.py
Files included:
- process_emails.py : processes CSV and creates data/processed_support_emails.csv
- dashboard.py : Streamlit dashboard to view and edit drafts
- app.py : optional FastAPI backend
