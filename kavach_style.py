KAVACH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── BACKGROUND ── */
.stApp { background: #F0F4FF; }
section[data-testid="stSidebar"] { background: #1A1A2E !important; }
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
section[data-testid="stSidebar"] .stSelectbox label { color: #94A3B8 !important; }

/* ── HEADER ── */
.kavach-hero {
    background: linear-gradient(135deg, #667EEA 0%, #764BA2 50%, #F093FB 100%);
    padding: 2.5rem 2.5rem 2rem; border-radius: 20px; color: white;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(102,126,234,0.4);
}
.kavach-hero::before {
    content: '🛡️'; position: absolute; right: 2rem; top: 50%;
    transform: translateY(-50%); font-size: 6rem; opacity: 0.15;
}
.kavach-hero h1 { margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; }
.kavach-hero p  { margin: 0.5rem 0 1rem; opacity: 0.9; font-size: 0.95rem; }
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.2); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.4); border-radius: 20px;
    padding: 4px 14px; font-size: 0.75rem; font-weight: 500;
    margin: 3px 4px 3px 0;
}

/* ── CARDS ── */
.card {
    background: white; border-radius: 16px; padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #E8EDFF;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.7rem; font-weight: 700; color: #8B9AC7;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;
}

/* ── RISK BOXES ── */
.risk-HIGH {
    background: linear-gradient(135deg, #FFF5F5, #FED7D7);
    border: 2px solid #FC8181; border-radius: 16px; padding: 1.25rem;
    box-shadow: 0 4px 15px rgba(252,129,129,0.2);
}
.risk-MEDIUM {
    background: linear-gradient(135deg, #FFFAF0, #FEEBC8);
    border: 2px solid #F6AD55; border-radius: 16px; padding: 1.25rem;
    box-shadow: 0 4px 15px rgba(246,173,85,0.2);
}
.risk-LOW {
    background: linear-gradient(135deg, #F0FFF4, #C6F6D5);
    border: 2px solid #68D391; border-radius: 16px; padding: 1.25rem;
    box-shadow: 0 4px 15px rgba(104,211,145,0.2);
}

/* ── FLAGS & STEPS ── */
.flag-item {
    background: linear-gradient(90deg, #FFF5EB, #FFFAF5);
    border-left: 4px solid #ED8936; padding: 0.7rem 1rem;
    margin: 0.4rem 0; border-radius: 0 10px 10px 0; font-size: 0.875rem;
    box-shadow: 0 2px 8px rgba(237,137,54,0.1);
}
.step-item {
    background: linear-gradient(90deg, #EBF8FF, #F0F9FF);
    border-left: 4px solid #4299E1; padding: 0.7rem 1rem;
    margin: 0.4rem 0; border-radius: 0 10px 10px 0; font-size: 0.875rem;
    box-shadow: 0 2px 8px rgba(66,153,225,0.1);
}

/* ── ALERT ── */
.alert-box {
    background: linear-gradient(135deg, #FFF5F5, #FED7D7);
    border: 2px solid #FC8181; border-radius: 14px;
    padding: 1.25rem; text-align: center; margin-top: 1rem;
    box-shadow: 0 4px 20px rgba(252,129,129,0.2);
}

/* ── STAT CARDS ── */
.stat-card {
    background: white; border-radius: 14px; padding: 1.25rem;
    text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #E8EDFF;
}
.stat-num   { font-size: 1.8rem; font-weight: 800; line-height: 1; }
.stat-label { font-size: 0.72rem; color: #8B9AC7; margin-top: 0.3rem; line-height: 1.4; }

/* ── EMPTY STATE ── */
.empty-state {
    background: white; border-radius: 20px; padding: 3.5rem 2rem;
    text-align: center; border: 2px dashed #C3D0FF;
    box-shadow: 0 4px 20px rgba(102,126,234,0.08);
}

/* ── BUTTONS ── */
.stButton > button {
    border-radius: 10px !important; font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667EEA, #764BA2) !important;
    border: none !important; color: white !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.5) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 12px; padding: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06); gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important; font-weight: 500 !important;
    color: #8B9AC7 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667EEA, #764BA2) !important;
    color: white !important;
}

/* ── NCRP ── */
.ncrp-box {
    background: #F0FFF4; border: 2px solid #68D391; border-radius: 12px;
    padding: 1rem; white-space: pre-wrap; font-family: monospace; font-size: 0.78rem;
    box-shadow: 0 2px 10px rgba(104,211,145,0.15);
}

/* ── SIDEBAR STATS ── */
.sidebar-stat {
    background: rgba(255,255,255,0.08); border-radius: 10px;
    padding: 0.75rem; text-align: center; border: 1px solid rgba(255,255,255,0.1);
}
.sidebar-stat-num   { font-size: 1.6rem; font-weight: 800; color: white !important; }
.sidebar-stat-label { font-size: 0.7rem; color: #94A3B8 !important; margin-top: 2px; }
</style>
"""
