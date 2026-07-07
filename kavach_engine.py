"""
kavach_engine.py — Core fraud analysis engine
Supports: Anthropic API (online) + rule-based fallback (offline)
"""

import os
import json
import re

# ── Language strings ───────────────────────────────────────────────────────────
LANGUAGES = {
    "English": {
        "input_title": "🔍 Describe the suspicious situation",
        "input_label": "Describe the call, message or payment request",
        "placeholder": "e.g. Someone called saying they are from CBI and my Aadhaar is linked to money laundering...",
        "analyze_btn": "Analyze for fraud risk",
        "high": "HIGH RISK — Likely fraud",
        "medium": "MEDIUM RISK — Stay cautious",
        "low": "LOW RISK — Appears safe",
        "verdict": "Verdict",
        "red_flags": "Red flags detected",
        "steps": "What to do right now",
    },
    "Hindi / हिन्दी": {
        "input_title": "🔍 संदिग्ध स्थिति का विवरण दें",
        "input_label": "कॉल, संदेश या भुगतान अनुरोध का विवरण दें",
        "placeholder": "उदा. किसी ने CBI से होने का दावा करते हुए कहा कि मेरा आधार हवाला से जुड़ा है...",
        "analyze_btn": "धोखाधड़ी जोखिम के लिए विश्लेषण करें",
        "high": "उच्च जोखिम — संभावित धोखाधड़ी",
        "medium": "मध्यम जोखिम — सतर्क रहें",
        "low": "कम जोखिम — सुरक्षित लगता है",
        "verdict": "निर्णय",
        "red_flags": "खतरे के संकेत",
        "steps": "अभी क्या करें",
    },
    "Telugu / తెలుగు": {
        "input_title": "🔍 అనుమానాస్పద పరిస్థితిని వివరించండి",
        "input_label": "కాల్, సందేశం లేదా చెల్లింపు అభ్యర్థనను వివరించండి",
        "placeholder": "ఉదా. CBI నుండి అని చెప్పి ఒకరు ఫోన్ చేసి నా ఆధార్ హవాలాతో అనుసంధానించబడిందని చెప్పారు...",
        "analyze_btn": "మోసం ప్రమాదం కోసం విశ్లేషించండి",
        "high": "అధిక ప్రమాదం — మోసం అనుమానం",
        "medium": "మధ్యస్థ ప్రమాదం — జాగ్రత్తగా ఉండండి",
        "low": "తక్కువ ప్రమాదం — సురక్షితంగా కనిపిస్తోంది",
        "verdict": "తీర్పు",
        "red_flags": "ప్రమాద సంకేతాలు",
        "steps": "ఇప్పుడు ఏమి చేయాలి",
    },
    "Tamil / தமிழ்": {
        "input_title": "🔍 சந்தேகமான நிலையை விவரிக்கவும்",
        "input_label": "அழைப்பு, செய்தி அல்லது கட்டண கோரிக்கையை விவரிக்கவும்",
        "placeholder": "எ.கா. CBI என்று கூறி யாரோ அழைத்து என் ஆதார் ஹவாலாவுடன் இணைக்கப்பட்டுள்ளது என்று சொன்னார்கள்...",
        "analyze_btn": "மோசடி ஆபத்துக்கு பகுப்பாய்வு செய்யவும்",
        "high": "அதிக ஆபத்து — மோசடி சாத்தியம்",
        "medium": "நடுத்தர ஆபத்து — எச்சரிக்கையாக இருங்கள்",
        "low": "குறைந்த ஆபத்து — பாதுகாப்பானது",
        "verdict": "தீர்ப்பு",
        "red_flags": "அபாய சிக்னல்கள்",
        "steps": "இப்போது என்ன செய்வது",
    },
}

# ── Rule-based offline engine ──────────────────────────────────────────────────
SCAM_PATTERNS = {
    "Digital Arrest Scam": {
        "keywords": ["cbi", "ed", "enforcement directorate", "customs", "trai", "police", "arrest",
                     "warrant", "case registered", "money laundering", "hawala", "aadhaar linked",
                     "digital arrest", "video call", "do not tell", "don't tell anyone", "clear your name",
                     "गिरफ्तारी", "सीबीआई", "అరెస్ట్", "கைது"],
        "risk": "HIGH",
        "score_range": (82, 97),
        "flags_en": [
            "Impersonation of government agency (CBI/ED/TRAI/Customs)",
            "Threat of arrest or legal action to create panic",
            "Demand for secrecy ('do not tell anyone')",
            "Request for payment to 'clear your name'",
            "Video call used to display fake ID/warrant"
        ],
        "steps_en": [
            "HANG UP immediately — no real government agency arrests via video call",
            "Do NOT transfer any money under any circumstances",
            "Call 1930 cybercrime helpline to report",
            "File complaint at cybercrime.gov.in",
            "Inform family members so they are not targeted next"
        ],
        "report_to": "1930 Helpline · I4C · cybercrime.gov.in · Local police cybercrime cell"
    },
    "KYC / Bank Fraud": {
        "keywords": ["kyc", "account blocked", "account suspended", "update kyc", "otp", "atm pin",
                     "net banking", "link", "click here", "verify now", "sbi", "hdfc", "icici",
                     "केवाईसी", "KYC నవీకరణ", "KYC புதுப்பிக்கவும்"],
        "risk": "HIGH",
        "score_range": (78, 93),
        "flags_en": [
            "Unsolicited message claiming your account is at risk",
            "Link to external website (not official bank domain)",
            "Request for OTP, PIN, or net banking credentials",
            "Urgency: 'account will be blocked in 24 hours'",
            "Spoofed sender ID mimicking legitimate bank"
        ],
        "steps_en": [
            "Do NOT click any links in the message",
            "Never share OTP or PIN with anyone, including 'bank staff'",
            "Call your bank's official number (on back of card) to verify",
            "Report phishing SMS to 1909 (TRAI DND registry)",
            "File complaint at cybercrime.gov.in if you shared credentials"
        ],
        "report_to": "Your bank's fraud helpline · 1909 (SMS fraud) · cybercrime.gov.in"
    },
    "Lottery / Prize Fraud": {
        "keywords": ["won", "winner", "lottery", "prize", "lucky draw", "kbc", "claim", "processing fee",
                     "tds", "tax", "release prize", "congratulations", "selected", "lakh", "crore",
                     "जीता", "इनाम", "బహుమతి", "பரிசு"],
        "risk": "HIGH",
        "score_range": (80, 95),
        "flags_en": [
            "Unsolicited prize notification for a lottery you never entered",
            "Request for 'processing fee' or 'TDS' before releasing prize",
            "Prize amount is unusually large (lakhs/crores)",
            "Pressure to act quickly before 'offer expires'",
            "Communication via personal WhatsApp/SMS, not official channel"
        ],
        "steps_en": [
            "Delete the message — you cannot win a lottery you didn't enter",
            "Never pay any 'fee' to collect a prize — this is the scam",
            "Block the number immediately",
            "Warn family members who may receive the same message",
            "Report at cybercrime.gov.in"
        ],
        "report_to": "cybercrime.gov.in · Local police station"
    },
    "Job Offer Fraud": {
        "keywords": ["job", "hiring", "work from home", "data entry", "registration fee", "training kit",
                     "salary", "placement", "apply now", "joining fee", "security deposit",
                     "नौकरी", "ఉద్యోగం", "வேலை"],
        "risk": "MEDIUM",
        "score_range": (60, 82),
        "flags_en": [
            "Job offer requiring upfront payment (registration/training/security deposit)",
            "Unrealistically high salary for simple work (data entry, form filling)",
            "Company not verifiable on MCA21 or LinkedIn",
            "Communication only via WhatsApp, no official email domain",
            "Offer made without proper interview process"
        ],
        "steps_en": [
            "Never pay any fee to get a job — legitimate employers do not charge candidates",
            "Verify company on mca.gov.in (Ministry of Corporate Affairs)",
            "Search company name + 'fraud' or 'scam' online",
            "Report to cybercrime.gov.in if money was already paid",
            "Contact your state's labour department if needed"
        ],
        "report_to": "cybercrime.gov.in · State Labour Department · Local police"
    },
    "Investment / Trading Fraud": {
        "keywords": ["investment", "returns", "profit", "trading", "crypto", "stock", "guaranteed",
                     "double", "triple", "scheme", "mlm", "referral", "earn from home",
                     "निवेश", "పెట్టుబడి", "முதலீடு"],
        "risk": "HIGH",
        "score_range": (75, 92),
        "flags_en": [
            "Promise of guaranteed high returns (10-30% monthly) — illegal in India",
            "Pressure to invest quickly before 'opportunity closes'",
            "Request to recruit others for additional commission (Ponzi/MLM markers)",
            "Platform not registered with SEBI",
            "Withdrawals blocked or delayed once invested"
        ],
        "steps_en": [
            "Verify investment platforms on SEBI SCORES portal (scores.gov.in)",
            "Never invest in schemes promising guaranteed returns",
            "Do not recruit others — you may become liable",
            "Report to SEBI at sebi.gov.in and cybercrime.gov.in",
            "Contact RBI for banking fraud: sachet.rbi.org.in"
        ],
        "report_to": "SEBI SCORES · RBI SACHET · cybercrime.gov.in · 1930 helpline"
    },
}

def rule_based_analyze(text: str, lang: str) -> dict:
    """Offline rule-based fraud detection engine."""
    text_lower = text.lower()
    
    best_match = None
    best_score = 0
    keyword_hits = 0

    for fraud_type, pattern in SCAM_PATTERNS.items():
        hits = sum(1 for kw in pattern["keywords"] if kw.lower() in text_lower)
        if hits > best_score:
            best_score = hits
            keyword_hits = hits
            best_match = fraud_type

    if best_match and keyword_hits >= 1:
        pattern = SCAM_PATTERNS[best_match]
        import random
        score = random.randint(*pattern["score_range"])
        
        lang_code = lang.split("/")[0].strip()
        
        summaries = {
            "HIGH": f"This matches a known {best_match} pattern. Do NOT comply with any demands or transfer money.",
            "MEDIUM": f"This has characteristics of a {best_match}. Exercise caution before proceeding.",
        }
        
        return {
            "risk_level": pattern["risk"],
            "risk_score": score,
            "fraud_type": best_match,
            "summary": summaries.get(pattern["risk"], f"Possible {best_match} detected. Verify carefully."),
            "red_flags": pattern["flags_en"][:4],
            "immediate_steps": pattern["steps_en"][:4],
            "report_to": pattern["report_to"],
            "engine": "offline"
        }
    else:
        # Low risk / unknown
        return {
            "risk_level": "LOW",
            "risk_score": 15,
            "fraud_type": "No clear pattern detected",
            "summary": "No known fraud patterns were detected. Stay cautious and verify through official channels if in doubt.",
            "red_flags": [],
            "immediate_steps": [
                "If in doubt, hang up and call the organisation's official number",
                "Never share OTP, PIN, or passwords",
                "Verify any government communication at official portals",
            ],
            "report_to": "cybercrime.gov.in · 1930 (if concerned)",
            "engine": "offline"
        }


def analyze_fraud(text: str, lang: str, mode: str) -> dict:
    """
    Main fraud analysis function.
    Tries Anthropic API first; falls back to offline rule-based engine.
    """
    lang_name = lang.split("/")[0].strip()
    
    system_prompt = f"""You are Kavach, an AI fraud detection assistant for Indian citizens.
Analyze the described situation for fraud risk.

Respond ONLY with a valid JSON object (no markdown, no preamble):
{{
  "risk_level": "HIGH" | "MEDIUM" | "LOW",
  "risk_score": 0-100,
  "fraud_type": "short fraud category name in {lang_name}",
  "summary": "2-sentence plain language verdict in {lang_name}",
  "red_flags": ["flag1 in {lang_name}", "flag2", "flag3", "flag4"],
  "immediate_steps": ["step1 in {lang_name}", "step2", "step3", "step4"],
  "report_to": "relevant Indian authority to report this to"
}}

Key fraud categories in India: Digital Arrest Scam, KYC Fraud, Lottery Fraud, Job Offer Fraud, Investment Fraud, Counterfeit Currency, Phishing, SIM Swap Fraud.

Be conservative: when in doubt, rate higher risk to protect citizens."""

    # Try API
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": f"Mode: {mode}\n\nDescription: {text}"}]
        )
        
        raw = message.content[0].text
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        result["engine"] = "api"
        return result

    except Exception:
        # Fallback to offline engine
        return rule_based_analyze(text, lang)
