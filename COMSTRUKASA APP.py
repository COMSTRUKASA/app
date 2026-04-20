import streamlit as st
import json
import os
import io
import csv
from datetime import datetime, date, time
from zoneinfo import ZoneInfo
import urllib.parse

st.set_page_config(
    page_title="COMSTRUKASA",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════
# CSS — TEMA ESCURO INDUSTRIAL PREMIUM
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background: #0a0a0a !important;
    color: #e8e0d5 !important;
}
.stApp { background: #0a0a0a !important; }
section[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid #1e1e1e !important;
}
.block-container { padding-top: 2rem !important; max-width: 700px !important; }

/* ── Animações ── */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes cardIn {
    from { opacity:0; transform:translateY(14px) scale(.98); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes slideRight {
    from { opacity:0; transform:translateX(-10px); }
    to   { opacity:1; transform:translateX(0); }
}
@keyframes glow-pulse {
    0%,100% { text-shadow: 0 0 20px rgba(255,109,0,0.3); }
    50%      { text-shadow: 0 0 40px rgba(255,109,0,0.7), 0 0 80px rgba(255,109,0,0.2); }
}
@keyframes line-scan {
    0%   { background-position:-400px 0; }
    100% { background-position:400px 0; }
}
@keyframes float-wpp {
    0%,100% { transform:translateY(0) scale(1); }
    50%      { transform:translateY(-8px) scale(1.02); }
}
@keyframes status-pulse {
    0%,100% { box-shadow:0 0 6px #4caf50; }
    50%      { box-shadow:0 0 16px #4caf50, 0 0 30px rgba(76,175,80,0.3); }
}
@keyframes logout-shine {
    0%   { background-position:-200% center; }
    100% { background-position:200% center; }
}
@keyframes bounce-in {
    0%   { transform:scale(0.85); opacity:0; }
    60%  { transform:scale(1.04); opacity:1; }
    100% { transform:scale(1); }
}

/* ── Logo ── */
.logo-wrap {
    text-align:center; padding:1.2rem 0 0.4rem;
    animation:fadeUp .6s ease both;
}
.logo-icon { font-size:2.6rem; display:block; margin-bottom:.2rem; }
.logo-title {
    font-family:'Rajdhani',sans-serif; font-weight:700;
    font-size:clamp(1.8rem,6vw,2.8rem);
    letter-spacing:5px; color:#FF6D00; text-align:center; line-height:1;
    animation:glow-pulse 3s ease infinite;
}
.logo-divider {
    width:80px; height:2px;
    background:linear-gradient(90deg,transparent,#FF6D00,transparent);
    background-size:400px 2px;
    margin:8px auto 4px;
    animation:line-scan 2.5s ease infinite;
}
.logo-sub { font-size:.68rem; color:#444; letter-spacing:5px; text-transform:uppercase; margin-bottom:1.4rem; }

/* ── Status bar ── */
.status-bar {
    display:flex; align-items:center; gap:10px;
    background:rgba(46,125,50,0.08);
    border:1px solid rgba(76,175,80,0.18);
    border-radius:10px; padding:.6rem 1rem;
    font-size:.8rem; color:#66bb6a; margin-bottom:1.2rem;
    animation:fadeUp .6s .15s ease both;
}
.status-dot {
    width:7px; height:7px; background:#4caf50; border-radius:50%;
    flex-shrink:0; animation:status-pulse 2s ease infinite;
}

/* ── Login box ── */
.login-box {
    background:#111; border:1px solid #1e1e1e;
    border-radius:20px; padding:2rem 2rem 1.6rem;
    position:relative; overflow:hidden;
    animation:cardIn .6s .1s ease both;
}
.login-box::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent 0%,#FF6D00 50%,transparent 100%);
}
.login-title {
    font-family:'Rajdhani',sans-serif; font-size:1.25rem; font-weight:600;
    color:#e8e0d5; letter-spacing:1px; margin:0 0 1.4rem;
}
.login-hint { font-size:.73rem; color:#444; margin-top:-.6rem; margin-bottom:1rem; }

/* ── Botão SAIR animado ── */
.logout-btn-wrap {
    margin-top:.8rem;
    animation:bounce-in .5s ease both;
}
.logout-btn {
    display:flex; align-items:center; justify-content:center; gap:8px;
    width:100%;
    background:linear-gradient(270deg, #c62828, #e53935, #ff5252, #e53935, #c62828);
    background-size:300% 100%;
    color:white !important; border:none; border-radius:12px;
    padding:11px 20px; font-family:'Rajdhani',sans-serif;
    font-weight:700; font-size:1rem; letter-spacing:1.5px;
    cursor:pointer; text-decoration:none;
    box-shadow:0 4px 18px rgba(229,57,53,0.35);
    transition:transform .2s, box-shadow .2s;
    animation:logout-shine 2.5s linear infinite;
}
.logout-btn:hover {
    transform:translateY(-2px) scale(1.02);
    box-shadow:0 6px 24px rgba(229,57,53,0.55);
}
.logout-btn:active { transform:scale(.97); }

/* ── Painel header ── */
.painel-header {
    background:#0f0900; border:1px solid #2a1800;
    border-radius:18px; padding:1.4rem 1.6rem;
    margin-bottom:1.2rem; position:relative; overflow:hidden;
    animation:cardIn .5s ease both;
}
.painel-header::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,#FF6D00,#FF8F00,#FF6D00);
}
.ph-name {
    font-family:'Rajdhani',sans-serif; font-size:1.3rem; font-weight:700;
    color:#FF8F00; letter-spacing:1px; margin:0;
}
.ph-sub { font-size:.8rem; color:#5a4020; margin:2px 0 0; }
.ph-badge {
    display:inline-block; background:rgba(255,109,0,0.1);
    border:1px solid rgba(255,109,0,0.25); color:#FF8F00;
    font-size:.7rem; font-weight:600; letter-spacing:.8px;
    padding:2px 10px; border-radius:20px; margin-top:6px; text-transform:uppercase;
}
.ph-avatar {
    width:46px; height:46px; border-radius:50%;
    background:rgba(255,109,0,0.1); border:1.5px solid rgba(255,109,0,0.35);
    display:flex; align-items:center; justify-content:center;
    font-family:'Rajdhani',sans-serif; font-weight:700; font-size:1.05rem;
    color:#FF8F00; flex-shrink:0;
}

/* ── Info cards ── */
.info-card {
    background:#111; border:1px solid #1e1e1e;
    border-radius:14px; padding:1.1rem 1.3rem;
    margin-bottom:.7rem; position:relative; overflow:hidden;
    transition:border-color .25s, transform .2s;
    animation:cardIn .5s ease both;
}
.info-card:hover { border-color:#3a1800; transform:translateY(-2px); }
.info-card::after {
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:linear-gradient(180deg,#FF6D00,#FF8F00); border-radius:3px 0 0 3px;
}
.ic-label { font-size:.68rem; color:#444; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:4px; }
.ic-value { font-family:'Rajdhani',sans-serif; font-size:1.65rem; font-weight:700; color:#FF8F00; line-height:1; }
.ic-sub { font-size:.76rem; color:#555; margin-top:4px; }

/* ── Badges ── */
.badge-ok     { background:rgba(46,125,50,0.12); color:#81c784; border:1px solid rgba(76,175,80,0.2);  padding:3px 11px; border-radius:20px; font-size:.76rem; font-weight:600; }
.badge-warn   { background:rgba(230,81,0,0.10);  color:#FF8F00; border:1px solid rgba(255,109,0,0.2); padding:3px 11px; border-radius:20px; font-size:.76rem; font-weight:600; }
.badge-danger { background:rgba(183,28,28,0.10); color:#ef9a9a; border:1px solid rgba(229,57,53,0.2); padding:3px 11px; border-radius:20px; font-size:.76rem; font-weight:600; }

/* ── Ponto rows ── */
.ponto-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:9px 0; border-bottom:1px solid #161616;
    animation:slideRight .3s ease both;
}
.ponto-row:last-child { border-bottom:none; }
.ponto-label { font-size:.86rem; color:#888; }

/* ── Próxima marcação ── */
.proxima-card {
    background:#0f0900; border:1px solid #2a1800;
    border-radius:14px; padding:1rem 1.3rem; margin-bottom:.9rem;
    display:flex; align-items:center; gap:12px;
    animation:cardIn .4s ease both;
}
.prox-icon { font-size:1.5rem; }
.prox-label { font-size:.68rem; color:#5a4020; text-transform:uppercase; letter-spacing:1px; }
.prox-value { font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:600; color:#FF8F00; }

/* ── Section title ── */
.sec-title {
    font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600;
    color:#555; letter-spacing:2px; text-transform:uppercase;
    margin:1.2rem 0 .7rem;
    display:flex; align-items:center; gap:10px;
}
.sec-title::after { content:''; flex:1; height:1px; background:#161616; }

/* ── Holerite aviso ── */
.holerite-aviso {
    background:rgba(255,193,7,0.06); border:1px solid rgba(255,193,7,0.18);
    border-radius:12px; padding:.85rem 1.1rem;
    color:#ffd54f; font-size:.86rem; margin:.7rem 0;
    animation:cardIn .4s ease both;
}

/* ── Bloqueio ── */
.bloqueio-card {
    background:#111; border:1px solid #1e0a0a;
    border-radius:20px; padding:2.5rem 2rem;
    text-align:center; max-width:440px; margin:2rem auto;
    position:relative; overflow:hidden;
    animation:cardIn .6s ease both;
}
.bloqueio-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent,#e53935,transparent);
}
.bloqueio-icon { font-size:3.2rem; display:block; margin-bottom:.7rem; }
.bloqueio-title { font-family:'Rajdhani',sans-serif; font-size:1.7rem; font-weight:700; color:#ef5350; letter-spacing:3px; }
.bloqueio-sub { color:#444; font-size:.86rem; line-height:1.7; margin-top:.7rem; }
.bloqueio-horarios { background:#161616; border-radius:10px; padding:.8rem 1rem; margin:1rem 0; font-size:.83rem; color:#666; }

/* ── WhatsApp flutuante ── */
.wpp-float {
    position:fixed; bottom:22px; right:22px; z-index:9999;
    animation:float-wpp 3.5s ease-in-out infinite;
}
.wpp-float a {
    background:linear-gradient(135deg,#25D366 0%,#128C7E 100%);
    color:white !important; border-radius:50px; padding:11px 20px;
    font-weight:600; font-size:.86rem; text-decoration:none !important;
    display:flex; align-items:center; gap:8px;
    box-shadow:0 4px 20px rgba(37,211,102,0.35);
    transition:transform .2s;
}
.wpp-float a:hover { transform:scale(1.06) !important; }

/* ── WPP btn link ── */
.wpp-btn {
    display:inline-flex; align-items:center; gap:8px;
    background:linear-gradient(135deg,#25D366,#128C7E);
    color:white !important; padding:9px 20px; border-radius:10px;
    text-decoration:none !important; font-weight:600; font-size:.85rem;
    box-shadow:0 4px 14px rgba(37,211,102,0.25);
    transition:all .2s; margin-top:.4rem;
}
.wpp-btn:hover { transform:translateY(-2px); box-shadow:0 6px 18px rgba(37,211,102,0.4); }

/* ── Download btn ── */
.dl-btn {
    display:inline-flex; align-items:center; gap:8px;
    background:linear-gradient(135deg,#1565C0,#0D47A1);
    color:white !important; padding:9px 20px; border-radius:10px;
    text-decoration:none !important; font-weight:600; font-size:.85rem;
    box-shadow:0 4px 14px rgba(21,101,192,0.3);
    transition:all .2s; margin-top:.4rem;
}
.dl-btn:hover { transform:translateY(-2px); }

/* ── Streamlit overrides ── */
.stButton > button {
    background:linear-gradient(135deg,#E65100,#BF360C) !important;
    color:white !important; border:none !important; border-radius:10px !important;
    font-family:'Rajdhani',sans-serif !important; font-weight:600 !important;
    font-size:1rem !important; letter-spacing:1px !important;
    box-shadow:0 4px 16px rgba(230,81,0,0.28) !important;
    transition:all .2s !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 6px 22px rgba(230,81,0,0.5) !important; }
.stButton > button:active { transform:scale(.98) !important; }

section[data-testid="stSidebar"] .stButton > button {
    background:#161616 !important; border:1px solid #2a2a2a !important;
    color:#666 !important; box-shadow:none !important;
}

div[data-baseweb="tab-list"] {
    background:#111 !important; border-radius:12px !important;
    padding:4px !important; gap:2px !important; border:1px solid #1e1e1e !important;
}
div[data-baseweb="tab"] { border-radius:8px !important; font-weight:600 !important; font-size:.83rem !important; color:#555 !important; transition:all .2s !important; }
div[data-baseweb="tab"][aria-selected="true"] { background:#1a0e00 !important; color:#FF8F00 !important; }

input, textarea, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
    background:#161616 !important; border-color:#222 !important;
    color:#e8e0d5 !important; border-radius:10px !important;
    transition:border-color .2s, box-shadow .2s !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
    border-color:#FF6D00 !important; box-shadow:0 0 0 2px rgba(255,109,0,0.12) !important;
}
div[data-baseweb="select"] > div { background:#161616 !important; border-color:#222 !important; border-radius:10px !important; color:#e8e0d5 !important; }

div[data-testid="stExpander"] { background:#111 !important; border:1px solid #1e1e1e !important; border-radius:12px !important; margin-bottom:.4rem !important; transition:border-color .2s !important; }
div[data-testid="stExpander"]:hover { border-color:#2a1800 !important; }
div[data-testid="stExpander"] summary { color:#888 !important; font-size:.86rem !important; }

div[data-testid="stMetric"] { background:#111; border:1px solid #1e1e1e; border-radius:14px; padding:1rem 1.2rem !important; animation:cardIn .5s ease both; }
div[data-testid="stMetricLabel"] { color:#444 !important; font-size:.72rem !important; }
div[data-testid="stMetricValue"] { color:#FF8F00 !important; font-family:'Rajdhani',sans-serif !important; font-size:1.7rem !important; }

section[data-testid="stFileUploadDropzone"] { background:#111 !important; border:1.5px dashed #222 !important; border-radius:12px !important; transition:border-color .2s !important; }
section[data-testid="stFileUploadDropzone"]:hover { border-color:#FF6D00 !important; }

div[data-testid="stAlert"] { border-radius:12px !important; animation:cardIn .3s ease both; }
hr { border-color:#161616 !important; }
.stCaption, small { color:#444 !important; }
section[data-testid="stSidebar"] * { color:#888 !important; }
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:#0a0a0a; }
::-webkit-scrollbar-thumb { background:#222; border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:#3a1800; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DADOS
# ══════════════════════════════════════════════════════════
FUNCIONARIOS = {
    # ── ADMINS ──
    "admin": {
        "nome":"Gustavo Steinwandt Venturini Soares","funcao":"Assistente Administrativo",
        "senha":"admin","salario":650.0,"meta":0,"comissao_pct":0,
        "mostrar_salario":True,"mostrar_meta":False,"mostrar_comissao":False,
        "holerite_aviso":False,"is_admin":True
    },
    "karen": {
        "nome":"Karen Steinwandt Venturini Soares","funcao":"Administradora",
        "senha":"admin1","salario":0,"meta":0,"comissao_pct":0,
        "mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,
        "holerite_aviso":False,"is_admin":True
    },
    "valdinei": {
        "nome":"Valdinei Rodrigues Soares","funcao":"Administrador",
        "senha":"admin2","salario":0,"meta":0,"comissao_pct":0,
        "mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,
        "holerite_aviso":False,"is_admin":True
    },
    # ── FUNCIONÁRIOS ──
    "sueli":    {"nome":"Sueli",   "funcao":"Vendedora",              "senha":"maria1819","salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
    "leiliane": {"nome":"Leiliane","funcao":"Vendedora",              "senha":"camila",   "salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
    "riquele":  {"nome":"Riquele", "funcao":"Zeladora",               "senha":"riquele24","salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
    "wagner":   {"nome":"Wagner",  "funcao":"Assistente Administrativo","senha":"wagner007","salario":650.0,"meta":0,"comissao_pct":0,"mostrar_salario":True, "mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":False,"is_admin":False},
    "agnaldo":  {"nome":"Agnaldo", "funcao":"Auxiliar de Produção",   "senha":"99551264", "salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
    "rogerio":  {"nome":"Rogério", "funcao":"Motorista",              "senha":"290580",   "salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
    "samuel":   {"nome":"Samuel",  "funcao":"Serrador",               "senha":"Sophia2710","salario":0,   "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
}

WHATSAPP_NUMERO  = "5541999013074"
WHATSAPP_SUPORTE = "5541999013074"
DATA_FILE = "comstrukasa_data.json"

MARCACOES    = ["Entrada","Saída Almoço","Retorno Almoço","Saída Café","Retorno Café","Saída"]
EMOJIS_PONTO = {"Entrada":"🟢","Saída Almoço":"🍽️","Retorno Almoço":"🔄","Saída Café":"☕","Retorno Café":"🔄","Saída":"🔴"}
TIPOS_DOC    = ["Atestado Médico","Admissão","Demissão","Declaração","Comprovante","Outro"]

MESES_PT = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",
            7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}

# ══════════════════════════════════════════════════════════
# PERSISTÊNCIA
# ══════════════════════════════════════════════════════════
def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"pontos":{},"documentos":[]}

def salvar_dados(d):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

# ══════════════════════════════════════════════════════════
# HORÁRIO
# ══════════════════════════════════════════════════════════
def verificar_horario():
    tz = ZoneInfo("America/Sao_Paulo")
    agora = datetime.now(tz)
    dia, hora = agora.weekday(), agora.time()
    if 0 <= dia <= 4: return time(7,45) <= hora <= time(19,0)
    if dia == 5:      return time(7,45) <= hora <= time(13,0)
    return False

def texto_horario():
    return "Seg – Sex: 07:45 – 19:00  ·  Sáb: 07:45 – 13:00"

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def fmt_moeda(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def wpp_link(msg):
    return f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(msg)}"

def avatar(nome):
    return "".join(p[0].upper() for p in nome.split()[:2])

def render_wpp_float():
    link = f"https://wa.me/{WHATSAPP_SUPORTE}?text=Ol%C3%A1%2C%20preciso%20de%20suporte%20no%20COMSTRUKASA!"
    st.markdown(f'<div class="wpp-float"><a href="{link}" target="_blank">💬 Suporte WhatsApp</a></div>', unsafe_allow_html=True)

def render_logo():
    st.markdown("""
    <div class="logo-wrap">
        <span class="logo-icon">🏗️</span>
        <div class="logo-title">COMSTRUKASA</div>
        <div class="logo-divider"></div>
        <div class="logo-sub">Materiais para Construção</div>
    </div>
    """, unsafe_allow_html=True)

def logout():
    st.session_state["logado"]  = False
    st.session_state["usuario"] = None
    st.rerun()

# ══════════════════════════════════════════════════════════
# DOWNLOAD CSV MENSAL
# ══════════════════════════════════════════════════════════
def gerar_csv_mensal(dados, usuario, ano, mes):
    """Gera CSV com todos os registros de ponto do mês selecionado."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Funcionário","Data","Marcação","Hora"])
    nome = FUNCIONARIOS[usuario]["nome"]
    registros = dados["pontos"].get(usuario, {})
    prefixo = f"{ano}-{mes:02d}"
    for d in sorted(registros.keys()):
        if not d.startswith(prefixo):
            continue
        reg = registros[d]
        data_fmt = datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")
        for m in MARCACOES:
            h = reg.get(m, "–")
            writer.writerow([nome, data_fmt, m, h])
    return output.getvalue().encode("utf-8-sig")

def gerar_csv_todos_mensal(dados, ano, mes):
    """Gera CSV com todos os funcionários no mês."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Funcionário","Função","Data","Marcação","Hora"])
    prefixo = f"{ano}-{mes:02d}"
    for uid, func in FUNCIONARIOS.items():
        registros = dados["pontos"].get(uid, {})
        for d in sorted(registros.keys()):
            if not d.startswith(prefixo):
                continue
            reg = registros[d]
            data_fmt = datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")
            for m in MARCACOES:
                h = reg.get(m, "–")
                writer.writerow([func["nome"], func["funcao"], data_fmt, m, h])
    return output.getvalue().encode("utf-8-sig")

# ══════════════════════════════════════════════════════════
# BLOQUEIO
# ══════════════════════════════════════════════════════════
def tela_bloqueio():
    render_logo()
    link = f"https://wa.me/{WHATSAPP_SUPORTE}?text=Preciso+de+suporte+fora+do+hor%C3%A1rio!"
    st.markdown(f"""
    <div class="bloqueio-card">
        <span class="bloqueio-icon">🔒</span>
        <div class="bloqueio-title">SISTEMA ENCERRADO</div>
        <div class="bloqueio-sub">O acesso está disponível apenas durante o horário de funcionamento.</div>
        <div class="bloqueio-horarios">
            📅 <b style="color:#888;">Segunda a Sexta</b> &nbsp;—&nbsp; 07:45 até 19:00<br>
            📅 <b style="color:#888;">Sábado</b> &nbsp;—&nbsp; 07:45 até 13:00
        </div>
        <div class="bloqueio-sub">Em caso de urgência, entre em contato via WhatsApp.</div>
        <br>
        <a href="{link}" target="_blank" class="wpp-btn">💬 Falar no WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)
    render_wpp_float()

# ══════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════
def tela_login():
    render_logo()
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot"></div>
        Sistema operando normalmente &nbsp;·&nbsp; {texto_horario()}
    </div>
    <div class="login-box">
        <div class="login-title">🔐 Acesso ao Sistema</div>
    </div>
    """, unsafe_allow_html=True)

    usuario = st.text_input("Usuário", placeholder="admin, sueli, wagner, rogerio...")
    st.markdown('<div class="login-hint">Use seu usuário de sistema (ex: admin, karen, wagner, rogerio...)</div>', unsafe_allow_html=True)
    senha = st.text_input("Senha", type="password", placeholder="••••••••")

    if st.button("ENTRAR  →", use_container_width=True):
        u = usuario.lower().strip()
        if u in FUNCIONARIOS:
            if FUNCIONARIOS[u]["senha"] == senha.strip():
                st.session_state["usuario"] = u
                st.session_state["logado"]  = True
                st.rerun()
            else:
                st.error("❌ Senha incorreta.")
        else:
            st.error("❌ Usuário não encontrado. Use: admin · karen · valdinei · sueli · leiliane · riquele · wagner · agnaldo · rogerio · samuel")

    render_wpp_float()

# ══════════════════════════════════════════════════════════
# PONTO DIGITAL
# ══════════════════════════════════════════════════════════
def tela_ponto(usuario, dados):
    tz   = ZoneInfo("America/Sao_Paulo")
    hoje = date.today().isoformat()

    if usuario not in dados["pontos"]:
        dados["pontos"][usuario] = {}
    if hoje not in dados["pontos"][usuario]:
        dados["pontos"][usuario][hoje] = {}

    reg = dados["pontos"][usuario][hoje]

    st.markdown(f'<div style="font-size:.78rem;color:#444;margin-bottom:.8rem;">📅 {datetime.now(tz).strftime("%d/%m/%Y  %H:%M")}</div>', unsafe_allow_html=True)

    proxima = next((m for m in MARCACOES if m not in reg), None)

    if proxima:
        st.markdown(f"""
        <div class="proxima-card">
            <span class="prox-icon">{EMOJIS_PONTO[proxima]}</span>
            <div>
                <div class="prox-label">Próxima marcação</div>
                <div class="prox-value">{proxima}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"⏱️  Registrar  {proxima}", use_container_width=True):
            hora_str = datetime.now(tz).strftime("%H:%M:%S")
            reg[proxima] = hora_str
            dados["pontos"][usuario][hoje] = reg
            salvar_dados(dados)
            nome = FUNCIONARIOS[usuario]["nome"]
            msg  = f"📋 PONTO COMSTRUKASA\n👤 {nome}\n⏰ {proxima}: {hora_str}\n📅 {hoje}"
            st.success(f"✅ {proxima} registrada às {hora_str}!")
            st.markdown(f'<a href="{wpp_link(msg)}" target="_blank" class="wpp-btn">📲 Confirmar no WhatsApp</a>', unsafe_allow_html=True)
            st.rerun()
    else:
        st.success("✅ Todas as marcações de hoje concluídas!")

    # Registros do dia
    if reg:
        st.markdown('<div class="sec-title">Registros de Hoje</div>', unsafe_allow_html=True)
        for m in MARCACOES:
            h = reg.get(m, "–")
            badge = "badge-ok" if h != "–" else "badge-warn"
            st.markdown(f'<div class="ponto-row"><span class="ponto-label">{EMOJIS_PONTO[m]} &nbsp;{m}</span><span class="{badge}">{h}</span></div>', unsafe_allow_html=True)

    # Download mensal
    st.markdown('<div class="sec-title">Download Mensal</div>', unsafe_allow_html=True)
    ano_atual = date.today().year
    mes_atual = date.today().month
    col1, col2 = st.columns(2)
    with col1:
        ano_sel = st.selectbox("Ano", [ano_atual - 1, ano_atual, ano_atual + 1], index=1, key=f"ano_{usuario}")
    with col2:
        mes_nomes = list(MESES_PT.values())
        mes_idx   = st.selectbox("Mês", mes_nomes, index=mes_atual - 1, key=f"mes_{usuario}")
        mes_sel   = mes_nomes.index(mes_idx) + 1

    csv_bytes = gerar_csv_mensal(dados, usuario, ano_sel, mes_sel)
    st.download_button(
        label=f"⬇️  Baixar Ponto — {mes_idx} {ano_sel}",
        data=csv_bytes,
        file_name=f"ponto_{FUNCIONARIOS[usuario]['nome'].split()[0].lower()}_{ano_sel}_{mes_sel:02d}.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Histórico
    hist = {d: v for d, v in dados["pontos"].get(usuario, {}).items() if d != hoje}
    if hist:
        st.markdown('<div class="sec-title">Histórico</div>', unsafe_allow_html=True)
        for d in sorted(hist.keys(), reverse=True)[:10]:
            r = hist[d]
            with st.expander(f"📅  {d}"):
                for m in MARCACOES:
                    h = r.get(m, "–")
                    badge = "badge-ok" if h != "–" else "badge-danger"
                    st.markdown(f'<div class="ponto-row"><span class="ponto-label">{EMOJIS_PONTO[m]} &nbsp;{m}</span><span class="{badge}">{h}</span></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DOCUMENTOS
# ══════════════════════════════════════════════════════════
def tela_documentos(usuario, func, dados):
    st.markdown('<div class="sec-title">Enviar Documento</div>', unsafe_allow_html=True)
    st.caption("Atestados, admissão, demissão, declarações e outros.")
    tipo = st.selectbox("Tipo", TIPOS_DOC)
    obs  = st.text_area("Observação (opcional)", placeholder="Descreva o documento...")
    arq  = st.file_uploader("Anexar arquivo (PNG ou PDF)", type=["png","pdf"])

    if st.button("📤  Enviar Documento", use_container_width=True):
        if arq is None:
            st.warning("⚠️ Selecione um arquivo antes de enviar.")
        else:
            data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            msg = (f"📁 DOCUMENTO COMSTRUKASA\n👤 {func['nome']}\n📄 {tipo}\n"
                   f"📝 {obs or 'Sem observação'}\n📅 {data_str}\n📎 {arq.name}")
            if "documentos" not in dados:
                dados["documentos"] = []
            dados["documentos"].append({
                "usuario": usuario, "nome": func["nome"],
                "tipo": tipo, "obs": obs, "arquivo": arq.name, "data": data_str
            })
            salvar_dados(dados)
            st.success("✅ Documento registrado!")
            st.markdown(f'<a href="{wpp_link(msg)}" target="_blank" class="wpp-btn">📲 Enviar via WhatsApp</a>', unsafe_allow_html=True)

    hist = [d for d in dados.get("documentos", []) if d["usuario"] == usuario]
    if hist:
        st.markdown('<div class="sec-title">Histórico de Envios</div>', unsafe_allow_html=True)
        for d in reversed(hist[-10:]):
            with st.expander(f"📄  {d['tipo']}  ·  {d['data']}"):
                st.write(f"**Arquivo:** {d['arquivo']}")
                if d.get("obs"): st.write(f"**Obs:** {d['obs']}")

# ══════════════════════════════════════════════════════════
# PAINEL FUNCIONÁRIO
# ══════════════════════════════════════════════════════════
def painel_funcionario(usuario, func, dados):
    av = avatar(func["nome"])
    st.markdown(f"""
    <div class="painel-header">
        <div style="display:flex;align-items:center;gap:14px;">
            <div class="ph-avatar">{av}</div>
            <div>
                <div class="ph-name">{func['nome']}</div>
                <div class="ph-sub">🏗️ COMSTRUKASA</div>
                <span class="ph-badge">{func['funcao']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Decide se mostra aba financeira
    tem_financeiro = (
        (func["mostrar_salario"] and func["salario"] > 0)
        or func["holerite_aviso"]
        or (func["mostrar_meta"] and func["meta"] > 0)
        or (func["mostrar_comissao"] and func["comissao_pct"] > 0)
    )

    if tem_financeiro:
        tab1, tab2, tab3 = st.tabs(["📋  Livro Ponto", "💰  Financeiro", "📁  Documentos"])
        tabs = [tab1, tab2, tab3]
    else:
        tab1, tab3 = st.tabs(["📋  Livro Ponto", "📁  Documentos"])
        tabs = [tab1, None, tab3]

    with tabs[0]:
        tela_ponto(usuario, dados)

    if tabs[1]:
        with tabs[1]:
            st.markdown('<div class="sec-title">Informações Financeiras</div>', unsafe_allow_html=True)

            if func["mostrar_salario"] and func["salario"] > 0:
                st.markdown(f"""
                <div class="info-card">
                    <div class="ic-label">Salário Mensal</div>
                    <div class="ic-value">{fmt_moeda(func['salario'])}</div>
                </div>""", unsafe_allow_html=True)
            elif func["holerite_aviso"]:
                st.markdown('<div class="holerite-aviso">📄 <b>Holerite:</b> Estará disponível ao fim do mês. Consulte o setor administrativo.</div>', unsafe_allow_html=True)

            if func["mostrar_meta"] and func["meta"] > 0:
                st.markdown(f"""
                <div class="info-card">
                    <div class="ic-label">Meta Mensal</div>
                    <div class="ic-value">{fmt_moeda(func['meta'])}</div>
                    <div class="ic-sub">Atingir esta meta garante sua comissão</div>
                </div>""", unsafe_allow_html=True)

            if func["mostrar_comissao"] and func["comissao_pct"] > 0:
                st.markdown(f"""
                <div class="info-card">
                    <div class="ic-label">Comissão sobre vendas acima da meta</div>
                    <div class="ic-value">{func['comissao_pct']}%</div>
                </div>""", unsafe_allow_html=True)
                if func["meta"] > 0:
                    st.markdown('<div class="sec-title">Simulador de Comissão</div>', unsafe_allow_html=True)
                    vendas = st.number_input("Vendas no mês (R$)", min_value=0.0, step=100.0)
                    if vendas > func["meta"]:
                        comissao = (vendas - func["meta"]) * (func["comissao_pct"] / 100)
                        st.success(f"🎉 Comissão estimada: {fmt_moeda(comissao)}")
                    elif vendas > 0:
                        st.warning(f"⚠️ Faltam {fmt_moeda(func['meta'] - vendas)} para a meta.")

    with tabs[2]:
        tela_documentos(usuario, func, dados)

# ══════════════════════════════════════════════════════════
# PAINEL ADMIN
# ══════════════════════════════════════════════════════════
def painel_admin(usuario, dados):
    func = FUNCIONARIOS[usuario]
    av   = avatar(func["nome"])
    st.markdown(f"""
    <div class="painel-header">
        <div style="display:flex;align-items:center;gap:14px;">
            <div class="ph-avatar" style="font-size:1.3rem;">🛡️</div>
            <div>
                <div class="ph-name">Painel Administrativo</div>
                <div class="ph-sub">🏗️ COMSTRUKASA</div>
                <span class="ph-badge">{func['nome'].split()[0]} — Admin</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["👥  Pontos", "📁  Documentos", "📊  Resumo", "⚙️  Meu Ponto"])

    # ── Pontos de todos ──
    with tab1:
        st.markdown('<div class="sec-title">Livro Ponto — Todos os Funcionários</div>', unsafe_allow_html=True)

        # Download geral
        ano_atual = date.today().year
        mes_atual = date.today().month
        mes_nomes = list(MESES_PT.values())
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            ano_dl = st.selectbox("Ano", [ano_atual-1, ano_atual, ano_atual+1], index=1, key="adm_ano")
        with col2:
            mes_dl_nome = st.selectbox("Mês", mes_nomes, index=mes_atual-1, key="adm_mes")
            mes_dl = mes_nomes.index(mes_dl_nome) + 1
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            csv_todos = gerar_csv_todos_mensal(dados, ano_dl, mes_dl)
            st.download_button(
                label=f"⬇️ Baixar Todos",
                data=csv_todos,
                file_name=f"ponto_todos_{ano_dl}_{mes_dl:02d}.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.divider()

        hoje = date.today().isoformat()
        for uid, func in FUNCIONARIOS.items():
            if func["is_admin"]: continue
            reg_hoje = dados["pontos"].get(uid, {}).get(hoje, {})
            ult = list(reg_hoje.keys())[-1] if reg_hoje else None
            badge = "badge-ok" if "Entrada" in reg_hoje else "badge-danger"
            status = f"{ult} {reg_hoje[ult]}" if ult else "Sem registro hoje"

            with st.expander(f"👤  {func['nome']}  ·  {func['funcao']}"):
                # Mini status hoje
                st.markdown(f'<span class="{badge}">{status}</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                registros = dados["pontos"].get(uid, {})
                datas = sorted(registros.keys(), reverse=True)
                if not datas:
                    st.caption("Sem registros.")
                else:
                    for d in datas[:20]:
                        st.markdown(f'<div style="font-size:.78rem;color:#FF8F00;margin:.5rem 0 .2rem;">📅 {d}</div>', unsafe_allow_html=True)
                        r = registros[d]
                        for m in MARCACOES:
                            h = r.get(m, "–")
                            bclass = "badge-ok" if h != "–" else "badge-danger"
                            st.markdown(f'<div class="ponto-row"><span class="ponto-label">{EMOJIS_PONTO[m]} &nbsp;{m}</span><span class="{bclass}">{h}</span></div>', unsafe_allow_html=True)
                        st.divider()

                # Download individual
                csv_ind = gerar_csv_mensal(dados, uid, ano_dl, mes_dl)
                st.download_button(
                    label=f"⬇️ Ponto de {func['nome'].split()[0]} — {mes_dl_nome}",
                    data=csv_ind,
                    file_name=f"ponto_{uid}_{ano_dl}_{mes_dl:02d}.csv",
                    mime="text/csv",
                    key=f"dl_{uid}_{ano_dl}_{mes_dl}"
                )

    # ── Documentos ──
    with tab2:
        st.markdown('<div class="sec-title">Documentos Recebidos</div>', unsafe_allow_html=True)
        docs = dados.get("documentos", [])
        if not docs:
            st.info("Nenhum documento enviado ainda.")
        else:
            for d in reversed(docs):
                with st.expander(f"📄  {d['nome']}  ·  {d['tipo']}  ·  {d['data']}"):
                    st.write(f"**Arquivo:** {d['arquivo']}")
                    if d.get("obs"): st.write(f"**Obs:** {d['obs']}")
                    msg = f"📁 DOCUMENTO\n👤 {d['nome']}\n📄 {d['tipo']}\n📅 {d['data']}\n📎 {d['arquivo']}"
                    st.markdown(f'<a href="{wpp_link(msg)}" target="_blank" class="wpp-btn" style="font-size:.78rem;padding:6px 14px;">📲 Reenviar</a>', unsafe_allow_html=True)

    # ── Resumo ──
    with tab3:
        hoje  = date.today().isoformat()
        total = len([u for u in FUNCIONARIOS if not FUNCIONARIOS[u]["is_admin"]])
        pres  = sum(1 for uid, f in FUNCIONARIOS.items()
                    if not f["is_admin"] and "Entrada" in dados["pontos"].get(uid, {}).get(hoje, {}))
        docs  = dados.get("documentos", [])

        c1, c2, c3 = st.columns(3)
        c1.metric("👥 Funcionários",   total)
        c2.metric("✅ Presentes hoje", pres)
        c3.metric("📁 Documentos",     len(docs))

        st.markdown('<div class="sec-title">Situação de Hoje</div>', unsafe_allow_html=True)
        for uid, func in FUNCIONARIOS.items():
            if func["is_admin"]: continue
            r     = dados["pontos"].get(uid, {}).get(hoje, {})
            ult   = list(r.keys())[-1] if r else None
            badge = "badge-ok" if "Entrada" in r else "badge-danger"
            status = f"{ult}: {r[ult]}" if ult else "Sem registro"
            st.markdown(
                f'<div class="ponto-row">'
                f'<span class="ponto-label">👤 {func["nome"]} '
                f'<span style="color:#333;font-size:.76rem;"> — {func["funcao"]}</span></span>'
                f'<span class="{badge}">{status}</span></div>',
                unsafe_allow_html=True
            )

    # ── Meu ponto ──
    with tab4:
        st.markdown('<div class="sec-title">Meu Livro Ponto</div>', unsafe_allow_html=True)
        tela_ponto(usuario, dados)

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
def render_sidebar(func, usuario):
    with st.sidebar:
        av = avatar(func["nome"])
        primeiro = func["nome"].split()[0]
        st.markdown(f"""
        <div style="padding:.4rem 0 .2rem;">
            <div style="width:44px;height:44px;border-radius:50%;
                background:rgba(255,109,0,0.1);
                border:1.5px solid rgba(255,109,0,0.28);
                display:flex;align-items:center;justify-content:center;
                font-family:'Rajdhani',sans-serif;font-weight:700;
                font-size:1rem;color:#FF8F00;margin-bottom:.5rem;">{av}</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.05rem;
                font-weight:600;color:#FF8F00 !important;letter-spacing:.8px;">{primeiro}</div>
            <div style="font-size:.75rem;color:#444 !important;">{func['funcao']}</div>
            {"<div style='font-size:.68rem;color:#c62828 !important;margin-top:2px;'>🛡️ ADMIN</div>" if func['is_admin'] else ""}
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # Botão SAIR animado
        st.markdown("""
        <div class="logout-btn-wrap">
            <style>
            div[data-testid="stSidebar"] .stButton.logout-trigger > button {
                background: linear-gradient(270deg, #c62828, #e53935, #ff5252, #e53935, #c62828) !important;
                background-size: 300% 100% !important;
                animation: logout-shine 2.5s linear infinite !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                font-family: 'Rajdhani', sans-serif !important;
                font-weight: 700 !important;
                font-size: .95rem !important;
                letter-spacing: 2px !important;
                box-shadow: 0 4px 18px rgba(229,57,53,0.4) !important;
                transition: transform .2s, box-shadow .2s !important;
            }
            div[data-testid="stSidebar"] .stButton.logout-trigger > button:hover {
                transform: translateY(-2px) scale(1.03) !important;
                box-shadow: 0 6px 24px rgba(229,57,53,0.6) !important;
            }
            </style>
        </div>
        """, unsafe_allow_html=True)

        col = st.container()
        with col:
            st.markdown('<div class="logout-trigger">', unsafe_allow_html=True)
            if st.button("🚪  SAIR", use_container_width=True, key="btn_logout"):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    dados = carregar_dados()

    if "logado"  not in st.session_state: st.session_state["logado"]  = False
    if "usuario" not in st.session_state: st.session_state["usuario"] = None

    if not st.session_state["logado"]:
        if not verificar_horario():
            tela_bloqueio()
        else:
            tela_login()
        return

    usuario = st.session_state["usuario"]
    func    = FUNCIONARIOS[usuario]

    render_sidebar(func, usuario)
    render_wpp_float()

    if func["is_admin"]:
        painel_admin(usuario, dados)
    else:
        painel_funcionario(usuario, func, dados)

if __name__ == "__main__":
    main()
