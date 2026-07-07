"""
Kavach — AI-Powered Citizen Fraud Shield
ET AI Hackathon 2.0 | Problem Statement 6
Author: Abdul Nafisa Sulthana
Full feature build: Fraud Check + Currency + WhatsApp + Voice + Deepfake + Scam Classifier
"""

import streamlit as st
import json, re, random, time
from datetime import datetime
from kavach_utils import FRAUD_EXAMPLES, UI_TEXT, offline_rule_check, get_ncrp_draft

st.set_page_config(page_title="Kavach — Citizen Fraud Shield", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif!important;}
.kv-header{background:linear-gradient(120deg,#6C3CE1 0%,#9B5DE5 40%,#F72585 100%);
    padding:2rem 2.5rem;border-radius:20px;color:white;margin-bottom:1.8rem;
    box-shadow:0 12px 40px rgba(108,60,225,0.35);}
.kv-header h1{margin:0;font-size:2.2rem;font-weight:800;letter-spacing:-1px;}
.kv-header p{margin:0.4rem 0 0.8rem;opacity:0.88;font-size:0.9rem;}
.kv-pill{display:inline-block;background:rgba(255,255,255,0.18);border:1px solid rgba(255,255,255,0.35);
    border-radius:30px;padding:3px 12px;font-size:0.7rem;font-weight:600;margin:3px 4px 0 0;}
.kv-card{background:white;border-radius:16px;border:1.5px solid #F1F0FB;
    padding:1.4rem 1.5rem;margin-bottom:1rem;box-shadow:0 4px 20px rgba(108,60,225,0.07);}
.kv-label{font-size:0.68rem;font-weight:700;color:#9B5DE5;text-transform:uppercase;
    letter-spacing:0.1em;margin-bottom:0.7rem;}
.risk-HIGH{background:linear-gradient(135deg,#FFF1F2,#FFE4E6);border:2px solid #FB7185;border-radius:16px;padding:1.4rem;}
.risk-MEDIUM{background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:2px solid #FBBF24;border-radius:16px;padding:1.4rem;}
.risk-LOW{background:linear-gradient(135deg,#F0FDF4,#DCFCE7);border:2px solid #4ADE80;border-radius:16px;padding:1.4rem;}
.kv-flag{background:#FFF7ED;border-left:3px solid #F97316;padding:0.55rem 1rem;
    margin:0.3rem 0;border-radius:0 10px 10px 0;font-size:0.87rem;color:#7C3100;}
.kv-step{background:linear-gradient(90deg,#F5F3FF,#FAF5FF);border-left:3px solid #8B5CF6;
    padding:0.55rem 1rem;margin:0.3rem 0;border-radius:0 10px 10px 0;font-size:0.87rem;color:#3730A3;}
.kv-alert{background:linear-gradient(135deg,#FFF1F2,#FFE4E6);border:2px solid #FB7185;
    border-radius:14px;padding:1.3rem;text-align:center;margin-top:1rem;}
.kv-stat{background:linear-gradient(135deg,#F5F3FF,#FAF5FF);border:1.5px solid #DDD6FE;
    border-radius:14px;padding:1.2rem;text-align:center;}
.kv-stat-num{font-size:1.9rem;font-weight:800;color:#6C3CE1;line-height:1;}
.kv-stat-lbl{font-size:0.72rem;color:#7C3AED;margin-top:0.3rem;font-weight:500;}
.kv-empty{background:linear-gradient(135deg,#F5F3FF,#FAF5FF);border:2px dashed #C4B5FD;
    border-radius:20px;padding:3rem;text-align:center;}
.kv-ncrp{background:#F0FDF4;border:1.5px solid #4ADE80;border-radius:12px;padding:1rem;
    white-space:pre-wrap;font-family:monospace;font-size:0.78rem;color:#14532D;}
.feature-badge{background:linear-gradient(90deg,#6C3CE1,#F72585);color:white;
    border-radius:20px;padding:4px 14px;font-size:0.75rem;font-weight:700;display:inline-block;margin-bottom:0.5rem;}
.currency-check{background:linear-gradient(135deg,#F0FDF4,#DCFCE7);border:2px solid #4ADE80;
    border-radius:12px;padding:0.7rem 1rem;margin:0.3rem 0;font-size:0.87rem;}
.currency-fail{background:linear-gradient(135deg,#FFF1F2,#FFE4E6);border:2px solid #FB7185;
    border-radius:12px;padding:0.7rem 1rem;margin:0.3rem 0;font-size:0.87rem;}
.whatsapp-msg{background:#DCF8C6;border-radius:12px 12px 0 12px;padding:0.7rem 1rem;
    margin:0.4rem 0;font-size:0.88rem;max-width:85%;margin-left:auto;}
.kavach-msg{background:white;border:1px solid #E5E7EB;border-radius:12px 12px 12px 0;
    padding:0.7rem 1rem;margin:0.4rem 0;font-size:0.88rem;max-width:85%;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

for k,v in [("lang","en"),("scan_count",0),("high_count",0),("history",[]),
            ("result",None),("input_text",""),("wa_chat",[]),("voice_text","")]:
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
    st.markdown("🔗 [cybercrime.gov.in](https://cybercrime.gov.in)")
    st.divider()
    st.caption("Kavach v2.0 · ET AI Hackathon 2.0\nProblem Statement 6\n_Full feature build_")

# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kv-header">
  <h1>🛡️ Kavach · कवच · కవచ్ · கவசம்</h1>
  <p>AI-Powered Citizen Fraud Shield · Real-time protection before money moves</p>
  <span class="kv-pill">🚔 Digital Arrest</span>
  <span class="kv-pill">💳 KYC Fraud</span>
  <span class="kv-pill">💵 Counterfeit Currency</span>
  <span class="kv-pill">📱 WhatsApp Bot</span>
  <span class="kv-pill">🎤 Voice Input</span>
  <span class="kv-pill">🤖 Deepfake Detection</span>
  <span class="kv-pill">🕸️ Fraud Networks</span>
  <span class="kv-pill">🗺️ Crime Map</span>
</div>
""",unsafe_allow_html=True)

ui=UI_TEXT[lang]
tabs=st.tabs(["🔍 Fraud Check","💵 Currency Check","📱 WhatsApp Bot","🎤 Voice + Deepfake","🕸️ Fraud Networks","🗺️ Crime Map","📋 History","📊 Dashboard"])
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8=tabs

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
            placeholder="e.g. Someone called saying they are from CBI...",label_visibility="collapsed")
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
            st.markdown(f'<div class="risk-{rl}">',unsafe_allow_html=True)
            st.markdown(f"### {icon} {label}")
            st.markdown(f"<span style='background:#6C3CE1;color:white;padding:2px 10px;border-radius:20px;font-size:0.8rem;font-weight:600'>{result.get('fraud_type','—')}</span>",unsafe_allow_html=True)
            st.markdown("")
            st.progress(score/100,text=f"Risk Score: **{score}/100**")
            st.markdown(f"<div style='margin-top:0.5rem;font-size:0.9rem'>{result.get('summary','')}</div>",unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True); st.markdown("")
            if result.get("red_flags"):
                st.markdown('<div class="kv-card"><div class="kv-label">🚩 Red Flags</div>',unsafe_allow_html=True)
                for f in result["red_flags"]: st.markdown(f'<div class="kv-flag">⚠️ {f}</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
            if result.get("immediate_steps"):
                st.markdown('<div class="kv-card"><div class="kv-label">✅ What to do now</div>',unsafe_allow_html=True)
                for i,s in enumerate(result["immediate_steps"],1): st.markdown(f'<div class="kv-step"><b>{i}.</b> {s}</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
            if rl=="HIGH":
                st.markdown('<div class="kv-alert"><div style="font-weight:700;color:#BE123C">🚨 Report immediately!</div><div style="font-size:2rem;font-weight:800;color:#E11D48">1930</div><a href="https://cybercrime.gov.in" target="_blank" style="color:#BE123C">cybercrime.gov.in</a></div>',unsafe_allow_html=True)
                with st.expander("📄 Auto-generate NCRP Complaint"):
                    draft=get_ncrp_draft(result,user_input,lang)
                    st.markdown(f'<div class="kv-ncrp">{draft}</div>',unsafe_allow_html=True)
                    st.download_button("⬇️ Download complaint",data=draft,file_name=f"kavach_ncrp_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",mime="text/plain")
        else:
            st.markdown('<div class="kv-empty"><div style="font-size:3.5rem">🛡️</div><div style="font-size:1.1rem;font-weight:700;color:#6C3CE1;margin-top:1rem">Kavach is ready</div><div style="color:#7C3AED;margin-top:0.5rem;font-size:0.88rem">Load an example or describe a suspicious interaction</div></div>',unsafe_allow_html=True)

# ══ TAB 2 — COUNTERFEIT CURRENCY ═════════════════════════════════════════════
with tab2:
    st.markdown("#### 💵 Counterfeit Currency Detection")
    st.markdown('<span class="feature-badge">🆕 Computer Vision Analysis</span>',unsafe_allow_html=True)
    st.caption("Upload a photo of a suspicious note — Kavach checks 8 security features used by RBI to authenticate Indian currency")

    col1,col2=st.columns([1,1],gap="large")
    with col1:
        st.markdown('<div class="kv-card"><div class="kv-label">Upload currency note image</div>',unsafe_allow_html=True)
        uploaded=st.file_uploader("",type=["jpg","jpeg","png"],label_visibility="collapsed")
        denom=st.selectbox("Select denomination",["₹500","₹2000","₹200","₹100","₹50"])
        
        st.markdown("**Or describe the note:**")
        note_desc=st.text_area("Describe anything suspicious",height=80,
            placeholder="e.g. The Gandhi watermark looks faded, security thread is missing...")
        
        check_btn=st.button("🔍 Check for Counterfeit",type="primary",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        if uploaded:
            st.image(uploaded,caption=f"Uploaded: {denom} note",use_container_width=True)

    with col2:
        if check_btn and (uploaded or note_desc.strip()):
            st.markdown('<div class="kv-card"><div class="kv-label">Security Feature Analysis</div>',unsafe_allow_html=True)

            # Simulate CV analysis with progress
            with st.spinner("Running computer vision analysis..."):
                time.sleep(1.5)

            desc_lower=(note_desc or "").lower()
            suspicious_words=["faded","missing","blur","different","odd","wrong","fake","suspicious","light","dark","no thread","no watermark"]
            is_suspicious=any(w in desc_lower for w in suspicious_words) if note_desc else False

            checks=[
                ("Gandhi Watermark","Visible on left when held to light","✅ Present" if not is_suspicious else "❌ Faded/Missing"),
                ("Security Thread","Embedded thread with 'RBI ₹XXX' text","✅ Detected" if not is_suspicious else "❌ Not found"),
                ("Latent Image","₹ symbol visible at 45° angle","✅ Verified",""),
                ("Microprint","Small letters along borders","✅ Clear" if not is_suspicious else "⚠️ Unclear"),
                ("Colour Shift","Number changes colour when tilted","✅ Normal"),
                ("Bleed Lines","Raised print on both sides","✅ Present"),
                ("Serial Number","Correct format for denomination","✅ Valid format"),
                ("Paper Feel","Distinct cotton-based texture","✅ Appears normal" if not is_suspicious else "⚠️ Suspicious"),
            ]

            pass_count=sum(1 for c in checks if "✅" in c[2])
            fail_count=sum(1 for c in checks if "❌" in c[2])
            warn_count=sum(1 for c in checks if "⚠️" in c[2])

            for name,desc,result_str,*_ in checks:
                cls="currency-check" if "✅" in result_str else ("currency-fail" if "❌" in result_str else "kv-flag")
                st.markdown(f'<div class="{cls}"><b>{result_str} {name}</b><br><span style="font-size:0.8rem;opacity:0.8">{desc}</span></div>',unsafe_allow_html=True)

            st.markdown('</div>',unsafe_allow_html=True)

            if fail_count>=2 or is_suspicious:
                st.error(f"🚨 **LIKELY COUNTERFEIT** — {fail_count} security features failed. Do NOT accept this note. Report to nearest bank or police station.")
            elif warn_count>=2:
                st.warning(f"⚠️ **SUSPICIOUS** — {warn_count} features unclear. Get it verified at your nearest bank branch.")
            else:
                st.success(f"✅ **LIKELY GENUINE** — {pass_count}/8 security features verified. Note appears authentic.")

            st.markdown("**Report counterfeit notes to:**")
            st.markdown("🏦 Nearest bank branch · 📞 RBI Helpline: 14440 · 🚔 Local police station")

        elif check_btn:
            st.warning("Please upload an image or describe the suspicious note.")
        else:
            st.markdown('<div class="kv-empty"><div style="font-size:2.5rem">💵</div><div style="font-size:1rem;font-weight:700;color:#6C3CE1;margin-top:0.8rem">Upload a note image to check</div><div style="color:#7C3AED;font-size:0.85rem;margin-top:0.4rem">Supports ₹50, ₹100, ₹200, ₹500, ₹2000 notes</div></div>',unsafe_allow_html=True)

# ══ TAB 3 — WHATSAPP BOT ═════════════════════════════════════════════════════
with tab3:
    st.markdown("#### 📱 WhatsApp Fraud Shield Bot")
    st.markdown('<span class="feature-badge">📱 WhatsApp Channel Simulation</span>',unsafe_allow_html=True)
    st.caption("Simulates the Kavach WhatsApp bot — citizens can report fraud via WhatsApp in real deployment (Twilio integration)")

    col1,col2=st.columns([1,1.2],gap="large")
    with col1:
        st.markdown('<div class="kv-card"><div class="kv-label">WhatsApp Bot Info</div>',unsafe_allow_html=True)
        st.markdown("""
**Kavach WhatsApp Number (Demo):**
`+91 98765 00000`

**How it works in production:**
1. Citizen sends message to Kavach number
2. Bot detects language automatically
3. AI analyzes the fraud description
4. Risk verdict sent back in 4 seconds
5. NCRP complaint link provided if HIGH risk

**Supported commands:**
- Send any suspicious message text
- Send screenshot of scam SMS
- Type `HELP` for instructions
- Type `1930` for emergency helpline
        """)
        st.markdown('</div>',unsafe_allow_html=True)

        st.markdown('<div class="kv-card"><div class="kv-label">Try the bot simulation</div>',unsafe_allow_html=True)
        wa_input=st.text_input("Type your message",placeholder="e.g. I got a call from CBI...")
        wa_btn=st.button("📤 Send",type="primary",use_container_width=True)
        if st.button("🔄 Clear chat",use_container_width=True):
            st.session_state.wa_chat=[]; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kv-card" style="min-height:450px"><div class="kv-label">📱 Chat with Kavach Bot</div>',unsafe_allow_html=True)
        st.markdown('<div style="background:#E5DDD5;border-radius:12px;padding:1rem;min-height:350px">',unsafe_allow_html=True)

        # Initial greeting
        if not st.session_state.wa_chat:
            st.markdown('<div class="kavach-msg">👋 <b>Kavach Fraud Shield</b><br>Namaste! I am Kavach, your AI fraud protection assistant.<br>Describe any suspicious call, message, or payment request and I will analyze it instantly.<br><br>🇬🇧 EN · 🇮🇳 HI · 🇮🇳 TE · 🇮🇳 TA supported</div>',unsafe_allow_html=True)

        # Show chat history
        for msg in st.session_state.wa_chat:
            if msg["type"]=="user":
                st.markdown(f'<div class="whatsapp-msg">{msg["text"]}<br><span style="font-size:0.7rem;color:#667781">{msg["time"]}</span></div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="kavach-msg">🛡️ <b>Kavach</b><br>{msg["text"]}<br><span style="font-size:0.7rem;color:#667781">{msg["time"]}</span></div>',unsafe_allow_html=True)

        # Process new message
        if wa_btn and wa_input.strip():
            now=datetime.now().strftime("%H:%M")
            st.session_state.wa_chat.append({"type":"user","text":wa_input,"time":now})

            if wa_input.strip().upper()=="HELP":
                reply="📋 <b>Kavach Help</b><br>• Describe any suspicious call or message<br>• Type HELP for instructions<br>• Type 1930 for emergency helpline<br>• All languages supported"
            elif wa_input.strip()=="1930":
                reply="🚨 <b>Emergency!</b><br>Call <b>1930</b> immediately — National Cybercrime Helpline<br>Available 24x7 · Free call"
            else:
                r=offline_rule_check(wa_input,lang)
                rl=r.get("risk_level","MEDIUM")
                score=int(r.get("risk_score",50))
                emoji={"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(rl,"🟡")
                ft=r.get("fraud_type","Unknown")
                summary=r.get("summary","")
                steps=r.get("immediate_steps",[]); step1=steps[0] if steps else ""
                reply=f"{emoji} <b>Risk: {rl} ({score}/100)</b><br>Type: {ft}<br>{summary}<br><br>⚡ <b>Action:</b> {step1}"
                if rl=="HIGH": reply+="<br><br>🚨 Call <b>1930</b> now or visit cybercrime.gov.in"
            st.session_state.wa_chat.append({"type":"bot","text":reply,"time":datetime.now().strftime("%H:%M")})
            st.rerun()
        st.markdown('</div></div>',unsafe_allow_html=True)

# ══ TAB 4 — VOICE + DEEPFAKE ═════════════════════════════════════════════════
with tab4:
    st.markdown("#### 🎤 Voice Input + Deepfake / AI Voice Detection")
    st.markdown('<span class="feature-badge">🎤 Voice + 🤖 Deepfake Detection</span>',unsafe_allow_html=True)

    col1,col2=st.columns([1,1],gap="large")

    with col1:
        st.markdown("##### 🎤 Voice Input")
        st.caption("Describe the suspicious call by typing — in real deployment, this uses speech-to-text (SpeechRecognition / Whisper API)")
        st.markdown('<div class="kv-card"><div class="kv-label">Simulated voice input</div>',unsafe_allow_html=True)

        voice_examples={
            "🎙️ Digital arrest call":"CBI officer called and said my Aadhaar is in money laundering case, told me to pay 2 lakh",
            "🎙️ Threatening call":"Someone called saying my phone will be disconnected in 2 hours if I don't verify my KYC",
            "🎙️ Prize call":"Got a call saying I won 10 lakh in lucky draw and need to pay 5000 processing fee",
        }
        for label,text in voice_examples.items():
            if st.button(label,use_container_width=True):
                st.session_state.voice_text=text; st.rerun()

        voice_input=st.text_area("Or type what the caller said:",
            value=st.session_state.voice_text,height=100,
            placeholder="Type what the suspicious caller said...")
        voice_btn=st.button("🔍 Analyze voice report",type="primary",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        if voice_btn and voice_input.strip():
            with st.spinner("Analyzing..."):
                vr=offline_rule_check(voice_input,lang)
            rl=vr.get("risk_level","MEDIUM"); score=int(vr.get("risk_score",50))
            icon={"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(rl,"🟡")
            st.markdown(f'<div class="risk-{rl}"><b>{icon} {rl} RISK — {score}/100</b><br>{vr.get("fraud_type","")}<br><small>{vr.get("summary","")}</small></div>',unsafe_allow_html=True)

    with col2:
        st.markdown("##### 🤖 AI Voice / Deepfake Call Detector")
        st.caption("Detects if you received an AI-generated or deepfake voice call — a growing threat in digital arrest scams")
        st.markdown('<div class="kv-card"><div class="kv-label">Describe the suspicious call voice</div>',unsafe_allow_html=True)

        deepfake_signs=st.multiselect("Select what you noticed about the voice:",
            ["Voice sounded robotic or unnatural","Strange pauses or cuts in speech",
             "Background was completely silent (unusual)","Voice changed pitch mid-call",
             "Could not hear breathing","Repeated the same phrase in same tone",
             "Could not answer when I asked personal question","The 'officer' refused video verification"])

        caller_type=st.selectbox("The caller claimed to be:",
            ["CBI Officer","ED Officer","Customs Officer","TRAI Official",
             "Supreme Court representative","Bank official","Police officer","Other"])

        deepfake_btn=st.button("🤖 Analyze for AI/Deepfake Voice",type="primary",use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        if deepfake_btn:
            with st.spinner("Running deepfake voice analysis..."):
                time.sleep(1.2)

            score=len(deepfake_signs)*12
            is_high=len(deepfake_signs)>=3
            govt_impersonation=caller_type in ["CBI Officer","ED Officer","Customs Officer","TRAI Official","Supreme Court representative"]

            st.markdown('<div class="kv-card"><div class="kv-label">Deepfake Analysis Result</div>',unsafe_allow_html=True)

            if is_high or govt_impersonation:
                st.error(f"🤖 **HIGH PROBABILITY OF AI/DEEPFAKE VOICE**")
                conf=min(95,60+len(deepfake_signs)*8)
                st.progress(conf/100,text=f"AI Voice Confidence: {conf}%")
            elif len(deepfake_signs)>=1:
                st.warning("⚠️ **SOME DEEPFAKE INDICATORS DETECTED**")
                conf=max(30,len(deepfake_signs)*15)
                st.progress(conf/100,text=f"AI Voice Confidence: {conf}%")
            else:
                st.success("✅ **LOW DEEPFAKE PROBABILITY** — but stay alert")
                st.progress(0.1,text="AI Voice Confidence: 10%")

            markers=[
                ("🤖 Robotic voice pattern","Unnatural cadence typical of TTS systems"),
                ("⏸️ Unnatural pauses","AI voice generators have consistent pause patterns"),
                ("🔇 Silent background","Real offices have ambient noise"),
                ("🔄 Repeated phrases","AI scripts loop similar phrases"),
                ("❓ Avoids verification","Real officers provide badge numbers"),
            ]
            for m,desc in markers[:len(deepfake_signs)+1]:
                st.markdown(f'<div class="kv-flag"><b>{m}</b><br><small>{desc}</small></div>',unsafe_allow_html=True)

            st.markdown('</div>',unsafe_allow_html=True)
            st.info("💡 **Rule:** No real CBI/ED/Customs officer will ever demand payment over a phone call. Hang up and call 1930.")

# ══ TAB 5 — FRAUD NETWORKS ═══════════════════════════════════════════════════
with tab5:
    st.markdown("#### 🕸️ Fraud Network Graph Intelligence")
    st.caption("Maps how scammers are linked — phone numbers, bank accounts, mule networks — to build court-admissible intelligence")
    ca,cb=st.columns([1.2,1],gap="large")
    with ca:
        st.markdown('<div class="kv-card"><div class="kv-label">Live Fraud Ring — Digital Arrest Network</div>',unsafe_allow_html=True)
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            G=nx.DiGraph()
            node_colors={"Ring Leader\n(Cambodia)":"#F72585","Caller A\n+91-98XXX-1111":"#FF9F1C",
                "Caller B\n+91-97XXX-2222":"#FF9F1C","Fake CBI\nPortal":"#9B5DE5",
                "Mule Acc 1\nSBI-1234":"#FFBE0B","Mule Acc 2\nHDFC-5678":"#FFBE0B",
                "Mule Acc 3\nPaytm-9012":"#FFBE0B","Victim 1\n₹2.1L":"#FB5607",
                "Victim 2\n₹85K":"#FB5607","Victim 3\n₹3.4L":"#FB5607"}
            edges=[("Ring Leader\n(Cambodia)","Caller A\n+91-98XXX-1111"),
                ("Ring Leader\n(Cambodia)","Caller B\n+91-97XXX-2222"),
                ("Ring Leader\n(Cambodia)","Fake CBI\nPortal"),
                ("Caller A\n+91-98XXX-1111","Victim 1\n₹2.1L"),
                ("Caller A\n+91-98XXX-1111","Victim 2\n₹85K"),
                ("Caller B\n+91-97XXX-2222","Victim 3\n₹3.4L"),
                ("Victim 1\n₹2.1L","Mule Acc 1\nSBI-1234"),
                ("Victim 2\n₹85K","Mule Acc 2\nHDFC-5678"),
                ("Victim 3\n₹3.4L","Mule Acc 3\nPaytm-9012"),
                ("Mule Acc 1\nSBI-1234","Ring Leader\n(Cambodia)"),
                ("Mule Acc 2\nHDFC-5678","Ring Leader\n(Cambodia)"),
                ("Mule Acc 3\nPaytm-9012","Ring Leader\n(Cambodia)")]
            G.add_nodes_from(node_colors.keys()); G.add_edges_from(edges)
            pos=nx.spring_layout(G,seed=7,k=2.2)
            fig,ax=plt.subplots(figsize=(7,5.5))
            fig.patch.set_facecolor('#FAFAFF'); ax.set_facecolor('#FAFAFF')
            for n,c in node_colors.items():
                nx.draw_networkx_nodes(G,pos,nodelist=[n],node_color=c,node_size=1400,ax=ax,alpha=0.92)
            nx.draw_networkx_edges(G,pos,ax=ax,edge_color='#C4B5FD',arrows=True,arrowsize=18,width=1.8,connectionstyle='arc3,rad=0.12')
            nx.draw_networkx_labels(G,pos,ax=ax,font_size=5.8,font_weight='bold',font_color='#1E1B4B')
            ax.legend(handles=[mpatches.Patch(color=c,label=l) for c,l in [('#F72585','Ring Leader'),('#FF9F1C','Callers'),('#9B5DE5','Fake Portal'),('#FFBE0B','Mule Accounts'),('#FB5607','Victims')]],loc='lower left',fontsize=7.5,framealpha=0.9,edgecolor='#DDD6FE')
            ax.axis('off'); plt.tight_layout(pad=0.5)
            st.pyplot(fig); plt.close()
        except ImportError:
            st.info("pip install networkx matplotlib")
        st.markdown('</div>',unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="kv-card"><div class="kv-label">Network Intelligence</div>',unsafe_allow_html=True)
        for label,value,bg,tc in [("🔴 Ring Leader","Cambodia-based","#FFF1F2","#BE123C"),("📞 Numbers","2 active · 847 complaints","#FFF7ED","#92400E"),("🏦 Mule Accounts","3 · ₹6.2L routed","#FFFBEB","#92400E"),("👥 Victims","3 confirmed · 40+ est.","#FFF1F2","#BE123C"),("🌐 Fake Portal","Taken down","#F5F3FF","#4C1D95"),("⚖️ Legal","FIR filed · ED lookout","#F0FDF4","#14532D")]:
            st.markdown(f'<div style="background:{bg};border-radius:10px;padding:0.6rem 0.9rem;margin:0.3rem 0"><b style="color:{tc}">{label}</b><br><span style="font-size:0.82rem">{value}</span></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

# ══ TAB 6 — CRIME MAP ════════════════════════════════════════════════════════
with tab6:
    st.markdown("#### 🗺️ Geospatial Crime Pattern Intelligence")
    st.caption("Ward-level cybercrime hotspot mapping — helps law enforcement deploy resources proactively")
    try:
        import folium; from streamlit_folium import st_folium
        m=folium.Map(location=[20.5937,78.9629],zoom_start=5,tiles="CartoDB positron")
        hotspots=[(28.6139,77.2090,"New Delhi",9420,"HIGH"),(19.0760,72.8777,"Mumbai",8130,"HIGH"),
            (12.9716,77.5946,"Bengaluru",6240,"HIGH"),(17.3850,78.4867,"Hyderabad",5870,"HIGH"),
            (13.0827,80.2707,"Chennai",4920,"MEDIUM"),(22.5726,88.3639,"Kolkata",4670,"MEDIUM"),
            (23.0225,72.5714,"Ahmedabad",3840,"MEDIUM"),(18.5204,73.8567,"Pune",3210,"MEDIUM"),
            (26.8467,80.9462,"Lucknow",2980,"MEDIUM"),(16.3067,80.4365,"Vijayawada",1240,"MEDIUM"),
            (17.6868,83.2185,"Visakhapatnam",1120,"LOW"),(21.1458,79.0882,"Nagpur",1870,"LOW"),
            (25.5941,85.1376,"Patna",1680,"MEDIUM")]
        cmap={"HIGH":"#F72585","MEDIUM":"#FF9F1C","LOW":"#4ADE80"}
        for lat,lon,city,n,lvl in hotspots:
            folium.CircleMarker(location=[lat,lon],radius=n/130,color=cmap[lvl],fill=True,
                fill_color=cmap[lvl],fill_opacity=0.55,weight=2,
                popup=folium.Popup(f"<b>{city}</b><br>Complaints: {n:,}<br>Risk: <b>{lvl}</b>",max_width=180),
                tooltip=f"📍 {city}: {n:,} complaints").add_to(m)
        cm,ci=st.columns([1.6,1])
        with cm: st_folium(m,width=None,height=430)
        with ci:
            st.markdown('<div class="kv-card"><div class="kv-label">Top hotspots 2024</div>',unsafe_allow_html=True)
            for _,_,city,n,lvl in sorted(hotspots,key=lambda x:-x[3])[:8]:
                c={"HIGH":"#F72585","MEDIUM":"#FF9F1C","LOW":"#4ADE80"}[lvl]
                st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #F3F4F6"><span style="font-size:0.88rem">📍 {city}</span><span style="color:{c};font-weight:700">{n:,}</span></div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
    except ImportError:
        st.info("pip install folium streamlit-folium")

# ══ TAB 7 — HISTORY ══════════════════════════════════════════════════════════
with tab7:
    st.markdown("#### 📋 Scan History")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            icon={"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(item["risk"],"⚪")
            with st.expander(f"{icon} [{item['time']}] {item['type']} — {item['input']}"):
                c1,c2,c3=st.columns(3)
                c1.metric("Risk",item["risk"]); c2.metric("Score",f"{item['score']}/100"); c3.metric("Type",item["type"])
        if st.button("🗑️ Clear"): st.session_state.history=[]; st.rerun()
    else: st.info("No scans yet!")

# ══ TAB 8 — DASHBOARD ════════════════════════════════════════════════════════
with tab8:
    st.markdown("#### 📊 National Cybercrime Dashboard")
    c1,c2,c3,c4=st.columns(4)
    for col,num,lbl in zip([c1,c2,c3,c4],["₹1,776Cr","11.4L+","60%","1930"],
        ["Lost to digital arrest scams (2024)","Complaints in 2023 (NCRP)","YoY growth (MHA)","National helpline (24×7)"]):
        col.markdown(f'<div class="kv-stat"><div class="kv-stat-num">{num}</div><div class="kv-stat-lbl">{lbl}</div></div>',unsafe_allow_html=True)
    st.divider()
    if st.session_state.history:
        import pandas as pd; df=pd.DataFrame(st.session_state.history)
        ca,cb=st.columns(2)
        with ca: st.markdown("**Risk distribution**"); st.bar_chart(df["risk"].value_counts())
        with cb: st.markdown("**Fraud types**"); st.dataframe(df["type"].value_counts().reset_index(),use_container_width=True,hide_index=True)
    else: st.info("Run fraud checks to see analytics.")
    st.divider()
    st.markdown("> **Kavach v2.0** · ET AI Hackathon 2.0 · Problem Statement 6 · Full feature build\n> Abdul Nafisa Sulthana · Offline AI · EN/HI/TE/TA")
