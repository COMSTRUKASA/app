import streamlit as st
import json
import os
import csv
import io
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
# CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Exo+2:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif !important;
    background: #0a0a0a !important;
    color: #e8e0d5 !important;
}
.stApp { background: #0a0a0a !important; }
.block-container { padding-top: 2rem !important; max-width: 700px !important; }
section[data-testid="stSidebar"] { background: #0f0f0f !important; border-right: 1px solid #1e1e1e !important; }

@keyframes fadeUp   { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
@keyframes cardIn   { from{opacity:0;transform:translateY(12px) scale(.98)} to{opacity:1;transform:translateY(0) scale(1)} }
@keyframes slideR   { from{opacity:0;transform:translateX(-10px)} to{opacity:1;transform:translateX(0)} }
@keyframes glowPulse{ 0%,100%{text-shadow:0 0 18px rgba(255,109,0,.3)} 50%{text-shadow:0 0 38px rgba(255,109,0,.75)} }
@keyframes scanLine { from{background-position:-400px 0} to{background-position:400px 0} }
@keyframes wppFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-7px)} }
@keyframes statusDot{ 0%,100%{box-shadow:0 0 5px #4caf50} 50%{box-shadow:0 0 14px #4caf50,0 0 28px rgba(76,175,80,.3)} }
@keyframes avFloat  { 0%,100%{transform:translateY(0) rotate(0deg)} 40%{transform:translateY(-4px) rotate(-1deg)} 70%{transform:translateY(-2px) rotate(1deg)} }
@keyframes avGlow   { 0%,100%{filter:drop-shadow(0 0 4px rgba(255,109,0,.4))} 50%{filter:drop-shadow(0 0 14px rgba(255,109,0,.9))} }
@keyframes avRing   { 0%{box-shadow:0 0 0 0 rgba(255,109,0,.7)} 70%{box-shadow:0 0 0 10px rgba(255,109,0,0)} 100%{box-shadow:0 0 0 0 rgba(255,109,0,0)} }
@keyframes sairGrad { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
@keyframes sairGlow { 0%,100%{box-shadow:0 0 8px 2px rgba(239,83,80,.55)} 50%{box-shadow:0 0 22px 7px rgba(239,83,80,.95)} }

/* ── Logo ── */
.logo-wrap { text-align:center; padding:1.2rem 0 .4rem; animation:fadeUp .6s ease both; }
.logo-icon  { font-size:2.6rem; display:block; margin-bottom:.2rem; }
.logo-title {
    font-family:'Rajdhani',sans-serif; font-weight:700;
    font-size:clamp(1.8rem,6vw,2.8rem); letter-spacing:5px;
    color:#FF6D00; line-height:1; animation:glowPulse 3s ease infinite;
}
.logo-div {
    width:80px; height:2px; margin:8px auto 4px;
    background:linear-gradient(90deg,transparent,#FF6D00,transparent);
    background-size:400px 2px; animation:scanLine 2.5s ease infinite;
}
.logo-sub { font-size:.68rem; color:#444; letter-spacing:5px; text-transform:uppercase; margin-bottom:1.4rem; }

/* ── Status ── */
.status-bar {
    display:flex; align-items:center; gap:10px;
    background:rgba(46,125,50,.08); border:1px solid rgba(76,175,80,.18);
    border-radius:10px; padding:.6rem 1rem; font-size:.8rem; color:#66bb6a;
    margin-bottom:1.2rem; animation:fadeUp .6s .15s ease both;
}
.status-dot { width:7px; height:7px; background:#4caf50; border-radius:50%; flex-shrink:0; animation:statusDot 2s ease infinite; }

/* ── Login ── */
.login-box {
    background:#111; border:1px solid #1e1e1e; border-radius:20px;
    padding:2rem 2rem 1.6rem; position:relative; overflow:hidden;
    animation:cardIn .6s .1s ease both;
}
.login-box::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,#FF6D00,transparent); }
.login-title { font-family:'Rajdhani',sans-serif; font-size:1.25rem; font-weight:600; color:#e8e0d5; letter-spacing:1px; margin:0 0 1.4rem; }
.login-hint  { font-size:.73rem; color:#444; margin-top:-.6rem; margin-bottom:1rem; }

/* ── Painel header ── */
.painel-header {
    background:#0f0900; border:1px solid #2a1800; border-radius:18px;
    padding:1.4rem 1.6rem; margin-bottom:1.2rem; position:relative; overflow:hidden;
    animation:cardIn .5s ease both;
}
.painel-header::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#FF6D00,#FF8F00,#FF6D00); }
.ph-name  { font-family:'Rajdhani',sans-serif; font-size:1.3rem; font-weight:700; color:#FF8F00; letter-spacing:1px; margin:0; }
.ph-sub   { font-size:.8rem; color:#5a4020; margin:2px 0 0; }
.ph-badge { display:inline-block; background:rgba(255,109,0,.1); border:1px solid rgba(255,109,0,.25); color:#FF8F00; font-size:.7rem; font-weight:600; letter-spacing:.8px; padding:2px 10px; border-radius:20px; margin-top:6px; text-transform:uppercase; }
.ph-avatar { width:46px; height:46px; border-radius:50%; background:rgba(255,109,0,.1); border:1.5px solid rgba(255,109,0,.35); display:flex; align-items:center; justify-content:center; font-family:'Rajdhani',sans-serif; font-weight:700; font-size:1.05rem; color:#FF8F00; flex-shrink:0; animation:avGlow 3s ease infinite, avFloat 4s ease-in-out infinite, avRing 2.5s ease infinite; }

/* ── Info cards ── */
.info-card { background:#111; border:1px solid #1e1e1e; border-radius:14px; padding:1.1rem 1.3rem; margin-bottom:.7rem; position:relative; overflow:hidden; transition:border-color .25s,transform .2s; animation:cardIn .5s ease both; }
.info-card:hover { border-color:#3a1800; transform:translateY(-2px); }
.info-card::after { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(180deg,#FF6D00,#FF8F00); border-radius:3px 0 0 3px; }
.ic-label { font-size:.68rem; color:#444; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:4px; }
.ic-value { font-family:'Rajdhani',sans-serif; font-size:1.65rem; font-weight:700; color:#FF8F00; line-height:1; }
.ic-sub   { font-size:.76rem; color:#555; margin-top:4px; }

/* ── Badges ── */
.badge-ok     { background:rgba(46,125,50,.12);  color:#81c784; border:1px solid rgba(76,175,80,.2);  padding:3px 11px; border-radius:20px; font-size:.76rem; font-weight:600; }
.badge-warn   { background:rgba(230,81,0,.10);   color:#FF8F00; border:1px solid rgba(255,109,0,.2); padding:3px 11px; border-radius:20px; font-size:.76rem; font-weight:600; }
.badge-danger { background:rgba(183,28,28,.10);  color:#ef9a9a; border:1px solid rgba(229,57,53,.2); padding:3px 11px; border-radius:20px; font-size:.76rem; font-weight:600; }

/* ── Ponto rows ── */
.ponto-row { display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:1px solid #161616; animation:slideR .3s ease both; }
.ponto-row:last-child { border-bottom:none; }
.ponto-label { font-size:.86rem; color:#888; }

/* ── Próxima marcação ── */
.proxima-card { background:#0f0900; border:1px solid #2a1800; border-radius:14px; padding:1rem 1.3rem; margin-bottom:.9rem; display:flex; align-items:center; gap:12px; animation:cardIn .4s ease both; }
.prox-label { font-size:.68rem; color:#5a4020; text-transform:uppercase; letter-spacing:1px; }
.prox-value { font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:600; color:#FF8F00; }

/* ── Section title ── */
.sec-title { font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:600; color:#555; letter-spacing:2px; text-transform:uppercase; margin:1.2rem 0 .7rem; display:flex; align-items:center; gap:10px; }
.sec-title::after { content:''; flex:1; height:1px; background:#161616; }

/* ── Holerite aviso ── */
.holerite-aviso { background:rgba(255,193,7,.06); border:1px solid rgba(255,193,7,.18); border-radius:12px; padding:.85rem 1.1rem; color:#ffd54f; font-size:.86rem; margin:.7rem 0; animation:cardIn .4s ease both; }

/* ── Bloqueio ── */
.bloqueio-card { background:#111; border:1px solid #1e0a0a; border-radius:20px; padding:2.5rem 2rem; text-align:center; max-width:440px; margin:2rem auto; position:relative; overflow:hidden; animation:cardIn .6s ease both; }
.bloqueio-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,#e53935,transparent); }
.bloqueio-title { font-family:'Rajdhani',sans-serif; font-size:1.7rem; font-weight:700; color:#ef5350; letter-spacing:3px; }
.bloqueio-sub   { color:#444; font-size:.86rem; line-height:1.7; margin-top:.7rem; }
.bloqueio-hrs   { background:#161616; border-radius:10px; padding:.8rem 1rem; margin:1rem 0; font-size:.83rem; color:#666; }

/* ── WPP flutuante ── */
.wpp-float { position:fixed; bottom:22px; right:22px; z-index:9999; animation:wppFloat 3.5s ease-in-out infinite; }
.wpp-float a { background:linear-gradient(135deg,#25D366,#128C7E); color:white !important; border-radius:50px; padding:11px 20px; font-weight:600; font-size:.86rem; text-decoration:none !important; display:flex; align-items:center; gap:8px; box-shadow:0 4px 20px rgba(37,211,102,.35); }

/* ── WPP / DL btn ── */
.wpp-btn { display:inline-flex; align-items:center; gap:8px; background:linear-gradient(135deg,#25D366,#128C7E); color:white !important; padding:9px 20px; border-radius:10px; text-decoration:none !important; font-weight:600; font-size:.85rem; box-shadow:0 4px 14px rgba(37,211,102,.25); transition:all .2s; margin-top:.4rem; }

/* ── Streamlit overrides ── */
.stButton > button {
    background:linear-gradient(135deg,#E65100,#BF360C) !important;
    color:white !important; border:none !important; border-radius:10px !important;
    font-family:'Rajdhani',sans-serif !important; font-weight:600 !important;
    font-size:1rem !important; letter-spacing:1px !important;
    box-shadow:0 4px 16px rgba(230,81,0,.28) !important; transition:all .2s !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 6px 22px rgba(230,81,0,.5) !important; }
.stButton > button:active { transform:scale(.98) !important; }

/* ── Botão SAIR — força via atributo data-testid do sidebar ── */
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(270deg,#7f0000,#c62828,#ef5350,#c62828,#7f0000) !important;
    background-size: 400% 400% !important;
    animation: sairGrad 2.5s ease infinite, sairGlow 2s ease infinite !important;
    color: #fff !important;
    border: 1.5px solid rgba(255,120,120,.4) !important;
    border-radius: 14px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    letter-spacing: 4px !important;
    box-shadow: 0 4px 16px rgba(183,28,28,.5) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-3px) scale(1.04) !important;
    filter: brightness(1.2) !important;
}

div[data-baseweb="tab-list"] { background:#111 !important; border-radius:12px !important; padding:4px !important; gap:2px !important; border:1px solid #1e1e1e !important; }
div[data-baseweb="tab"] { border-radius:8px !important; font-weight:600 !important; font-size:.83rem !important; color:#555 !important; }
div[data-baseweb="tab"][aria-selected="true"] { background:#1a0e00 !important; color:#FF8F00 !important; }

input, div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { background:#161616 !important; border-color:#222 !important; color:#e8e0d5 !important; border-radius:10px !important; }
div[data-baseweb="input"]:focus-within { border-color:#FF6D00 !important; box-shadow:0 0 0 2px rgba(255,109,0,.12) !important; }
div[data-baseweb="select"] > div { background:#161616 !important; border-color:#222 !important; border-radius:10px !important; color:#e8e0d5 !important; }

div[data-testid="stExpander"] { background:#111 !important; border:1px solid #1e1e1e !important; border-radius:12px !important; margin-bottom:.4rem !important; }
div[data-testid="stExpander"]:hover { border-color:#2a1800 !important; }
div[data-testid="stExpander"] summary { color:#888 !important; font-size:.86rem !important; }

div[data-testid="stMetric"] { background:#111; border:1px solid #1e1e1e; border-radius:14px; padding:1rem 1.2rem !important; }
div[data-testid="stMetricLabel"] { color:#444 !important; font-size:.72rem !important; }
div[data-testid="stMetricValue"] { color:#FF8F00 !important; font-family:'Rajdhani',sans-serif !important; font-size:1.7rem !important; }

section[data-testid="stFileUploadDropzone"] { background:#111 !important; border:1.5px dashed #222 !important; border-radius:12px !important; }
section[data-testid="stFileUploadDropzone"]:hover { border-color:#FF6D00 !important; }

div[data-testid="stAlert"] { border-radius:12px !important; }
hr { border-color:#161616 !important; }
.stCaption, small { color:#444 !important; }
section[data-testid="stSidebar"] * { color:#888 !important; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-thumb { background:#222; border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DADOS
# ══════════════════════════════════════════════════════════
FUNCIONARIOS = {
    "admin":    {"nome":"Gustavo Steinwandt Venturini Soares","funcao":"Assistente Administrativo","senha":"admin",      "salario":650.0,"meta":0,"comissao_pct":0,"mostrar_salario":True, "mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":False,"is_admin":True},
    "karen":    {"nome":"Karen Steinwandt Venturini Soares",  "funcao":"Administradora",           "senha":"admin1",     "salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":False,"is_admin":True},
    "valdinei": {"nome":"Valdinei Rodrigues Soares",          "funcao":"Administrador",            "senha":"admin2",     "salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":False,"is_admin":True},
    "sueli":    {"nome":"Sueli",   "funcao":"Vendedora",              "senha":"maria1819","salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
    "SUELI":    {"nome":"Sueli",   "funcao":"Vendedora",              "senha":"MARIA1819","salario":0,    "meta":0,"comissao_pct":0,"mostrar_salario":False,"mostrar_meta":False,"mostrar_comissao":False,"holerite_aviso":True, "is_admin":False},
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
MESES_PT     = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}

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

def logout():
    st.session_state["logado"]  = False
    st.session_state["usuario"] = None
    st.rerun()

def render_wpp_float():
    link = f"https://wa.me/{WHATSAPP_SUPORTE}?text=Ol%C3%A1%2C%20preciso%20de%20suporte%20no%20COMSTRUKASA!"
    st.markdown(f'<div class="wpp-float"><a href="{link}" target="_blank">💬 Suporte WhatsApp</a></div>', unsafe_allow_html=True)

def render_logo():
    st.markdown("""
    <div class="logo-wrap">
        <span class="logo-icon">🏗️</span>
        <div class="logo-title">COMSTRUKASA</div>
        <div class="logo-div"></div>
        <div class="logo-sub">Materiais para Construção</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# CSV DOWNLOAD
# ══════════════════════════════════════════════════════════
def gerar_csv_mensal(dados, usuario, ano, mes):
    out = io.StringIO()
    w   = csv.writer(out)
    w.writerow(["Funcionário","Função","Data","Dia da Semana","Marcação","Hora"])
    nome   = FUNCIONARIOS[usuario]["nome"]
    funcao = FUNCIONARIOS[usuario]["funcao"]
    dias_semana = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
    prefixo = f"{ano}-{mes:02d}"
    for d in sorted(dados["pontos"].get(usuario,{}).keys()):
        if not d.startswith(prefixo): continue
        reg      = dados["pontos"][usuario][d]
        data_fmt = datetime.strptime(d,"%Y-%m-%d").strftime("%d/%m/%Y")
        dia_sem  = dias_semana[datetime.strptime(d,"%Y-%m-%d").weekday()]
        for m in MARCACOES:
            w.writerow([nome, funcao, data_fmt, dia_sem, m, reg.get(m,"–")])
    return out.getvalue().encode("utf-8-sig")

def gerar_csv_todos(dados, ano, mes):
    out = io.StringIO()
    w   = csv.writer(out)
    w.writerow(["Funcionário","Função","Data","Dia da Semana","Marcação","Hora"])
    dias_semana = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
    prefixo = f"{ano}-{mes:02d}"
    for uid, func in FUNCIONARIOS.items():
        for d in sorted(dados["pontos"].get(uid,{}).keys()):
            if not d.startswith(prefixo): continue
            reg      = dados["pontos"][uid][d]
            data_fmt = datetime.strptime(d,"%Y-%m-%d").strftime("%d/%m/%Y")
            dia_sem  = dias_semana[datetime.strptime(d,"%Y-%m-%d").weekday()]
            for m in MARCACOES:
                w.writerow([func["nome"],func["funcao"],data_fmt,dia_sem,m,reg.get(m,"–")])
    return out.getvalue().encode("utf-8-sig")

# ══════════════════════════════════════════════════════════
# BLOQUEIO
# ══════════════════════════════════════════════════════════
def tela_bloqueio():
    render_logo()
    link = f"https://wa.me/{WHATSAPP_SUPORTE}?text=Preciso+de+suporte+fora+do+hor%C3%A1rio!"
    st.markdown(f"""
    <div class="bloqueio-card">
        <div style="font-size:3.2rem;margin-bottom:.7rem;">🔒</div>
        <div class="bloqueio-title">SISTEMA ENCERRADO</div>
        <div class="bloqueio-sub">O acesso está disponível apenas durante o horário de funcionamento.</div>
        <div class="bloqueio-hrs">
            📅 <b style="color:#888;">Segunda a Sexta</b> &nbsp;—&nbsp; 07:45 até 19:00<br>
            📅 <b style="color:#888;">Sábado</b> &nbsp;—&nbsp; 07:45 até 13:00
        </div>
        <div class="bloqueio-sub">Em caso de urgência, entre em contato via WhatsApp.</div>
        <br>
        <a href="{link}" target="_blank" class="wpp-btn">💬 Falar no WhatsApp</a>
    </div>""", unsafe_allow_html=True)
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
    </div>""", unsafe_allow_html=True)

    usuario = st.text_input("Usuário", placeholder="admin, karen, sueli, wagner...")
    st.markdown('<div class="login-hint">Use seu usuário de sistema (ex: admin, karen, valdinei, sueli...)</div>', unsafe_allow_html=True)
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
# PONTO
# ══════════════════════════════════════════════════════════
def tela_ponto(usuario, dados):
    tz   = ZoneInfo("America/Sao_Paulo")
    hoje = date.today().isoformat()
    dados["pontos"].setdefault(usuario, {})
    dados["pontos"][usuario].setdefault(hoje, {})
    reg = dados["pontos"][usuario][hoje]

    st.markdown(f'<div style="font-size:.78rem;color:#444;margin-bottom:.8rem;">📅 {datetime.now(tz).strftime("%d/%m/%Y  %H:%M")}</div>', unsafe_allow_html=True)

    proxima = next((m for m in MARCACOES if m not in reg), None)

    if proxima:
        st.markdown(f"""
        <div class="proxima-card">
            <span style="font-size:1.5rem;">{EMOJIS_PONTO[proxima]}</span>
            <div>
                <div class="prox-label">Próxima marcação</div>
                <div class="prox-value">{proxima}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"⏱️  Registrar  {proxima}", use_container_width=True):
            hora_str = datetime.now(tz).strftime("%H:%M:%S")
            reg[proxima] = hora_str
            salvar_dados(dados)
            nome = FUNCIONARIOS[usuario]["nome"]
            msg  = f"📋 PONTO COMSTRUKASA\n👤 {nome}\n⏰ {proxima}: {hora_str}\n📅 {hoje}"
            st.success(f"✅ {proxima} registrada às {hora_str}!")
            st.markdown(f'<a href="{wpp_link(msg)}" target="_blank" class="wpp-btn">📲 Confirmar no WhatsApp</a>', unsafe_allow_html=True)
            st.rerun()
    else:
        st.success("✅ Todas as marcações de hoje concluídas!")

    if reg:
        st.markdown('<div class="sec-title">Registros de Hoje</div>', unsafe_allow_html=True)
        for m in MARCACOES:
            h     = reg.get(m,"–")
            badge = "badge-ok" if h != "–" else "badge-warn"
            st.markdown(f'<div class="ponto-row"><span class="ponto-label">{EMOJIS_PONTO[m]} &nbsp;{m}</span><span class="{badge}">{h}</span></div>', unsafe_allow_html=True)

    # Download mensal
    st.markdown('<div class="sec-title">Download do Ponto</div>', unsafe_allow_html=True)
    ano_atual = date.today().year
    mes_atual = date.today().month
    c1, c2 = st.columns(2)
    with c1:
        ano_sel = st.selectbox("Ano", [ano_atual-1, ano_atual, ano_atual+1], index=1, key=f"ano_{usuario}")
    with c2:
        mes_nomes = list(MESES_PT.values())
        mes_nome  = st.selectbox("Mês", mes_nomes, index=mes_atual-1, key=f"mes_{usuario}")
        mes_sel   = mes_nomes.index(mes_nome) + 1

    csv_b = gerar_csv_mensal(dados, usuario, ano_sel, mes_sel)
    st.download_button(
        label=f"📥  Baixar Planilha — {mes_nome} {ano_sel}",
        data=csv_b,
        file_name=f"ponto_{FUNCIONARIOS[usuario]['nome'].split()[0].lower()}_{ano_sel}_{mes_sel:02d}.csv",
        mime="text/csv",
        use_container_width=True
    )

    # Histórico
    hist = {d:v for d,v in dados["pontos"].get(usuario,{}).items() if d != hoje}
    if hist:
        st.markdown('<div class="sec-title">Histórico</div>', unsafe_allow_html=True)
        for d in sorted(hist.keys(), reverse=True)[:10]:
            r = hist[d]
            with st.expander(f"📅  {d}"):
                for m in MARCACOES:
                    h     = r.get(m,"–")
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
            msg = f"📁 DOCUMENTO COMSTRUKASA\n👤 {func['nome']}\n📄 {tipo}\n📝 {obs or 'Sem observação'}\n📅 {data_str}\n📎 {arq.name}"
            dados.setdefault("documentos",[]).append({"usuario":usuario,"nome":func["nome"],"tipo":tipo,"obs":obs,"arquivo":arq.name,"data":data_str})
            salvar_dados(dados)
            st.success("✅ Documento registrado!")
            st.markdown(f'<a href="{wpp_link(msg)}" target="_blank" class="wpp-btn">📲 Enviar via WhatsApp</a>', unsafe_allow_html=True)

    hist = [d for d in dados.get("documentos",[]) if d["usuario"]==usuario]
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
    </div>""", unsafe_allow_html=True)

    tem_fin = ((func["mostrar_salario"] and func["salario"]>0)
               or func["holerite_aviso"]
               or (func["mostrar_meta"] and func["meta"]>0)
               or (func["mostrar_comissao"] and func["comissao_pct"]>0))

    if tem_fin:
        tab1, tab2, tab3 = st.tabs(["📋  Livro Ponto","💰  Financeiro","📁  Documentos"])
    else:
        tab1, tab3 = st.tabs(["📋  Livro Ponto","📁  Documentos"])
        tab2 = None

    with tab1: tela_ponto(usuario, dados)

    if tab2:
        with tab2:
            st.markdown('<div class="sec-title">Informações Financeiras</div>', unsafe_allow_html=True)
            if func["mostrar_salario"] and func["salario"]>0:
                st.markdown(f'<div class="info-card"><div class="ic-label">Salário Mensal</div><div class="ic-value">{fmt_moeda(func["salario"])}</div></div>', unsafe_allow_html=True)
            elif func["holerite_aviso"]:
                st.markdown('<div class="holerite-aviso">📄 <b>Holerite:</b> Estará disponível ao fim do mês. Consulte o setor administrativo.</div>', unsafe_allow_html=True)
            if func["mostrar_meta"] and func["meta"]>0:
                st.markdown(f'<div class="info-card"><div class="ic-label">Meta Mensal</div><div class="ic-value">{fmt_moeda(func["meta"])}</div><div class="ic-sub">Atingir esta meta garante sua comissão</div></div>', unsafe_allow_html=True)
            if func["mostrar_comissao"] and func["comissao_pct"]>0:
                st.markdown(f'<div class="info-card"><div class="ic-label">Comissão acima da meta</div><div class="ic-value">{func["comissao_pct"]}%</div></div>', unsafe_allow_html=True)
                if func["meta"]>0:
                    vendas = st.number_input("Vendas no mês (R$)", min_value=0.0, step=100.0)
                    if vendas > func["meta"]:
                        st.success(f"🎉 Comissão: {fmt_moeda((vendas-func['meta'])*(func['comissao_pct']/100))}")
                    elif vendas > 0:
                        st.warning(f"⚠️ Faltam {fmt_moeda(func['meta']-vendas)} para a meta.")

    with tab3: tela_documentos(usuario, func, dados)

# ══════════════════════════════════════════════════════════
# PAINEL ADMIN
# ══════════════════════════════════════════════════════════
def painel_admin(usuario, dados):
    func = FUNCIONARIOS[usuario]
    st.markdown(f"""
    <div class="painel-header">
        <div style="display:flex;align-items:center;gap:14px;">
            <div class="ph-avatar">🛡️</div>
            <div>
                <div class="ph-name">Painel Administrativo</div>
                <div class="ph-sub">🏗️ COMSTRUKASA</div>
                <span class="ph-badge">{func['nome'].split()[0]} — Admin</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["👥  Pontos","📁  Documentos","📊  Resumo","⚙️  Meu Ponto"])

    with tab1:
        st.markdown('<div class="sec-title">Livro Ponto — Todos os Funcionários</div>', unsafe_allow_html=True)
        ano_atual = date.today().year
        mes_atual = date.today().month
        mes_nomes = list(MESES_PT.values())
        c1,c2,c3 = st.columns([1,1,1])
        with c1:
            ano_dl = st.selectbox("Ano", [ano_atual-1,ano_atual,ano_atual+1], index=1, key="adm_ano")
        with c2:
            mes_dl_nome = st.selectbox("Mês", mes_nomes, index=mes_atual-1, key="adm_mes")
            mes_dl = mes_nomes.index(mes_dl_nome)+1
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button("📥 Todos", gerar_csv_todos(dados,ano_dl,mes_dl),
                file_name=f"ponto_todos_{ano_dl}_{mes_dl:02d}.csv", mime="text/csv", use_container_width=True)
        st.divider()

        hoje = date.today().isoformat()
        for uid, func in FUNCIONARIOS.items():
            if func["is_admin"]: continue
            r_hoje = dados["pontos"].get(uid,{}).get(hoje,{})
            ult    = list(r_hoje.keys())[-1] if r_hoje else None
            badge  = "badge-ok" if "Entrada" in r_hoje else "badge-danger"
            status = f"{ult} {r_hoje[ult]}" if ult else "Sem registro hoje"
            with st.expander(f"👤  {func['nome']}  ·  {func['funcao']}"):
                st.markdown(f'<span class="{badge}">{status}</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                registros = dados["pontos"].get(uid,{})
                datas = sorted(registros.keys(), reverse=True)
                if not datas:
                    st.caption("Sem registros.")
                else:
                    for d in datas[:20]:
                        st.markdown(f'<div style="font-size:.78rem;color:#FF8F00;margin:.5rem 0 .2rem;">📅 {d}</div>', unsafe_allow_html=True)
                        r = registros[d]
                        for m in MARCACOES:
                            h = r.get(m,"–")
                            bc = "badge-ok" if h != "–" else "badge-danger"
                            st.markdown(f'<div class="ponto-row"><span class="ponto-label">{EMOJIS_PONTO[m]} &nbsp;{m}</span><span class="{bc}">{h}</span></div>', unsafe_allow_html=True)
                        st.divider()
                st.download_button(f"📥 Planilha de {func['nome'].split()[0]}",
                    gerar_csv_mensal(dados,uid,ano_dl,mes_dl),
                    file_name=f"ponto_{uid}_{ano_dl}_{mes_dl:02d}.csv",
                    mime="text/csv", key=f"dl_{uid}_{mes_dl}_{ano_dl}")

    with tab2:
        st.markdown('<div class="sec-title">Documentos Recebidos</div>', unsafe_allow_html=True)
        docs = dados.get("documentos",[])
        if not docs:
            st.info("Nenhum documento enviado ainda.")
        else:
            for d in reversed(docs):
                with st.expander(f"📄  {d['nome']}  ·  {d['tipo']}  ·  {d['data']}"):
                    st.write(f"**Arquivo:** {d['arquivo']}")
                    if d.get("obs"): st.write(f"**Obs:** {d['obs']}")
                    msg = f"📁 DOCUMENTO\n👤 {d['nome']}\n📄 {d['tipo']}\n📅 {d['data']}\n📎 {d['arquivo']}"
                    st.markdown(f'<a href="{wpp_link(msg)}" target="_blank" class="wpp-btn" style="font-size:.78rem;padding:6px 14px;">📲 Reenviar</a>', unsafe_allow_html=True)

    with tab3:
        hoje  = date.today().isoformat()
        total = len([u for u in FUNCIONARIOS if not FUNCIONARIOS[u]["is_admin"]])
        pres  = sum(1 for uid,f in FUNCIONARIOS.items() if not f["is_admin"] and "Entrada" in dados["pontos"].get(uid,{}).get(hoje,{}))
        docs  = dados.get("documentos",[])
        c1,c2,c3 = st.columns(3)
        c1.metric("👥 Funcionários", total)
        c2.metric("✅ Presentes hoje", pres)
        c3.metric("📁 Documentos", len(docs))
        st.markdown('<div class="sec-title">Situação de Hoje</div>', unsafe_allow_html=True)
        for uid,func in FUNCIONARIOS.items():
            if func["is_admin"]: continue
            r     = dados["pontos"].get(uid,{}).get(hoje,{})
            ult   = list(r.keys())[-1] if r else None
            badge = "badge-ok" if "Entrada" in r else "badge-danger"
            status = f"{ult}: {r[ult]}" if ult else "Sem registro"
            st.markdown(f'<div class="ponto-row"><span class="ponto-label">👤 {func["nome"]} <span style="color:#333;font-size:.76rem;">— {func["funcao"]}</span></span><span class="{badge}">{status}</span></div>', unsafe_allow_html=True)

    with tab4:
        tela_ponto(usuario, dados)

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
def render_sidebar(func):
    with st.sidebar:
        av       = avatar(func["nome"])
        primeiro = func["nome"].split()[0]
        admin_badge = "<div style='font-size:.68rem;color:#FF6D00 !important;margin-top:3px;letter-spacing:1px;font-weight:700;'>🛡️ ADMINISTRADOR</div>" if func["is_admin"] else ""
        st.markdown(f"""
        <div style="padding:.6rem 0 .4rem;text-align:center;">
            <div style="width:62px;height:62px;border-radius:50%;
                background:radial-gradient(circle at 35% 35%,#3a1800,#1a0900);
                border:2px solid rgba(255,109,0,.5);
                display:flex;align-items:center;justify-content:center;
                font-family:'Rajdhani',sans-serif;font-weight:700;font-size:1.3rem;color:#FF8F00;
                margin:0 auto .6rem;
                animation:avRing 2.5s ease infinite,avFloat 4s ease-in-out infinite,avGlow 3s ease infinite;
                position:relative;">
                {av}
                <div style="position:absolute;bottom:2px;right:2px;width:11px;height:11px;border-radius:50%;background:#4caf50;border:2px solid #0f0f0f;box-shadow:0 0 6px #4caf50;"></div>
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;color:#FF8F00 !important;letter-spacing:1px;">{primeiro}</div>
            <div style="font-size:.73rem;color:#555 !important;margin-top:1px;">{func['funcao']}</div>
            {admin_badge}
        </div>""", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪  S A I R", use_container_width=True, key="btn_logout"):
            logout()

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    dados = carregar_dados()
    if "logado"  not in st.session_state: st.session_state["logado"]  = False
    if "usuario" not in st.session_state: st.session_state["usuario"] = None

    if not st.session_state["logado"]:
        tela_bloqueio() if not verificar_horario() else tela_login()
        return

    usuario = st.session_state["usuario"]
    func    = FUNCIONARIOS[usuario]
    render_sidebar(func)
    render_wpp_float()
    painel_admin(usuario, dados) if func["is_admin"] else painel_funcionario(usuario, func, dados)

if __name__ == "__main__":
    main()
