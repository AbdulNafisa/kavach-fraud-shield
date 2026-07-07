"""
Kavach utilities — language data, prompts, offline engine, NCRP draft
"""

from datetime import datetime

LANGUAGES = ["en", "hi", "te", "ta"]

# ── UI TEXT ───────────────────────────────────────────────────────────────────
UI_TEXT = {
    "en": {
        "tab_check": "Fraud Check", "tab_history": "History", "tab_dashboard": "Dashboard",
        "input_heading": "Describe the suspicious interaction",
        "input_mode_label": "What are you checking?",
        "mode_call": "Call / Message", "mode_payment": "Payment Request",
        "mode_link": "Link / Website", "mode_screenshot": "Screenshot",
        "examples_label": "Quick examples:", "analyze_btn": "Analyze for fraud",
        "input_placeholder": "Describe the call, message, or payment request you received...",
        "result_heading": "Fraud Analysis Result",
        "analyzing": "Analyzing with Kavach AI...",
        "empty_warning": "Please describe the suspicious interaction first.",
        "result_placeholder": "Your fraud analysis will appear here after you click Analyze.",
        "risk_high": "High Risk — Likely Fraud", "risk_medium": "Medium Risk — Stay Cautious",
        "risk_low": "Low Risk — Appears Safe",
        "fraud_type_label": "Fraud type", "flags_label": "Red flags detected",
        "steps_label": "What to do right now", "report_label": "Report to",
        "emergency_heading": "Report this fraud immediately",
        "emergency_text": "Call the National Cybercrime Helpline now:",
        "ncrp_heading": "Auto-generated NCRP Complaint Draft",
        "download_complaint": "Download complaint draft",
        "no_history": "No scans yet. Run a fraud check to see history here.",
    },
    "hi": {
        "tab_check": "धोखाधड़ी जांच", "tab_history": "इतिहास", "tab_dashboard": "डैशबोर्ड",
        "input_heading": "संदिग्ध बातचीत का विवरण दें",
        "input_mode_label": "आप क्या जांच रहे हैं?",
        "mode_call": "कॉल / संदेश", "mode_payment": "भुगतान अनुरोध",
        "mode_link": "लिंक / वेबसाइट", "mode_screenshot": "स्क्रीनशॉट",
        "examples_label": "उदाहरण:", "analyze_btn": "धोखाधड़ी की जांच करें",
        "input_placeholder": "जो कॉल, संदेश या भुगतान अनुरोध आया उसका विवरण दें...",
        "result_heading": "धोखाधड़ी विश्लेषण परिणाम",
        "analyzing": "Kavach AI से विश्लेषण हो रहा है...",
        "empty_warning": "कृपया पहले संदिग्ध बातचीत का विवरण दें।",
        "result_placeholder": "विश्लेषण यहाँ दिखेगा।",
        "risk_high": "उच्च जोखिम — संभावित धोखाधड़ी",
        "risk_medium": "मध्यम जोखिम — सतर्क रहें",
        "risk_low": "कम जोखिम — सुरक्षित लगता है",
        "fraud_type_label": "धोखाधड़ी का प्रकार", "flags_label": "खतरे के संकेत",
        "steps_label": "अभी क्या करें", "report_label": "रिपोर्ट करें",
        "emergency_heading": "तुरंत इस धोखाधड़ी की रिपोर्ट करें",
        "emergency_text": "राष्ट्रीय साइबर अपराध हेल्पलाइन पर कॉल करें:",
        "ncrp_heading": "NCRP शिकायत ड्राफ्ट",
        "download_complaint": "शिकायत डाउनलोड करें",
        "no_history": "अभी तक कोई जांच नहीं। धोखाधड़ी जांच चलाएं।",
    },
    "te": {
        "tab_check": "మోసం తనిఖీ", "tab_history": "చరిత్ర", "tab_dashboard": "డ్యాష్‌బోర్డ్",
        "input_heading": "అనుమానాస్పద సంభాషణను వివరించండి",
        "input_mode_label": "మీరు ఏమి తనిఖీ చేస్తున్నారు?",
        "mode_call": "కాల్ / సందేశం", "mode_payment": "చెల్లింపు అభ్యర్థన",
        "mode_link": "లింక్ / వెబ్‌సైట్", "mode_screenshot": "స్క్రీన్‌షాట్",
        "examples_label": "ఉదాహరణలు:", "analyze_btn": "మోసం కోసం విశ్లేషించండి",
        "input_placeholder": "మీకు వచ్చిన కాల్, సందేశం లేదా చెల్లింపు అభ్యర్థనను వివరించండి...",
        "result_heading": "మోసం విశ్లేషణ ఫలితం",
        "analyzing": "Kavach AI తో విశ్లేషిస్తోంది...",
        "empty_warning": "దయచేసి ముందుగా అనుమానాస్పద సంభాషణను వివరించండి.",
        "result_placeholder": "విశ్లేషణ ఇక్కడ కనిపిస్తుంది.",
        "risk_high": "అధిక ప్రమాదం — మోసం", "risk_medium": "మధ్యస్థ ప్రమాదం — జాగ్రత్తగా ఉండండి",
        "risk_low": "తక్కువ ప్రమాదం — సురక్షితం",
        "fraud_type_label": "మోసం రకం", "flags_label": "ప్రమాద సంకేతాలు",
        "steps_label": "ఇప్పుడు ఏమి చేయాలి", "report_label": "నివేదించండి",
        "emergency_heading": "ఈ మోసాన్ని వెంటనే నివేదించండి",
        "emergency_text": "జాతీయ సైబర్ క్రైమ్ హెల్ప్‌లైన్‌కు కాల్ చేయండి:",
        "ncrp_heading": "NCRP ఫిర్యాదు డ్రాఫ్ట్",
        "download_complaint": "ఫిర్యాదు డౌన్‌లోడ్ చేయండి",
        "no_history": "ఇంకా స్కాన్ లేదు. మోసం తనిఖీ నడపండి.",
    },
    "ta": {
        "tab_check": "மோசடி சோதனை", "tab_history": "வரலாறு", "tab_dashboard": "டாஷ்போர்டு",
        "input_heading": "சந்தேகமான தொடர்பை விவரிக்கவும்",
        "input_mode_label": "நீங்கள் எதை சோதிக்கிறீர்கள்?",
        "mode_call": "அழைப்பு / செய்தி", "mode_payment": "கட்டண கோரிக்கை",
        "mode_link": "இணைப்பு / வலைத்தளம்", "mode_screenshot": "திரைப்படம்",
        "examples_label": "எடுத்துக்காட்டுகள்:", "analyze_btn": "மோசடிக்காக பகுப்பாய்வு செய்யுங்கள்",
        "input_placeholder": "நீங்கள் பெற்ற அழைப்பு, செய்தி அல்லது கட்டண கோரிக்கையை விவரிக்கவும்...",
        "result_heading": "மோசடி பகுப்பாய்வு முடிவு",
        "analyzing": "Kavach AI பகுப்பாய்வு செய்கிறது...",
        "empty_warning": "முதலில் சந்தேகமான தொடர்பை விவரிக்கவும்.",
        "result_placeholder": "பகுப்பாய்வு இங்கே தோன்றும்.",
        "risk_high": "அதிக ஆபத்து — மோசடி", "risk_medium": "நடுத்தர ஆபத்து — கவனமாக இருங்கள்",
        "risk_low": "குறைந்த ஆபத்து — பாதுகாப்பானது",
        "fraud_type_label": "மோசடி வகை", "flags_label": "அபாய சிக்னல்கள்",
        "steps_label": "இப்போது என்ன செய்வது", "report_label": "புகாரளிக்கவும்",
        "emergency_heading": "இந்த மோசடியை உடனடியாக புகாரளிக்கவும்",
        "emergency_text": "தேசிய சைபர் குற்ற உதவி எண்ணை அழைக்கவும்:",
        "ncrp_heading": "NCRP புகார் வரைவு",
        "download_complaint": "புகாரை பதிவிறக்கவும்",
        "no_history": "இன்னும் ஸ்கேன் இல்லை. மோசடி சோதனை இயக்கவும்.",
    },
}

# ── FRAUD EXAMPLES ─────────────────────────────────────────────────────────────
FRAUD_EXAMPLES = {
    "en": {
        "Digital arrest": "Someone called saying they are from CBI. They said my Aadhaar is linked to a money laundering case. They showed me a fake arrest warrant on WhatsApp video call and said I will be arrested in 2 hours unless I pay ₹1.5 lakh. They told me not to tell anyone.",
        "KYC fraud": "I got an SMS saying my SBI account KYC is expired and will be blocked in 24 hours. The link in the SMS is sbi-kyc-update.in and it is asking for my ATM PIN and OTP.",
        "Lottery fraud": "I received a call saying I won ₹25 lakhs in KBC Lucky Draw. They said I need to pay ₹15,000 as processing fee before they can release the prize money to my account.",
        "Job fraud": "A company called TechHire Global offered me a data entry job from home with ₹40,000 per month. They asked me to pay ₹5,000 registration fee and ₹3,000 for a training kit before I can start.",
    },
    "hi": {
        "डिजिटल अरेस्ट": "किसी ने CBI से होने का दावा करते हुए फोन किया। कहा कि मेरा आधार मनी लॉन्ड्रिंग केस से जुड़ा है। WhatsApp वीडियो कॉल पर नकली गिरफ्तारी वारंट दिखाया और बोला कि ₹1.5 लाख न दिए तो 2 घंटे में गिरफ्तार हो जाऊंगा।",
        "KYC धोखाधड़ी": "SMS आया कि मेरे SBI खाते की KYC समाप्त हो गई है और 24 घंटे में बंद हो जाएगा। लिंक sbi-kyc-update.in है और ATM PIN और OTP मांग रहा है।",
        "लॉटरी धोखाधड़ी": "फोन आया कि KBC Lucky Draw में मुझे ₹25 लाख मिले हैं। पहले ₹15,000 प्रोसेसिंग फीस देनी होगी।",
        "नौकरी धोखाधड़ी": "TechHire Global ने ₹40,000/माह पर घर से काम का ऑफर दिया। काम शुरू करने से पहले ₹5,000 रजिस्ट्रेशन और ₹3,000 ट्रेनिंग किट के लिए मांगे।",
    },
    "te": {
        "డిజిటల్ అరెస్ట్": "CBI నుండి అని చెప్పి ఎవరో ఫోన్ చేశారు. నా ఆధార్ మనీ లాండరింగ్ కేసుకు లింక్ అయిందని చెప్పారు. WhatsApp వీడియో కాల్‌లో నకిలీ అరెస్ట్ వారంట్ చూపించారు. ₹1.5 లక్షలు చెల్లించకపోతే 2 గంటల్లో అరెస్ట్ చేస్తామని బెదిరించారు.",
        "KYC మోసం": "నా SBI అకౌంట్ KYC గడువు తీరిపోయిందని SMS వచ్చింది. sbi-kyc-update.in లింక్ ఇచ్చి ATM PIN మరియు OTP అడుగుతోంది.",
        "లాటరీ మోసం": "KBC Lucky Draw లో ₹25 లక్షలు గెల్చావని ఫోన్ వచ్చింది. ముందు ₹15,000 ప్రాసెసింగ్ ఫీ చెల్లించాలని చెప్పారు.",
        "ఉద్యోగ మోసం": "TechHire Global ₹40,000/నెల ఇంటి నుండి పని ఆఫర్ చేసింది. పని మొదలుపెట్టే ముందు ₹5,000 రిజిస్ట్రేషన్ ఫీ అడిగారు.",
    },
    "ta": {
        "டிஜிட்டல் கைது": "CBI என்று கூறி யாரோ அழைத்தார்கள். என் ஆதார் பணமோசடி வழக்கில் இணைக்கப்பட்டதாக கூறினார்கள். WhatsApp வீடியோ அழைப்பில் போலி கைது உத்தரவு காட்டி ₹1.5 லட்சம் கட்டாவிட்டால் 2 மணி நேரத்தில் கைது செய்வோம் என்றார்கள்.",
        "KYC மோசடி": "என் SBI கணக்கின் KYC காலாவதியாகிவிட்டது என SMS வந்தது. sbi-kyc-update.in இணைப்பில் ATM PIN மற்றும் OTP கேட்கிறது.",
        "லாட்டரி மோசடி": "KBC Lucky Draw-ல் ₹25 லட்சம் வென்றதாக அழைப்பு வந்தது. பரிசை வெளியிட ₹15,000 செலுத்த வேண்டும் என்றார்கள்.",
        "வேலை மோசடி": "TechHire Global ₹40,000/மாதம் வீட்டிலிருந்து வேலை வழங்கியது. தொடங்குவதற்கு ₹5,000 பதிவுக் கட்டணம் கேட்டார்கள்.",
    },
}

# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
def build_system_prompt(lang: str) -> str:
    lang_names = {"en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil"}
    lang_name = lang_names.get(lang, "English")
    return f"""You are Kavach, an AI fraud detection assistant built to protect Indian citizens from digital fraud, scams, and cybercrime.

Analyze the described situation for fraud risk and respond ONLY with a valid JSON object — no markdown fences, no preamble, no explanation outside the JSON.

JSON schema:
{{
  "risk_level": "HIGH" | "MEDIUM" | "LOW",
  "risk_score": <integer 0-100>,
  "fraud_type": "<short category name in {lang_name}>",
  "summary": "<2-sentence plain language verdict in {lang_name}>",
  "red_flags": ["<flag in {lang_name}>", ...],
  "immediate_steps": ["<step in {lang_name}>", ...],
  "report_to": "<relevant Indian authority in {lang_name}>"
}}

Detection priorities (India-specific):
- Digital arrest scams: impersonation of CBI/ED/Customs/TRAI/Supreme Court, fake arrest warrants, secrecy demands, UPI payment to "clear your name"
- KYC fraud: spoofed bank SMS, fake domain links, credential harvesting, OTP requests
- Lottery/prize fraud: advance fee demanded before prize release, KBC/government impersonation
- Job offer fraud: registration/training fee demanded before employment
- Counterfeit currency: suspicious note features described
- Investment fraud: guaranteed returns, crypto schemes, Ponzi indicators
- Impersonation: fake government portals, utility company threats

Risk scoring guide:
- HIGH (70-100): Clear fraud indicators — impersonation + financial demand + urgency + secrecy
- MEDIUM (35-69): Some suspicious elements but incomplete picture
- LOW (0-34): Legitimate-seeming interaction with minor concerns

Always include 3-5 red flags and 3-4 actionable immediate steps. Steps must be specific and doable by a non-technical citizen."""


# ── OFFLINE RULE-BASED ENGINE ──────────────────────────────────────────────────
def offline_rule_check(text: str, lang: str = "en") -> dict:
    """Fallback rule-based fraud detection when API is unavailable."""
    text_lower = text.lower()

    HIGH_KEYWORDS = [
        "cbi","ed","customs","trai","arrest","warrant","money laundering","hawala",
        "aadhaar","frozen","blocked","case","do not tell","don't tell","secret",
        "kyc expired","kyc update","atm pin","otp","verify your account",
        "prize money","lucky draw","won","processing fee","registration fee",
        "work from home","easy money","guaranteed return","crypto","bitcoin",
        "package stuck","customs duty","delivery fee","fake","impersonat",
        "video call","stay on call","digital arrest","cyber police",
    ]
    MEDIUM_KEYWORDS = [
        "verify","update","expire","urgent","immediately","limited time",
        "click here","link","download","install","share","account",
        "payment","transfer","send money","wallet","upi",
    ]

    high_hits = [k for k in HIGH_KEYWORDS if k in text_lower]
    med_hits  = [k for k in MEDIUM_KEYWORDS if k in text_lower]

    if len(high_hits) >= 3 or (len(high_hits) >= 1 and any(x in text_lower for x in ["pay","send","transfer","₹","rs.","lakh","thousand"])):
        risk_level = "HIGH"
        risk_score = min(95, 65 + len(high_hits) * 5)
    elif len(high_hits) >= 1 or len(med_hits) >= 3:
        risk_level = "MEDIUM"
        risk_score = min(65, 35 + len(high_hits) * 8 + len(med_hits) * 3)
    else:
        risk_level = "LOW"
        risk_score = max(10, len(med_hits) * 8)

    # Detect fraud type
    if any(x in text_lower for x in ["cbi","ed","customs","arrest","warrant","digital arrest"]):
        fraud_type = {"en":"Digital arrest scam","hi":"डिजिटल अरेस्ट स्कैम","te":"డిజిటల్ అరెస్ట్ మోసం","ta":"டிஜிட்டல் கைது மோசடி"}[lang]
    elif any(x in text_lower for x in ["kyc","atm pin","otp","bank","sbi","hdfc","account"]):
        fraud_type = {"en":"KYC / banking fraud","hi":"KYC / बैंकिंग धोखाधड़ी","te":"KYC / బ్యాంకింగ్ మోసం","ta":"KYC / வங்கி மோசடி"}[lang]
    elif any(x in text_lower for x in ["won","prize","lucky draw","lottery","kbc"]):
        fraud_type = {"en":"Lottery / prize fraud","hi":"लॉटरी / पुरस्कार धोखाधड़ी","te":"లాటరీ / బహుమతి మోసం","ta":"லாட்டரி / பரிசு மோசடி"}[lang]
    elif any(x in text_lower for x in ["job","work from home","salary","registration fee","training"]):
        fraud_type = {"en":"Job offer fraud","hi":"नौकरी धोखाधड़ी","te":"ఉద్యోగ మోసం","ta":"வேலை மோசடி"}[lang]
    else:
        fraud_type = {"en":"Suspicious activity","hi":"संदिग्ध गतिविधि","te":"అనుమానాస్పద కార్యకలాపం","ta":"சந்தேகமான செயல்"}[lang]

    flags_en = [
        "Request for immediate payment or money transfer",
        "Threat of arrest or legal action to create fear",
        "Demand for secrecy — 'do not tell anyone'",
        "Impersonation of government or bank official",
        "Unsolicited contact from unknown number",
    ]
    steps_en = [
        "Do NOT make any payment — hang up or stop responding immediately",
        "Do NOT share OTP, ATM PIN, Aadhaar, or bank details with anyone",
        "Call the National Cybercrime Helpline: 1930",
        "Report online at cybercrime.gov.in with call details and screenshots",
    ]

    flags_map = {
        "en": flags_en,
        "hi": ["तत्काल भुगतान या पैसे ट्रांसफर का अनुरोध","गिरफ्तारी या कानूनी कार्रवाई की धमकी","गोपनीयता की मांग — 'किसी को मत बताओ'","सरकारी या बैंक अधिकारी का प्रतिरूपण","अज्ञात नंबर से अनचाहा संपर्क"],
        "te": ["తక్షణ చెల్లింపు లేదా నగదు బదిలీ కోసం అభ్యర్థన","అరెస్ట్ లేదా చట్టపరమైన చర్య యొక్క బెదిరింపు","రహస్యానికి డిమాండ్ — 'ఎవరికీ చెప్పకండి'","ప్రభుత్వ లేదా బ్యాంక్ అధికారి వేషం","తెలియని నంబర్ నుండి అభ్యర్థించని సంప్రదింపు"],
        "ta": ["உடனடி கட்டணம் அல்லது பணம் பரிமாற்றம் கோரிக்கை","கைது அல்லது சட்ட நடவடிக்கை அச்சுறுத்தல்","இரகசிய கோரிக்கை — 'யாரிடமும் சொல்லாதே'","அரசாங்க அல்லது வங்கி அதிகாரியாக போலி","அறியப்படாத எண்ணிலிருந்து தேவையற்ற தொடர்பு"],
    }
    steps_map = {
        "en": steps_en,
        "hi": ["कोई भी पैसे न दें — तुरंत फोन काटें","OTP, ATM PIN, आधार या बैंक विवरण किसी को न दें","राष्ट्रीय साइबर अपराध हेल्पलाइन पर कॉल करें: 1930","cybercrime.gov.in पर शिकायत दर्ज करें"],
        "te": ["ఏ మొత్తమూ చెల్లించకండి — వెంటనే ఫోన్ కట్ చేయండి","OTP, ATM PIN, ఆధార్ లేదా బ్యాంక్ వివరాలు ఇవ్వకండి","జాతీయ సైబర్ క్రైమ్ హెల్ప్‌లైన్‌కు కాల్ చేయండి: 1930","cybercrime.gov.in లో ఫిర్యాదు నమోదు చేయండి"],
        "ta": ["எந்த கட்டணமும் செலுத்தாதீர்கள் — உடனடியாக தொடர்பை துண்டிக்கவும்","OTP, ATM PIN, ஆதார் அல்லது வங்கி விவரங்களை யாரிடமும் பகிர வேண்டாம்","தேசிய சைபர் குற்ற உதவி எண்: 1930","cybercrime.gov.in இல் புகாரளிக்கவும்"],
    }

    summaries = {
        "HIGH": {
            "en": "This interaction shows strong signs of fraud. You are likely being targeted by a scammer. Do not pay any money.",
            "hi": "यह बातचीत धोखाधड़ी के स्पष्ट संकेत दिखाती है। कोई पैसे न दें।",
            "te": "ఈ సంభాషణ మోసానికి స్పష్టమైన సంకేతాలు చూపిస్తోంది. ఏ మొత్తమూ చెల్లించకండి.",
            "ta": "இந்த தொடர்பு மோசடியின் தெளிவான அறிகுறிகளை காட்டுகிறது. எந்த பணமும் செலுத்தாதீர்கள்.",
        },
        "MEDIUM": {
            "en": "Some elements of this interaction are suspicious. Proceed with caution and verify through official channels before taking any action.",
            "hi": "इस बातचीत के कुछ तत्व संदिग्ध हैं। कोई भी कदम उठाने से पहले आधिकारिक माध्यमों से सत्यापित करें।",
            "te": "ఈ సంభాషణలో కొన్ని అంశాలు అనుమానాస్పదంగా ఉన్నాయి. అధికారిక మార్గాల ద్వారా ధృవీకరించండి.",
            "ta": "இந்த தொடர்பின் சில அம்சங்கள் சந்தேகமானவை. உத்தியோகபூர்வ வழிகள் மூலம் சரிபாருங்கள்.",
        },
        "LOW": {
            "en": "This interaction appears mostly safe, but always be cautious with unsolicited contacts and never share sensitive information.",
            "hi": "यह बातचीत अधिकतर सुरक्षित लगती है, लेकिन हमेशा सावधान रहें।",
            "te": "ఈ సంభాషణ చాలావరకు సురక్షితంగా కనిపిస్తోంది, కానీ ఎల్లప్పుడూ జాగ్రత్తగా ఉండండి.",
            "ta": "இந்த தொடர்பு பெரும்பாலும் பாதுகாப்பானதாக தெரிகிறது, ஆனால் எப்போதும் கவனமாக இருங்கள்.",
        },
    }

    report_to_map = {
        "en": "cybercrime.gov.in · National Cybercrime Helpline: 1930 · Nearest police station",
        "hi": "cybercrime.gov.in · राष्ट्रीय साइबर अपराध हेल्पलाइन: 1930 · नजदीकी पुलिस स्टेशन",
        "te": "cybercrime.gov.in · జాతీయ సైబర్ క్రైమ్ హెల్ప్‌లైన్: 1930 · సమీప పోలీస్ స్టేషన్",
        "ta": "cybercrime.gov.in · தேசிய சைபர் குற்ற உதவி: 1930 · அருகிலுள்ள காவல் நிலையம்",
    }

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "fraud_type": fraud_type,
        "summary": summaries[risk_level][lang],
        "red_flags": flags_map[lang][:min(len(high_hits)+2, 5)] if high_hits else flags_map[lang][:3],
        "immediate_steps": steps_map[lang],
        "report_to": report_to_map[lang],
        "_source": "offline_engine",
    }


# ── NCRP COMPLAINT DRAFT ──────────────────────────────────────────────────────
def get_ncrp_draft(result: dict, user_input: str, lang: str = "en") -> str:
    now = datetime.now().strftime("%d %B %Y, %H:%M IST")
    fraud_type = result.get("fraud_type", "Cybercrime / Fraud")
    flags = "\n".join(f"  - {f}" for f in result.get("red_flags", []))
    steps_note = "See immediate protective steps in Kavach app output."

    return f"""CYBERCRIME COMPLAINT DRAFT
Generated by Kavach — Citizen Fraud Shield
Date & Time: {now}
--------------------------------------------------

TO: Superintendent of Police (Cyber Crime)
    National Cybercrime Reporting Portal (NCRP)
    cybercrime.gov.in | Helpline: 1930

SUBJECT: Complaint regarding {fraud_type}

COMPLAINANT DETAILS:
  Name: [Your Full Name]
  Address: [Your Address]
  Mobile: [Your Mobile Number]
  Email: [Your Email]
  Aadhaar (last 4 digits): [XXXX]

INCIDENT DETAILS:
  Date of Incident: {datetime.now().strftime("%d %B %Y")}
  Fraud Category: {fraud_type}
  Risk Assessment: {result.get("risk_level","HIGH")} (Score: {result.get("risk_score",85)}/100)

DESCRIPTION OF INCIDENT:
{user_input}

RED FLAGS IDENTIFIED BY KAVACH AI:
{flags}

FINANCIAL DETAILS (if applicable):
  Amount Demanded: ₹ [Amount]
  Amount Paid (if any): ₹ [Amount]
  Mode of Payment: [UPI / Bank Transfer / Cash]
  UPI ID / Account No.: [Details]

EVIDENCE AVAILABLE:
  [ ] Screenshot of call / message
  [ ] WhatsApp chat screenshots
  [ ] Bank transaction records
  [ ] Screen recording
  [ ] Other: ___________

APPLICABLE SECTIONS (BNS / IT Act):
  - Section 318 BNS (Cheating / Fraud)
  - Section 319 BNS (Cheating by personation)
  - Section 66C IT Act (Identity theft)
  - Section 66D IT Act (Cheating by personation using computer resource)

DECLARATION:
I hereby declare that the above information is true and correct to the best of my knowledge.
I request appropriate legal action against the fraudsters.

Signature: _______________
Date: {datetime.now().strftime("%d/%m/%Y")}

--------------------------------------------------
This complaint was auto-generated by Kavach v1.0
ET AI Hackathon 2.0 · Problem Statement 6
Report online: cybercrime.gov.in
"""
