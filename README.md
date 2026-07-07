# 🛡️ Kavach — AI-Powered Citizen Fraud Shield

> **ET AI Hackathon 2.0 · Problem Statement 6: AI for Digital Public Safety**

Kavach is a real-time multilingual AI fraud detection platform that protects Indian citizens from digital arrest scams, KYC fraud, lottery fraud, and job offer scams — **before money changes hands**.

## Features
- Real-time fraud detection powered by Claude Sonnet (Anthropic API)
- 4-language support: English, Hindi, Telugu, Tamil
- Offline rule-based fallback (no API key needed for demo)
- Auto-generated NCRP complaint draft in 30 seconds
- 1930 cybercrime helpline integration for high-risk alerts

## Quick Start
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
streamlit run app.py
```

## Project Structure
```
kavach/
├── app.py           # Main Streamlit app
├── kavach_utils.py  # Language data, prompts, offline engine, NCRP draft
├── requirements.txt
└── README.md
```

## Submission
ET AI Hackathon 2.0 · Phase 2 · Problem Statement 6

