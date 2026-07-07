CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* Hide streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }

/* ── HEADER ── */
.kv-header {
    background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 40%, #2563EB 100%);
    border-radius: 20px; padding: 2rem 2.5rem; color: white;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
    box-shadow: 0 10px 40px rgba(99,102,241,0.35);
}
.kv-header::before {
    content: ''; position: absolute; top: -40%; right: -10%;
    width: 400px; height: 400px; border-radius: 50%;
    background: rgba(255,255,255,0.06); pointer-events: none;
}
.kv-header h1 { margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; }
.kv-header p  { margin: 0.3rem 0 0; opacity: 0.75; font-size: 0.92rem; }
.kv-pill {
    display: inline-block; background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3); border-radius: 20px;
    padding: 3px 11px; font-size: 0.72rem; font-weight: 600;
    margin: 8px 4px 0 0; backdrop-filter: blur(4px);
}

/* ── CARDS ── */
.kv-card {
    background: white; border: 1px solid #EEF0F6;
    border-radius: 16px; padding: 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}
.kv-card-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #9CA3AF; margin-bottom: 1rem;
}

/* ── RISK BOXES ── */
.risk-HIGH {
    background: linear-gradient(135deg, #FFF1F1 0%, #FFE4E4 100%);
    border: 2px solid #FF4444; border-radius: 16px; padding: 1.25rem;
    box-shadow: 0 4px 16px rgba(255,68,68,0.15);
}
.risk-MEDIUM {
    background: linear-gradient(135deg, #FFFCF0 0%, #FFF3CC 100%);
    border: 2px solid #FFAA00; border-radius: 16px; padding: 1.25rem;
    box-shadow: 0 4px 16px rgba(255,170,0,0.15);
}
.risk-LOW {
    background: linear-gradient(135deg, #F0FFF8 0%, #CCFFE8 100%);
    border: 2px solid #00CC66; border-radius: 16px; padding: 1.25rem;
    box-shadow: 0 4px 16px rgba(0,204,102,0.12);
}

/* ── FLAGS & STEPS ── */
.flag-item {
    background: linear-gradient(90deg, #FFF7ED, #FFFAF5);
    border-left: 4px solid #FF6B00;
    padding: 0.65rem 1rem; margin: 0.3rem 0;
    border-radius: 0 10px 10px 0; font-size: 0.88rem; color: #374151;
}
.step-item {
    background: linear-gradient(90deg, #F0F4FF, #F8FAFF);
    border-left: 4px solid #4F46E5;
    padding: 0.65rem 1rem; margin: 0.3rem 0;
    border-radius: 0 10px 10px 0; font-size: 0.88rem; color: #374151;
}

/* ── STAT CARDS ── */
.kv-stat {
    background: white; border: 1px solid #EEF0F6;
    border-radius: 14px; padding: 1.1rem; text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.kv-stat-num   { font-size: 1.75rem; font-weight: 800; color: #1E1B4B; line-height: 1; }
.kv-stat-label { font-size: 0.72rem; color: #9CA3AF; margin-top: 0.3rem; line-height: 1.4; }

/* ── ALERT BOX ── */
.kv-alert {
    background: linear-gradient(135deg, #FFF1F1, #FFE4E4);
    border: 2px solid #FF4444; border-radius: 14px;
    padding: 1.25rem; text-align: center; margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(255,68,68,0.2);
}

/* ── EMPTY STATE ── */
.kv-empty {
    background: linear-gradient(135deg, #F8F5FF, #EEF2FF);
    border: 2px dashed #C4B5FD; border-radius: 18px;
    padding: 3rem; text-align: center;
}

/* ── NCRP BOX ── */
.kv-ncrp {
    background: #F0FFF8; border: 1.5px solid #00CC66;
    border-radius: 12px; padding: 1rem;
    white-space: pre-wrap; font-family: 'Courier New', monospace;
    font-size: 0.78rem; color: #065F46;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1B4B 0%, #312E81 100%) !important;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stSelectbox label { color: #A5B4FC !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

.kv-sidebar-stat {
    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px; padding: 1rem; text-align: center;
}
.kv-sidebar-stat-num { font-size: 1.8rem; font-weight: 800; color: white !important; }
.kv-sidebar-stat-label { font-size: 0.72rem; color: #A5B4FC !important; }

/* ── BUTTONS ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C3AED, #4F46E5) !important;
    border: none !important; border-radius: 12px !important;
    font-weight: 700 !important; font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important; letter-spacing: 0.01em !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(99,102,241,0.6) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:not([kind="primary"]) {
    border-radius: 10px !important; font-weight: 600 !important;
    border: 1.5px solid #E5E7EB !important; font-size: 0.82rem !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: #F3F4F6;
    border-radius: 14px; padding: 5px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.85rem !important; padding: 0.45rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
}

/* ── RADIO ── */
.stRadio > div { gap: 0.5rem; }
.stRadio label {
    background: #F9FAFB; border: 1.5px solid #E5E7EB;
    border-radius: 10px; padding: 0.4rem 0.9rem !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    cursor: pointer; transition: all 0.15s;
}
.stRadio label:hover { border-color: #7C3AED; background: #F5F3FF; }

/* ── TEXT AREA ── */
.stTextArea textarea {
    border-radius: 12px !important; border: 1.5px solid #E5E7EB !important;
    font-size: 0.9rem !important; line-height: 1.6 !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}
</style>
"""
