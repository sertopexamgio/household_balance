# 🏠 household_balance

A simple and customizable Streamlit app to **track and analyze income and expenses** for your household.  
Visualize your monthly balance, top spending categories, income vs expenses, savings, and more.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/sertopexamgio/household_balance.git
cd household_balance
```

### 2. Set up the Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up the Python environment
```bash
streamlit run app.py
```


📂 Project Structure
```
household_balance/
├── app.py                  # Main entry point for Streamlit UI
├── requirements.txt        # Python dependencies
├── data/                   # Optional: store your CSV/DB file here
├── utils/
│   ├── db.py      # Load & preprocess financial data
│   └── visuals.py          # All plots and visualization helpers
└── README.md               # You're here!
```

✨ Features
```
	•	Upload or load household financial data
	•	Monthly summary of income, expenses, and net balance
	•	Category-level breakdowns with interactive charts
	•	Auto-detection of transfers between accounts
	•	Highlight savings and visualize financial trends
```

📝 Requirements
```
	•	Python 3.8+
	•	Streamlit
	•	pandas
	•	altair
```

📌 Future Ideas
```
    •	Upload transactions via PDFs
    •	Auto categorization
	•	Tag recurring expenses
	•	Forecasting future balances
    •	Alert for transaction anomalies
```

📬 Feedback
If you have suggestions or feature requests, feel free to open an issue or pull request.


## License

This project is licensed under the [MIT License](LICENSE).
