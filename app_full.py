"""
Kavach — AI-Powered Citizen Fraud Shield
ET AI Hackathon 2.0 | Problem Statement 6
Author: Abdul Nafisa Sulthana
Full version: Fraud Check + Network Graph + Crime Map + 
              Counterfeit Currency + WhatsApp Simulator + History + Dashboard
"""

import streamlit as st
import json, re, random
from datetime import datetime
from kavach_utils import FRAUD_EXAMPLES, UI_TEXT, offline_rule_check, get_ncrp_draft

st.set_page_config(page_title="Kavach — Citizen Fraud Shield", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.kv-header {
    background: linear-gradient(120deg, #6C3CE1 0%, #9B5DE5 40%, #F72585 100%);
    padding: 2.2rem 2.5rem; border-radius: 20px; color: white;
    margin-bottom: 1.8rem; box-shadow: 0 12px 40px rgba(108,60,225,0.35);
}
.kv-header h1 { margin:0; font-size:2.3rem; font-weight:800; letter-spacing:-1px; }
.kv-header p  { margin:0.4rem 0 0.8rem; opacity:0.88; font-size:0.92rem; }
.kv-pill {
    display:inline-block; background:rgba(255,255,255,0.18);
    border:1px solid rgba(255,255,255,0.35); border-radius:30px;
    padding:3px 12px; font-size:0.72rem; font-weight:600; margin:3px 4px 0 0;
}
.kv-card {
    background:white; border-radius:16px; border:1.5px solid #F1F0FB;
    padding:1.4rem 1.5rem; margin-bottom:1rem;
    box-shadow:0 4px 20px rgba(108,60,225,0.07);
}
.kv-label { font-size:0.68rem; font-weight:700; color:#9B5DE5;
    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.7rem; }
.risk-HIGH   { background:linear-gradient(135deg,#FFF1F2,#FFE4E6); border:2px solid #FB7185; border-radius:16px; padding:1.4rem; }
.risk-MEDIUM { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border:2px solid #FBBF24; border-radius:16px; padding:1.4rem; }
.risk-LOW    { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); border:2px solid #4ADE80; border-radius:16px; padding:1.4rem; }
.kv-flag { background:#FFF7ED; border-left:3px solid #F97316;
    padding:0.55rem 1rem; margin:0.3rem 0; border-radius:0 10px 10px 0; font-size:0.87rem; color:#7C3100; }
.kv-step { background:linear-gradient(90deg,#F5F3FF,#FAF5FF); border-left:3px solid #8B5CF6;
    padding:0.55rem 1rem; margin:0.3rem 0; border-radius:0 10px 10px 0; font-size:0.87rem; color:#3730A3; }
.kv-alert { background:linear-gradient(135deg,#FFF1F2,#FFE4E6);
    border:2px solid #FB7185; border-radius:14px; padding:1.3rem; text-align:center; margin-top:1rem; }
.kv-stat { background:linear-gradient(135deg,#F5F3FF,#FAF5FF);
    border:1.5px solid #DDD6FE; border-radius:14px; padding:1.2rem; text-align:center; }
.kv-stat-num { font-size:1.9rem; font-weight:800; color:#6C3CE1; line-height:1; }
.kv-stat-lbl { font-size:0.72rem; color:#7C3AED; margin-top:0.3rem; font-weight:500; }
.kv-empty { background:linear-gradient(135deg,#F5F3FF,#FAF5FF);
    border:2px dashed #C4B5FD; border-radius:20px; padding:3rem; text-align:center; }
.kv-ncrp { background:#F0FDF4; border:1.5px solid #4ADE80; border-radius:12px;
    padding:1rem; white-space:pre-wrap; font-family:monospace; font-size:0.78rem; color:#14532D; }

/* WhatsApp chat */
.wa-screen { background:#0A0A0A; border-radius:16px; padding:0; overflow:hidden; max-width:380px; margin:auto; box-shadow:0 8px 32px rgba(0,0,0,0.4); }
.wa-header { background:#128C7E; padding:0.8rem 1rem; display:flex; align-items:center; gap:10px; }
.wa-avatar { width:36px;height:36px;background:#25D366;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem; }
.wa-name { color:white;font-weight:600;font-size:0.9rem; }
.wa-status { color:rgba(255,255,255,0.7);font-size:0.72rem; }
.wa-body { background:#ECE5DD; padding:1rem; min-height:260px; }
.wa-msg-in { background:white; border-radius:0 12px 12px 12px; padding:0.6rem 0.8rem;
    margin:0.4rem 0; max-width:85%; font-size:0.82rem; color:#111; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
.wa-msg-out { background:#DCF8C6; border-radius:12px 0 12px 12px; padding:0.6rem 0.8rem;
    margin:0.4rem 0 0.4rem auto; max-width:85%; font-size:0.82rem; color:#111;
    box-shadow:0 1px 3px rgba(0,0,0,0.1); text-align:right; }
.wa-time { font-size:0.65rem; color:#999; margin-top:3px; }
.wa-kavach { background:linear-gradient(135deg,#6C3CE1,#9B5DE5); color:white;
    border-radius:12px; padding:0.8rem; margin:0.4rem 0; font-size:0.8rem; }

/* Currency check */
.note-feature { border-radius:10px; padding:0.6rem 0.9rem; margin:0.3rem 0; font-size:0.85rem; }
.feat-pass { background:#F0FDF4; border-left:3px solid #4ADE80; color:#14532D; }
.feat-fail { background:#FFF1F2; border-left:3px solid #FB7185; color:#BE123C; }
.feat-warn { background:#FFFBEB; border-left:3px solid #FBBF24; color:#92400E; }

#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

for k,v in [("lang","en"),("scan_count",0),("high_count",0),("history",[]),("result",None),("input_text",""),("wa_messages",[]),("currency_result",None)]:
    if k not in st.session_state: st.session_state[k]=v

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ Kavach")
    lang_options={"🇬🇧 English":"en","🇮🇳 हिन्दी":"hi","🇮🇳 తెలుగు":"te","🇮🇳 தமிழ்":"ta"}
    sel=st.selectbox("Language",list(lang_options.keys()))
    st.session_state.lang=lang_options[sel]; lang=st.session_state.lang
    st.divider()
    st.markdown("**Session Stats**")
    c1,c2=st.columns(2)
    c1.markdown(f'<div class="kv-stat"><div class="kv-stat-num">{st.session_state.scan_count}</div><div class="kv-stat-lbl">Scans</div></div>',unsafe_allow_html=True)
    c2.markdown(f'<div class="kv-stat"><div class="kv-stat-num" style="color:#F72585">{st.session_state.high_count}</div><div class="kv-stat-lbl">High Risk</div></div>',unsafe_allow_html=True)
    st.divider()
    st.markdown('<div style="background:linear-gradient(135deg,#FFF1F2,#FFE4E6);border:2px solid #FB7185;border-radius:12px;padding:1rem;text-align:center"><div style="font-weight:700;color:#BE123C">🚨 Emergency</div><div style="font-size:1.8rem;font-weight:800;color:#E11D48">1930</div><div style="font-size:0.75rem;color:#BE123C">National Cybercrime Helpline</div></div>',unsafe_allow_html=True)
    st.markdown("")
    st.markdown("🔗 [cybercrime.gov.in](https://cybercrime.gov.in)")
    st.divider()
    st.caption("Kavach v1.0 · ET AI Hackathon 2.0\nProblem Statement 6 · Public Safety\n_Offline AI — no API key needed_")

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kv-header">
  <h1>🛡️ Kavach · कवच · కవచ్ · கவசம்</h1>
  <p>AI-Powered Citizen Fraud Shield · Real-time protection before money moves</p>
  <span class="kv-pill">🚔 Digital Arrest</span>
  <span class="kv-pill">💳 KYC Fraud</span>
  <span class="kv-pill">🎰 Lottery Scam</span>
  <span class="kv-pill">💼 Job Fraud</span>
  <span class="kv-pill">💵 Counterfeit Currency</span>
  <span class="kv-pill">💬 WhatsApp Bot</span>
  <span class="kv-pill">🕸️ Fraud Networks</span>
  <span class="kv-pill">🗺️ Crime Map</span>
</div>
""",unsafe_allow_html=True)

ui=UI_TEXT[lang]
tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs([
    "🔍 Fraud Check",
    "💵 Currency Check",
    "💬 WhatsApp Bot",
    "🕸️ Fraud Networks",
    "🗺️ Crime Map",
    "📋 History",
    "📊 Dashboard"
])

# ══ TAB 1 — FRAUD CHECK ══════════════════════════════════════════════════════
with tab1:
    L,R=st.columns([1.15,0.85],gap="large")
    with L:
        st.markdown('<div class="kv-card"><div class="kv-label">What are you checking?</div>',unsafe_allow_html=True)
        mode=st.radio("",["call_message","payment","link","screenshot"],
            format_func=lambda x:{"call_message":"📞 Call / Message","payment":"💳 Payment Request","link":"🔗 Suspicious Link","screenshot":"📷 Screenshot"}[x],
            horizontal=True,label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="kv-card"><div class="kv-label">⚡ Quick load examples</div>',unsafe_allow_html=True)
        examples=FRAUD_EXAMPLES[lang]; ec=st.columns(4)
        for i,(key,val) in enumerate(examples.items()):
            with ec[i]:
                if st.button(key,use_container_width=True,key=f"ex_{i}"):
                    st.session_state.input_text=val; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="kv-card"><div class="kv-label">Describe the suspicious interaction</div>',unsafe_allow_html=True)
        user_input=st.text_area("",value=st.session_state.input_text,height=155,
            placeholder="e.g. Someone called saying they are from CBI and my Aadhaar is linked to money laundering...",
            label_visibility="collapsed")
        if st.button("🔍 Analyze for Fraud Risk",type="primary",use_container_width=True):
            if user_input.strip():
                with st.spinner("Analyzing with Kavach AI..."):
                    result=offline_rule_check(user_input,lang)
                st.session_state.result=result; st.session_state.scan_count+=1
                if result.get("risk_level")=="HIGH": st.session_state.high_count+=1
                st.session_state.history.append({"time":datetime.now().strftime("%d %b %H:%M"),
                    "input":user_input[:70]+("..." if len(user_input)>70 else ""),
                    "risk":result.get("risk_level","?"),"type":result.get("fraud_type","—"),
                    "score":int(result.get("risk_score",50))})
                st.rerun()
            else: st.warning("Please describe the suspicious interaction first.")
        st.markdown('</div>',unsafe_allow_html=True)

    with R:
        result=st.session_state.result
        if result:
            rl=result.get("risk_level","MEDIUM"); score=int(result.get("risk_score",50))
            icon={"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(rl,"🟡")
            label={"HIGH":ui['risk_high'],"MEDIUM":ui['risk_medium'],"LOW":ui['risk_low']}.get(rl,"")
            flags=result.get("red_flags",[]); steps=result.get("immediate_steps",[])
            st.markdown(f'<div class="risk-{rl}">',unsafe_allow_html=True)
            st.markdown(f"### {icon} {label}")
            st.markdown(f"<span style='background:#6C3CE1;color:white;padding:2px 10px;border-radius:20px;font-size:0.8rem;font-weight:600'>{result.get('fraud_type','—')}</span>",unsafe_allow_html=True)
            st.markdown("")
            st.progress(score/100,text=f"Risk Score: **{score}/100**")
            st.markdown(f"<div style='margin-top:0.5rem;font-size:0.9rem;color:#374151'>{result.get('summary','')}</div>",unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True); st.markdown("")
            if flags:
                st.markdown('<div class="kv-card"><div class="kv-label">🚩 Red Flags Detected</div>',unsafe_allow_html=True)
                for f in flags: st.markdown(f'<div class="kv-flag">⚠️ {f}</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
            if steps:
                st.markdown('<div class="kv-card"><div class="kv-label">✅ What to do right now</div>',unsafe_allow_html=True)
                for i,s in enumerate(steps,1): st.markdown(f'<div class="kv-step"><b>{i}.</b> {s}</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
            if rl=="HIGH":
                st.markdown('<div class="kv-alert"><div style="font-weight:700;color:#BE123C">🚨 Report this fraud immediately!</div><div style="font-size:2rem;font-weight:800;color:#E11D48">1930</div><a href="https://cybercrime.gov.in" target="_blank" style="color:#BE123C">cybercrime.gov.in</a></div>',unsafe_allow_html=True)
                with st.expander("📄 Auto-generate NCRP Complaint"):
                    draft=get_ncrp_draft(result,user_input,lang)
                    st.markdown(f'<div class="kv-ncrp">{draft}</div>',unsafe_allow_html=True)
                    st.download_button("⬇️ Download complaint",data=draft,file_name=f"kavach_ncrp_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",mime="text/plain")
        else:
            st.markdown('<div class="kv-empty"><div style="font-size:3.5rem">🛡️</div><div style="font-size:1.15rem;font-weight:700;color:#6C3CE1;margin-top:1rem">Kavach is ready</div><div style="color:#7C3AED;margin-top:0.5rem;font-size:0.9rem">Click a quick example or describe a suspicious interaction</div></div>',unsafe_allow_html=True)

# ══ TAB 2 — COUNTERFEIT CURRENCY ═════════════════════════════════════════════
with tab2:
    st.markdown("#### 💵 Counterfeit Currency Identification")
    st.caption("AI checks ₹500 / ₹2000 note security features — deployable on mobile, bank counters, and PoS terminals")

    CL,CR=st.columns([1,1],gap="large")
    with CL:
        st.markdown('<div class="kv-card"><div class="kv-label">Select denomination</div>',unsafe_allow_html=True)
        denom=st.selectbox("",["₹500 Note","₹2000 Note","₹200 Note","₹100 Note"],label_visibility="collapsed")
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="kv-card"><div class="kv-label">Describe the note or upload image</div>',unsafe_allow_html=True)
        note_img=st.file_uploader("Upload note image (optional)",type=["jpg","jpeg","png"])
        note_desc=st.text_area("Describe suspicious features",height=120,
            placeholder="e.g. The security thread is missing, Gandhi watermark is blurry, serial number font looks different, color shifts when tilted...")
        check_btn=st.button("🔍 Check for Counterfeit",type="primary",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="kv-card"><div class="kv-label">Quick suspicious scenarios</div>',unsafe_allow_html=True)
        sc1,sc2=st.columns(2)
        with sc1:
            if st.button("Missing security thread",use_container_width=True):
                st.session_state.currency_result={
                    "verdict":"LIKELY FAKE","score":91,
                    "features":[("Security thread","FAIL","Missing or not visible — genuine notes have embedded thread"),
                        ("Watermark","WARN","Verify Gandhi portrait watermark against light"),
                        ("Serial number","WARN","Check font consistency — fake notes often use wrong typeface"),
                        ("Color shift ink","FAIL","Numeral 500/2000 should shift green→blue when tilted"),
                        ("Microprint","FAIL","'RBI' microtext on thread not visible — may be printed on paper"),],
                    "action":"Do NOT accept this note. Report to nearest bank or police station immediately."}
                st.rerun()
        with sc2:
            if st.button("Blurry Gandhi image",use_container_width=True):
                st.session_state.currency_result={
                    "verdict":"SUSPICIOUS","score":67,
                    "features":[("Security thread","PASS","Thread appears present"),
                        ("Watermark","FAIL","Gandhi portrait watermark appears blurry or faint — possible fake"),
                        ("Serial number","PASS","Font appears consistent"),
                        ("Color shift ink","WARN","Tilt the note to confirm green→blue shift"),
                        ("Paper texture","WARN","Genuine notes have distinct feel — compare with known genuine note"),],
                    "action":"Proceed with caution. Verify with bank branch UV scanner before accepting."}
                st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

        if check_btn and (note_desc.strip() or note_img):
            desc_lower=(note_desc or "").lower()
            fail_signals=["missing","not visible","blurry","wrong","different","fake","no thread","no watermark","poor","bad print"]
            fail_count=sum(1 for s in fail_signals if s in desc_lower)
            if fail_count>=3: verdict,vscore="LIKELY FAKE",88
            elif fail_count>=1: verdict,vscore="SUSPICIOUS",62
            else: verdict,vscore="APPEARS GENUINE",18
            st.session_state.currency_result={
                "verdict":verdict,"score":vscore,
                "features":[
                    ("Security thread","PASS" if "thread" not in desc_lower else "FAIL","Embedded security thread check"),
                    ("Watermark","PASS" if "watermark" not in desc_lower else "FAIL","Gandhi portrait watermark"),
                    ("Serial number","PASS" if "serial" not in desc_lower else "WARN","Serial number font & format"),
                    ("Color shift ink","WARN","Tilt note to verify green→blue color shift on numeral"),
                    ("Microprint","PASS" if "micro" not in desc_lower else "FAIL","'RBI' microtext on security thread"),
                ],
                "action":"Report to nearest bank or call 1930 if you suspect counterfeit." if vscore>50 else "Note appears genuine. Keep for reference."}
            st.rerun()

    with CR:
        cr=st.session_state.currency_result
        if cr:
            v=cr["verdict"]; vs=cr["score"]
            vcolor={"LIKELY FAKE":"#E11D48","SUSPICIOUS":"#D97706","APPEARS GENUINE":"#16A34A"}.get(v,"#6B7280")
            vbg={"LIKELY FAKE":"#FFF1F2","SUSPICIOUS":"#FFFBEB","APPEARS GENUINE":"#F0FDF4"}.get(v,"#F9FAFB")
            vborder={"LIKELY FAKE":"#FB7185","SUSPICIOUS":"#FCD34D","APPEARS GENUINE":"#4ADE80"}.get(v,"#E5E7EB")
            st.markdown(f'<div style="background:{vbg};border:2px solid {vborder};border-radius:16px;padding:1.4rem;margin-bottom:1rem">',unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:1.5rem;font-weight:800;color:{vcolor}'>{v}</div>",unsafe_allow_html=True)
            st.progress(vs/100,text=f"Suspicion Score: {vs}/100")
            st.markdown(f"<div style='font-size:0.85rem;color:#374151;margin-top:0.5rem'>{cr['action']}</div>",unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

            st.markdown('<div class="kv-card"><div class="kv-label">Security Feature Analysis</div>',unsafe_allow_html=True)
            for feat,status,desc in cr["features"]:
                cls={"PASS":"feat-pass","FAIL":"feat-fail","WARN":"feat-warn"}.get(status,"feat-warn")
                icon2={"PASS":"✅","FAIL":"❌","WARN":"⚠️"}.get(status,"⚠️")
                st.markdown(f'<div class="note-feature {cls}"><b>{icon2} {feat}</b> — <span style="font-weight:600">{status}</span><br><span style="font-size:0.8rem">{desc}</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

            st.markdown('<div class="kv-card"><div class="kv-label">Genuine Note Security Features</div>',unsafe_allow_html=True)
            st.markdown("""
**₹500 / ₹2000 — What to check:**
- 🧵 **Security thread** — embedded, reads 'भारत' / 'RBI'
- 👤 **Watermark** — Gandhi portrait visible against light
- 🎨 **Color-shift ink** — numeral shifts green→blue when tilted  
- 🔢 **Serial number** — consistent RBI font, no blur
- 📄 **Paper feel** — crisp, distinct texture vs regular paper
- 🔬 **Microprint** — 'RBI' text on thread (needs magnifier)
- ⬆️ **Raised print** — 'RBI', Ashoka Pillar feel raised to touch
""")
            st.markdown('</div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="kv-empty"><div style="font-size:3rem">💵</div><div style="font-size:1.1rem;font-weight:700;color:#6C3CE1;margin-top:1rem">Currency Checker Ready</div><div style="color:#7C3AED;font-size:0.9rem;margin-top:0.5rem">Describe suspicious note features or click a quick scenario</div></div>',unsafe_allow_html=True)

# ══ TAB 3 — WHATSAPP BOT SIMULATOR ══════════════════════════════════════════
with tab3:
    st.markdown("#### 💬 WhatsApp Fraud Detection Bot")
    st.caption("Simulation of Kavach's WhatsApp channel — citizens send suspicious messages directly on WhatsApp and get instant fraud verdicts")

    WL,WR=st.columns([1,1.2],gap="large")
    with WL:
        st.markdown('<div class="kv-card"><div class="kv-label">How it works in production</div>',unsafe_allow_html=True)
        st.markdown("""
**Citizens WhatsApp Kavach at:**  
📱 `+91-XXXX-KAVACH`

**What they can send:**
- 📝 Describe a suspicious call
- 📸 Screenshot of scam message
- 🔗 Suspicious link for check
- 📞 Scammer's phone number

**Kavach replies in < 4 seconds with:**
- Risk verdict (HIGH/MEDIUM/LOW)  
- Red flags detected
- Protective steps in their language
- NCRP complaint link if HIGH risk

**Tech stack:**  
Twilio WhatsApp API → FastAPI webhook → Kavach AI engine → Response
""")
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="kv-card"><div class="kv-label">Try the simulator</div>',unsafe_allow_html=True)
        wa_examples={
            "Digital arrest scam":"Someone called from CBI saying my Aadhaar is in a money laundering case. They want ₹1.5 lakh urgently.",
            "KYC fraud SMS":"Got SMS: Your SBI KYC expired. Click sbi-kyc-update.in to update or account blocked.",
            "Lottery fraud":"Call saying I won ₹25 lakh in KBC. Need to pay ₹15,000 processing fee first.",
        }
        wa_sel=st.selectbox("Select example",list(wa_examples.keys()))
        wa_custom=st.text_input("Or type your own message","")
        if st.button("📤 Send to Kavach WhatsApp Bot",type="primary",use_container_width=True):
            msg=wa_custom if wa_custom.strip() else wa_examples[wa_sel]
            result_wa=offline_rule_check(msg,"en")
            rl_wa=result_wa.get("risk_level","MEDIUM")
            score_wa=int(result_wa.get("risk_score",50))
            ftype_wa=result_wa.get("fraud_type","Unknown")
            flags_wa=result_wa.get("red_flags",[])[:3]
            steps_wa=result_wa.get("immediate_steps",[])[:2]
            risk_emoji={"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(rl_wa,"🟡")
            reply=f"{risk_emoji} *KAVACH ALERT — {rl_wa} RISK*\n\n*Fraud type:* {ftype_wa}\n*Risk score:* {score_wa}/100\n\n*🚩 Red flags:*\n"+"".join(f"• {f}\n" for f in flags_wa)+f"\n*✅ Do this now:*\n"+"".join(f"{i+1}. {s}\n" for i,s in enumerate(steps_wa))
            if rl_wa=="HIGH": reply+="\n🚨 *Call 1930 immediately*\ncybercrime.gov.in"
            st.session_state.wa_messages=[
                {"from":"user","text":msg,"time":datetime.now().strftime("%H:%M")},
                {"from":"kavach","text":reply,"time":datetime.now().strftime("%H:%M")},
            ]
            st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

    with WR:
        st.markdown('<div class="kv-card"><div class="kv-label">WhatsApp Chat Preview</div>',unsafe_allow_html=True)
        msgs=st.session_state.wa_messages
        chat_html='<div class="wa-screen"><div class="wa-header"><div class="wa-avatar">🛡️</div><div><div class="wa-name">Kavach Fraud Shield</div><div class="wa-status">🟢 Online · Powered by AI</div></div></div><div class="wa-body">'
        if not msgs:
            chat_html+='<div style="text-align:center;padding:2rem;color:#666;font-size:0.85rem">Send a message to see Kavach reply instantly 👆</div>'
        for m in msgs:
            t=m["time"]
            if m["from"]=="user":
                chat_html+=f'<div class="wa-msg-out">{m["text"]}<div class="wa-time">{t} ✓✓</div></div>'
            else:
                txt=m["text"].replace("\n","<br>").replace("*","<b>",1)
                # Simple bold replace
                import re as _re
                txt=_re.sub(r'\*([^*]+)\*',r'<b>\1</b>',m["text"].replace("\n","<br>"))
                chat_html+=f'<div class="wa-kavach">{txt}<div class="wa-time" style="color:rgba(255,255,255,0.7)">{t}</div></div>'
        chat_html+='</div></div>'
        st.markdown(chat_html,unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 4 — FRAUD NETWORK ════════════════════════════════════════════════════
with tab4:
    st.markdown("#### 🕸️ Fraud Network Graph Intelligence")
    st.caption("AI maps scammer linkages — phone numbers, bank accounts, mule networks — for court-admissible intelligence packages")
    ca,cb=st.columns([1.2,1],gap="large")
    with ca:
        st.markdown('<div class="kv-card"><div class="kv-label">Live Fraud Ring — Digital Arrest Network</div>',unsafe_allow_html=True)
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            G=nx.DiGraph()
            colors_map={"Ring Leader\n(Cambodia)":"#F72585","Caller A\n+91-98XXX-1111":"#FF9F1C","Caller B\n+91-97XXX-2222":"#FF9F1C","Fake CBI\nPortal":"#9B5DE5","Mule Acc 1\nSBI-XXXX1234":"#FFBE0B","Mule Acc 2\nHDFC-XXXX5678":"#FFBE0B","Mule Acc 3\nPaytm-XXXX9012":"#FFBE0B","Victim 1\n₹2.1L lost":"#FB5607","Victim 2\n₹85K lost":"#FB5607","Victim 3\n₹3.4L lost":"#FB5607"}
            edges=[("Ring Leader\n(Cambodia)","Caller A\n+91-98XXX-1111"),("Ring Leader\n(Cambodia)","Caller B\n+91-97XXX-2222"),("Ring Leader\n(Cambodia)","Fake CBI\nPortal"),("Caller A\n+91-98XXX-1111","Victim 1\n₹2.1L lost"),("Caller A\n+91-98XXX-1111","Victim 2\n₹85K lost"),("Caller B\n+91-97XXX-2222","Victim 3\n₹3.4L lost"),("Victim 1\n₹2.1L lost","Mule Acc 1\nSBI-XXXX1234"),("Victim 2\n₹85K lost","Mule Acc 2\nHDFC-XXXX5678"),("Victim 3\n₹3.4L lost","Mule Acc 3\nPaytm-XXXX9012"),("Mule Acc 1\nSBI-XXXX1234","Ring Leader\n(Cambodia)"),("Mule Acc 2\nHDFC-XXXX5678","Ring Leader\n(Cambodia)"),("Mule Acc 3\nPaytm-XXXX9012","Ring Leader\n(Cambodia)")]
            G.add_nodes_from(colors_map.keys()); G.add_edges_from(edges)
            pos=nx.spring_layout(G,seed=7,k=2.2)
            fig,ax=plt.subplots(figsize=(7,5.5)); fig.patch.set_facecolor('#FAFAFF'); ax.set_facecolor('#FAFAFF')
            for node,col in colors_map.items():
                nx.draw_networkx_nodes(G,pos,nodelist=[node],node_color=col,node_size=1400,ax=ax,alpha=0.92)
            nx.draw_networkx_edges(G,pos,ax=ax,edge_color='#C4B5FD',arrows=True,arrowsize=18,width=1.8,connectionstyle='arc3,rad=0.12')
            nx.draw_networkx_labels(G,pos,ax=ax,font_size=5.8,font_weight='bold',font_color='#1E1B4B')
            legend_items=[mpatches.Patch(color='#F72585',label='Ring Leader'),mpatches.Patch(color='#FF9F1C',label='Callers'),mpatches.Patch(color='#9B5DE5',label='Fake Portals'),mpatches.Patch(color='#FFBE0B',label='Mule Accounts'),mpatches.Patch(color='#FB5607',label='Victims')]
            ax.legend(handles=legend_items,loc='lower left',fontsize=7.5,framealpha=0.9,edgecolor='#DDD6FE')
            ax.axis('off'); plt.tight_layout(pad=0.5); st.pyplot(fig); plt.close()
        except ImportError:
            st.info("pip install networkx matplotlib")
        st.markdown('</div>',unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="kv-card"><div class="kv-label">Network Intelligence Summary</div>',unsafe_allow_html=True)
        for label,value,bg,tc in [("🔴 Ring Leader","Cambodia-based operation","#FFF1F2","#BE123C"),("📞 Scam Numbers","2 active · 847 complaints linked","#FFF7ED","#92400E"),("🏦 Mule Accounts","3 accounts · ₹6.2L routed","#FFFBEB","#92400E"),("👥 Victims","3 confirmed · est. 40+ total","#FFF1F2","#BE123C"),("🌐 Fake Portal","cbionline-verify.in (taken down)","#F5F3FF","#4C1D95"),("⚖️ Legal Status","FIR filed · ED lookout issued","#F0FDF4","#14532D")]:
            st.markdown(f'<div style="background:{bg};border-radius:10px;padding:0.65rem 0.9rem;margin:0.35rem 0"><div style="font-weight:700;color:{tc};font-size:0.85rem">{label}</div><div style="font-size:0.82rem;color:#374151;margin-top:2px">{value}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 5 — CRIME MAP ════════════════════════════════════════════════════════
with tab5:
    st.markdown("#### 🗺️ Geospatial Crime Pattern Intelligence")
    st.caption("Ward-level cybercrime hotspot mapping — helps law enforcement deploy resources before fraud peaks")
    try:
        import folium
        from streamlit_folium import st_folium
        m=folium.Map(location=[20.5937,78.9629],zoom_start=5,tiles="CartoDB positron")
        hotspots=[(28.6139,77.2090,"New Delhi",9420,"HIGH"),(19.0760,72.8777,"Mumbai",8130,"HIGH"),(12.9716,77.5946,"Bengaluru",6240,"HIGH"),(17.3850,78.4867,"Hyderabad",5870,"HIGH"),(13.0827,80.2707,"Chennai",4920,"MEDIUM"),(22.5726,88.3639,"Kolkata",4670,"MEDIUM"),(23.0225,72.5714,"Ahmedabad",3840,"MEDIUM"),(18.5204,73.8567,"Pune",3210,"MEDIUM"),(26.8467,80.9462,"Lucknow",2980,"MEDIUM"),(16.3067,80.4365,"Vijayawada",1240,"MEDIUM"),(17.6868,83.2185,"Visakhapatnam",1120,"LOW"),(21.1458,79.0882,"Nagpur",1870,"LOW"),(25.5941,85.1376,"Patna",1680,"MEDIUM")]
        cmap={"HIGH":"#F72585","MEDIUM":"#FF9F1C","LOW":"#4ADE80"}
        for lat,lon,city,n,lvl in hotspots:
            folium.CircleMarker(location=[lat,lon],radius=n/130,color=cmap[lvl],fill=True,fill_color=cmap[lvl],fill_opacity=0.55,weight=2,popup=folium.Popup(f"<b>{city}</b><br>Complaints: {n:,}<br>Risk: <b>{lvl}</b>",max_width=180),tooltip=f"📍 {city}: {n:,} complaints").add_to(m)
        cm2,ci2=st.columns([1.6,1])
        with cm2: st_folium(m,width=None,height=430)
        with ci2:
            st.markdown('<div class="kv-card"><div class="kv-label">Top hotspots 2024</div>',unsafe_allow_html=True)
            for _,_,city,n,lvl in sorted(hotspots,key=lambda x:-x[3])[:8]:
                c={"HIGH":"#F72585","MEDIUM":"#FF9F1C","LOW":"#4ADE80"}[lvl]
                st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #F3F4F6"><span style="font-size:0.88rem">📍 {city}</span><span style="color:{c};font-weight:700">{n:,}</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
    except ImportError:
        st.info("pip install folium streamlit-folium")
        import pandas as pd
        st.dataframe(pd.DataFrame({"City":["New Delhi","Mumbai","Bengaluru","Hyderabad","Vijayawada"],"Complaints":[9420,8130,6240,5870,1240],"Risk":["HIGH","HIGH","HIGH","HIGH","MEDIUM"]}),use_container_width=True,hide_index=True)

# ══ TAB 6 — HISTORY ══════════════════════════════════════════════════════════
with tab6:
    st.markdown("#### 📋 Scan History")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            icon={"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(item["risk"],"⚪")
            with st.expander(f"{icon} [{item['time']}] {item['type']} — {item['input']}"):
                c1,c2,c3=st.columns(3)
                c1.metric("Risk",item["risk"]); c2.metric("Score",f"{item['score']}/100"); c3.metric("Type",item["type"])
        if st.button("🗑️ Clear history"): st.session_state.history=[]; st.rerun()
    else: st.info("No scans yet — go to Fraud Check and analyze something!")

# ══ TAB 7 — DASHBOARD ════════════════════════════════════════════════════════
with tab7:
    st.markdown("#### 📊 National Cybercrime Dashboard")
    c1,c2,c3,c4=st.columns(4)
    for col,num,lbl in zip([c1,c2,c3,c4],["₹1,776Cr","11.4L+","60%","1930"],["Lost to digital arrest scams (2024)","Cybercrime complaints in 2023","YoY growth in cybercrime","National Cybercrime Helpline"]):
        col.markdown(f'<div class="kv-stat"><div class="kv-stat-num">{num}</div><div class="kv-stat-lbl">{lbl}</div></div>',unsafe_allow_html=True)
    st.divider()
    if st.session_state.history:
        import pandas as pd
        df=pd.DataFrame(st.session_state.history)
        ca,cb=st.columns(2)
        with ca: st.markdown("**Risk distribution**"); st.bar_chart(df["risk"].value_counts())
        with cb: st.markdown("**Fraud types**"); st.dataframe(df["type"].value_counts().reset_index().rename(columns={"index":"Type","type":"Count"}),use_container_width=True,hide_index=True)
    else: st.info("Run fraud checks to see analytics.")
    st.divider()
    st.markdown("> **Kavach v1.0** · ET AI Hackathon 2.0 · Problem Statement 6 — AI for Digital Public Safety\n> Built by Abdul Nafisa Sulthana · EN / HI / TE / TA · Offline AI · No API key needed")
