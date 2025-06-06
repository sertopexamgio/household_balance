import os
from openai import OpenAI
from typing import List, Dict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant that extracts financial transactions from raw bank statements.
Each transaction should be a dictionary with:
- bank_name (string)
- month (YYYY-MM)
- receiver (string)
- category (string, guess if not present)
- amount (float, negative for expenses, positive for income)

Output a Python list of dictionaries. Only valid structured data, no explanation.
"""

def extract_transactions_from_text(text: str) -> List[Dict]:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text[:4000]},
            ],
            temperature=0.2
        )
        raw_output = response.choices[0].message.content.strip()

        transactions = eval(raw_output, {"__builtins__": {}})
        if isinstance(transactions, list):
            for tx in transactions:
                assert all(k in tx for k in ["bank_name", "month", "receiver", "category", "amount"])
            return transactions
        return []

    except Exception as e:
        print(f"LLM extraction failed: {e}")
        return []