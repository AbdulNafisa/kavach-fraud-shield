"""
kavach_data.py — Static data: quick examples, national stats, recent alerts
"""

QUICK_EXAMPLES = [
    {
        "label": "🚨 Digital arrest scam",
        "text": "Someone called saying they are from CBI. They said my Aadhaar card is linked to a hawala money laundering case. They showed me a fake arrest warrant on WhatsApp video call and said I will be arrested in 2 hours unless I pay ₹1.5 lakh to clear my name. They told me not to tell anyone."
    },
    {
        "label": "🏦 KYC fraud SMS",
        "text": "I got an SMS saying my SBI account KYC is expired and will be blocked within 24 hours. The link in the SMS says sbi-kyc-update.in and is asking for my ATM PIN and OTP to update my KYC details."
    },
    {
        "label": "🎰 Lottery prize fraud",
        "text": "I received a call saying I won ₹25 lakhs in KBC Lucky Draw. They said I need to pay ₹15,000 as processing fee and ₹8,000 as TDS before they release the prize money to my account. They said the offer expires tomorrow."
    },
    {
        "label": "💼 Fake job offer",
        "text": "A company called TechHire Global offered me a work from home data entry job with ₹40,000 per month salary. They asked me to pay ₹5,000 as registration fee and ₹3,000 for a training kit before I can start. They said my profile was specially selected."
    },
]

FRAUD_STATS = [
    {"value": "₹1,776 Cr", "label": "Lost to digital arrest scams (Jan–Sep 2024)"},
    {"value": "11.4 Lakh+", "label": "Cybercrime complaints in 2023 (MHA)"},
    {"value": "60%", "label": "Year-on-year increase in cybercrimes"},
    {"value": "1930", "label": "National Cybercrime Helpline"},
]

def get_recent_alerts():
    """Simulated recent national fraud alerts (would be live CERT-In / MHA feed in production)."""
    return [
        {
            "type": "Digital Arrest",
            "location": "Hyderabad",
            "detail": "New wave: fraudsters claiming to be TRAI officials suspending SIM cards."
        },
        {
            "type": "Investment Fraud",
            "location": "Mumbai",
            "detail": "Fake trading app 'ProfitMax' stealing UPI credentials."
        },
        {
            "type": "KYC Fraud",
            "location": "Delhi NCR",
            "detail": "Spoofed HDFC Bank SMSes with phishing links circulating."
        },
    ]
