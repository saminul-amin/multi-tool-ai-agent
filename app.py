import os, sys, sqlite3, warnings

warnings.filterwarnings("ignore")

import streamlit as st
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

load_dotenv()
from agent import create_agent_executor

st.set_page_config(
    page_title="Bangladesh AI Agent",
    page_icon="🇧🇩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject Full Custom CSS ────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── reset streamlit chrome ───────────────────────────── */
#MainMenu,footer,header,
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"]{display:none!important}

/* ── global ───────────────────────────────────────────── */
:root{
  --bg:#0f172a;--bg2:#1e293b;--bg3:#334155;
  --text:#f1f5f9;--muted:#94a3b8;--dim:#64748b;
  --blue:#3b82f6;--green:#22c55e;
}
html,body,.stApp{
  font-family:'Inter',system-ui,sans-serif;
  background:var(--bg)!important;color:var(--text);
}
.block-container{padding-top:0!important;max-width:100%!important}
div[data-testid="stAppViewBlockContainer"]{padding-top:0!important}

/* ── sidebar ──────────────────────────────────────────── */
section[data-testid="stSidebar"]{
  background:var(--bg2)!important;
  border-right:1px solid var(--bg3)!important;width:280px!important;
}
section[data-testid="stSidebar"] *{color:var(--muted)}
section[data-testid="stSidebar"] hr{border-color:var(--bg3)!important;margin:12px 0!important}

.sb-logo{display:flex;align-items:center;gap:12px;padding:4px 0 8px;
  font-size:20px;font-weight:700;color:var(--text)}
.sb-logo .flag{font-size:28px}

.sb-section{font-size:11px;font-weight:600;text-transform:uppercase;
  letter-spacing:.8px;color:var(--dim);padding:0 0 10px}

.nav{display:flex;align-items:center;gap:12px;padding:10px 12px;
  border-radius:8px;font-size:14px;color:var(--muted);margin-bottom:2px}
.nav:hover{background:var(--bg3);color:var(--text)}
.nav.on{background:rgba(59,130,246,.15);color:var(--blue);font-weight:500}
.nav .ic{font-size:18px;width:24px;text-align:center}
.nav .badge{margin-left:auto;font-size:11px;font-weight:500;
  background:var(--bg3);padding:2px 8px;border-radius:10px;color:var(--dim)}
.nav.on .badge{background:rgba(59,130,246,.2);color:var(--blue)}

.sb-row{display:flex;justify-content:space-between;font-size:12px;padding:3px 0}
.sb-row .l{color:var(--dim)}
.sb-row .v{color:var(--muted);font-weight:500}
.sb-row .v.ok{color:var(--green)!important}

section[data-testid="stSidebar"] .stButton>button{
  background:var(--bg3)!important;border:1px solid #475569!important;
  color:var(--text)!important;border-radius:8px!important;
  font-size:13px!important;font-weight:500!important}
section[data-testid="stSidebar"] .stButton>button:hover{
  background:#475569!important;border-color:var(--dim)!important}

/* ── header bar ───────────────────────────────────────── */
.topbar{padding:16px 32px;border-bottom:1px solid var(--bg3);
  background:var(--bg2);margin:0 -1rem;padding-left:calc(1rem+32px)}
.topbar h1{font-size:18px;font-weight:600;color:var(--text);margin:0;letter-spacing:-.3px}
.topbar p{font-size:13px;color:var(--dim);margin:2px 0 0}

/* ── welcome ──────────────────────────────────────────── */
.welcome{max-width:820px;margin:42px auto 22px;text-align:center}
.welcome-card{
  position:relative;
  background:linear-gradient(145deg,rgba(30,41,59,.72),rgba(15,23,42,.78));
  border:1px solid rgba(71,85,105,.45);
  border-radius:20px;
  padding:34px 28px 26px;
  box-shadow:0 18px 45px rgba(2,6,23,.42),inset 0 1px 0 rgba(148,163,184,.07);
  backdrop-filter:blur(10px);
  overflow:hidden;
}
.welcome-card:before{
  content:"";
  position:absolute;
  width:320px;height:320px;
  background:radial-gradient(circle,rgba(59,130,246,.16),rgba(59,130,246,0) 70%);
  top:-160px;right:-120px;pointer-events:none;
}
.welcome .icon{font-size:54px;margin-bottom:12px;filter:drop-shadow(0 0 16px rgba(59,130,246,.22))}
.welcome h2{font-size:32px;font-weight:700;color:var(--text);margin-bottom:10px;letter-spacing:-.6px;line-height:1.15}
.welcome p{font-size:15px;color:var(--muted);line-height:1.75;max-width:610px;margin:0 auto 20px}
.welcome-meta{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:2px}
.welcome-chip{
  font-size:11px;font-weight:600;letter-spacing:.02em;
  color:#bfdbfe;background:rgba(30,58,138,.26);
  border:1px solid rgba(59,130,246,.28);
  border-radius:999px;padding:5px 10px;
}
.example-title{
  max-width:820px;margin:18px auto 12px;
  color:var(--muted);font-size:12px;font-weight:600;
  letter-spacing:.08em;text-transform:uppercase;
  text-align:left;padding-left:8px;
}

/* example buttons */
.ex-grid{max-width:820px;margin:0 auto}
.ex-grid .stColumn{padding:0 6px!important}
.ex-grid .stButton>button{
  position:relative!important;
  background:rgba(15,23,42,.55)!important;
  border:1px solid rgba(71,85,105,.48)!important;
  border-radius:14px!important;
  color:#e2e8f0!important;
  padding:34px 18px 14px 18px!important;
  font-size:14px!important;
  text-align:left!important;
  font-family:'Inter',sans-serif!important;
  line-height:1.6!important;
  font-weight:500!important;
  letter-spacing:-.01em!important;
  transition:transform .18s ease, border-color .18s ease, background .18s ease, box-shadow .18s ease!important;
  backdrop-filter:blur(10px)!important;
  box-shadow:0 6px 18px rgba(2,6,23,.24), inset 0 1px 0 rgba(148,163,184,.05)!important;
  overflow:hidden!important;
}
.ex-grid .stButton>button::after{
  content:"Run";
  position:absolute;
  top:10px;right:12px;
  font-size:10px;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:rgba(148,163,184,.9);
  border:1px solid rgba(71,85,105,.55);
  background:rgba(2,6,23,.22);
  padding:3px 8px;
  border-radius:999px;
}
.ex-grid .stButton>button::before{
  content:"Suggested";
  position:absolute;
  top:10px;left:14px;
  font-size:10px;
  letter-spacing:.12em;
  text-transform:uppercase;
  color:rgba(148,163,184,.92);
}
.ex-grid .stButton>button:hover{
  background:rgba(30,41,59,.62)!important;
  border-color:rgba(100,116,139,.72)!important;
  transform:translateY(-2px);
  box-shadow:0 14px 34px rgba(2,6,23,.42)!important;
}
.ex-grid .stButton>button:active{
  transform:translateY(0)!important;
  box-shadow:none!important}

/* category rail + label */
.ex-hosp .stButton>button{border-left:4px solid rgba(239,68,68,.75)!important}
.ex-inst .stButton>button{border-left:4px solid rgba(168,85,247,.8)!important}
.ex-rest .stButton>button{border-left:4px solid rgba(245,158,11,.8)!important}
.ex-web  .stButton>button{border-left:4px solid rgba(34,197,94,.8)!important}

.ex-hosp .stButton>button::before{content:"Hospitals";color:rgba(254,202,202,.92)}
.ex-inst .stButton>button::before{content:"Institutions";color:rgba(233,213,255,.92)}
.ex-rest .stButton>button::before{content:"Restaurants";color:rgba(254,243,199,.92)}
.ex-web  .stButton>button::before{content:"Web Search";color:rgba(187,247,208,.92)}

.ex-hosp .stButton>button:hover{box-shadow:0 14px 34px rgba(2,6,23,.42), 0 0 0 3px rgba(239,68,68,.10)!important}
.ex-inst .stButton>button:hover{box-shadow:0 14px 34px rgba(2,6,23,.42), 0 0 0 3px rgba(168,85,247,.10)!important}
.ex-rest .stButton>button:hover{box-shadow:0 14px 34px rgba(2,6,23,.42), 0 0 0 3px rgba(245,158,11,.10)!important}
.ex-web  .stButton>button:hover{box-shadow:0 14px 34px rgba(2,6,23,.42), 0 0 0 3px rgba(34,197,94,.10)!important}

/* ── user bubble ──────────────────────────────────────── */
.u-wrap{display:flex;justify-content:flex-end;margin-bottom:24px}
.u-msg{background:var(--blue);color:#fff;padding:12px 18px;
  border-radius:16px 16px 4px 16px;max-width:65%;font-size:14px;line-height:1.6}

/* ── agent card ───────────────────────────────────────── */
.a-wrap{display:flex;gap:14px;align-items:flex-start;margin-bottom:24px}
.a-av{width:36px;height:36px;border-radius:50%;
  background:linear-gradient(135deg,#1e40af,#3b82f6);
  display:flex;align-items:center;justify-content:center;
  font-size:18px;flex-shrink:0;margin-top:2px}
.a-body{flex:1;min-width:0}
.a-head{font-size:13px;font-weight:600;color:var(--muted);
  margin-bottom:6px;display:flex;align-items:center;gap:8px}
.a-tag{font-size:10px;font-weight:500;background:var(--bg3);
  padding:2px 7px;border-radius:4px;color:var(--dim)}
.a-text{background:var(--bg2);border:1px solid var(--bg3);
  border-radius:4px 16px 16px 16px;padding:16px 20px;
  font-size:14px;line-height:1.75;color:var(--text)}
.a-text p{margin:0 0 8px}

/* ── tool badges ──────────────────────────────────────── */
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;
  padding-top:12px;border-top:1px solid var(--bg3)}
.tb{display:inline-flex;align-items:center;gap:5px;font-size:11px;
  padding:4px 10px;border-radius:6px;font-weight:500}
.tb.inst{background:rgba(168,85,247,.12);color:#a855f7;border:1px solid rgba(168,85,247,.2)}
.tb.hosp{background:rgba(239,68,68,.12);color:#ef4444;border:1px solid rgba(239,68,68,.2)}
.tb.rest{background:rgba(245,158,11,.12);color:#f59e0b;border:1px solid rgba(245,158,11,.2)}
.tb.web{background:rgba(34,197,94,.12);color:#22c55e;border:1px solid rgba(34,197,94,.2)}

/* ── thinking dots ────────────────────────────────────── */
.thinking{display:flex;gap:14px;align-items:flex-start;margin-bottom:24px}
.dots{display:flex;gap:4px;padding:6px 0}
.dots .d{width:8px;height:8px;background:var(--dim);border-radius:50%;
  animation:bonce 1.4s ease-in-out infinite}
.dots .d:nth-child(2){animation-delay:.15s}
.dots .d:nth-child(3){animation-delay:.3s}
@keyframes bonce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-8px)}}

/* ── error ────────────────────────────────────────────── */
.err-text{background:rgba(239,68,68,.1)!important;
  border-color:rgba(239,68,68,.25)!important;color:#fca5a5!important}

/* ── chat input ───────────────────────────────────────── */
div[data-testid="stChatInput"]{max-width:800px;margin:0 auto}
div[data-testid="stChatInput"] textarea{
  background:rgba(15,23,42,.6)!important;
  border:1px solid rgba(51,65,85,.5)!important;
  border-radius:12px!important;color:var(--text)!important;
  font-family:'Inter',sans-serif!important;font-size:14px!important;
  backdrop-filter:blur(8px)!important;
  transition:border-color .2s,box-shadow .2s!important}
div[data-testid="stChatInput"] textarea::placeholder{color:var(--dim)!important}
div[data-testid="stChatInput"] textarea:focus{
  background:rgba(30,41,59,.7)!important;
  border-color:rgba(59,130,246,.4)!important;
  box-shadow:0 0 0 3px rgba(59,130,246,.1)!important}
div[data-testid="stChatInput"] button{
  background:rgba(59,130,246,.8)!important;border-radius:8px!important;
  color:#fff!important;transition:background .2s!important}
div[data-testid="stChatInput"] button:hover{background:var(--blue)!important}

/* ── expander ─────────────────────────────────────────── */
details{background:var(--bg)!important;border:1px solid var(--bg3)!important;
  border-radius:8px!important}
details summary{color:var(--muted)!important;font-size:13px!important}
details[open] summary{color:var(--text)!important}

/* ── responsive ───────────────────────────────────────── */
@media(max-width:768px){
  .welcome{margin-top:28px}
  .welcome-card{padding:28px 18px 22px}
  .welcome h2{font-size:24px}
  .example-title{padding-left:2px}
  .u-msg{max-width:85%}
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
# The custom CSS is also given by AI as I am weak in CSS sadly! :(

