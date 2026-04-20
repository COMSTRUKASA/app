import streamlit as st
import json
import os
from datetime import datetime, date, time
import pytz
import urllib.parse

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="COMSTRUKASA",
    page_icon="🏗️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

/* Remove padding padrão */
.block-container { padding-top: 1rem !important; }

/* Logo principal */
.logo-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    color: #E65100;
    letter-spacing: 2px;
    text-align: center;
    line-height: 1;
}
.logo-sub {
    font-size: 0.85rem;
    color: #888;
    text-align: center;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* Card de login */
.login-card {
    background: #fff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.10);
    max-width: 400px;
    margin: 0 auto;
}

/* Botão WhatsApp flutuante */
.wpp-float {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 9999;
    animation: float 2.5s ease-in-out infinite;
}
.wpp-float a {
    background: #25D366;
    color: white !important;
    border-radius: 50px;
    padding: 12px 20px;
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none !important;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 4px 18px rgba(37,211,102,0.5);
}
@keyframes float {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

/* Aviso de período encerrado */
.bloqueio-card {
    background: #fff3f3;
    border: 2px solid #e53935;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    max-width: 420px;
    margin: 2rem auto;
}
.bloqueio-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #c62828;
}
.bloqueio-sub { color: #666; margin-top: .5rem; }

/* Cabeçalho do painel */
.painel-header {
    background: linear-gradient(135deg, #E65100 0%, #BF360C 100%);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    color: white;
    margin-bottom: 1rem;
}
.painel-header h2 { color: white; margin: 0; font-size: 1.3rem; }
.painel-header p  { color: rgba(255,255,255,0.80); margin: 0; font-size: 0.9rem; }

/* Cards de info */
.info-card {
    background: #fff;
    border-radius: 12px;
    border: 1px solid #eee;
    padding: 1.2rem;
    margin-bottom: .8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.info-card-title { font-size: 0.78rem; color: #999; text-transform: uppercase; letter-spacing: 1px; }
.info-card-value { font-size: 1.5rem; font-weight: 700; color: #E65100; }
.info-card-sub   { font-size: 0.85rem; color: #555; }

/* Ponto badge */
.badge-ok     { background:#e8f5e9; color:#2e7d32; padding:4px 12px; border-radius:20px; font-size:.82rem; font-weight:600; }
.badge-warn   { background:#fff3e0; color:#e65100; padding:4px 12px; border-radius:20px; font-size:.82rem; font-weight:600; }
.badge-danger { background:#ffebee; color:#c62828; padding:4px 12px; border-radius:20px; font-size:.82rem; font-weight:600; }

/* Holerite aviso */
.holerite-aviso {
    background:#fff8e1;
    border-left:4px solid #ffc107;
    padding:.9rem 1.2rem;
    border-radius:0 10px 10px 0;
    color:#795548;
    font-size:.9rem;
    margin:.8rem 0;
}

/* Tabs customizadas */
div[data-baseweb="tab-list"] {
    gap: 4px;
    background: #f5f5f5;
    border-radius: 12px;
    padding: 4px;
}
div[data-baseweb="tab"] {
    border-radius: 8px !important;
    font-weight: 600;
}

/* Upload area */
.upload-hint {
    background:#f0f4ff;
    border:2px dashed #90a4f9;
    border-radius:12px;
    padding:1rem;
    text-align:center;
    color:#5c6bc0;
    font-size:.9rem;
    margin:.5rem 0;
}

/* Aviso normal */
.aviso-normal {
    background:#e8f5e9;
    border-left:4px solid #43a047;
    padding:.7rem 1rem;
    border-radius:0 8px 8px 0;
    color:#1b5e20;
    font-size:.85rem;
}

/* Scrollbar */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-thumb { background:#ccc; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DADOS DOS FUNCIONÁRIOS
# ─────────────────────────────────────────────
FUNCIONARIOS = {
    "admin": {
        "nome": "Gustavo Steinwandt Venturini Soares",
        "funcao": "Assistente Administrativo",
        "senha": "admin",
        "salario": 650.00,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": True,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": False,
        "is_admin": True
    },
    "sueli": {
        "nome": "Sueli",
        "funcao": "Vendedora",
        "senha": "maria1819",
        "salario": 0,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": False,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": True,
        "is_admin": False
    },
    "leiliane": {
        "nome": "Leiliane",
        "funcao": "Vendedora",
        "senha": "camila",
        "salario": 0,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": False,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": True,
        "is_admin": False
    },
    "riquele": {
        "nome": "Riquele",
        "funcao": "Zeladora",
        "senha": "riquele24",
        "salario": 0,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": False,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": True,
        "is_admin": False
    },
    "wagner": {
        "nome": "Wagner",
        "funcao": "Assistente Administrativo",
        "senha": "wagner007",
        "salario": 650.00,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": True,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": False,
        "is_admin": False
    },
    "agnaldo": {
        "nome": "Agnaldo",
        "funcao": "Auxiliar de Produção",
        "senha": "99551264",
        "salario": 0,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": False,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": True,
        "is_admin": False
    },
    "rogerio": {
        "nome": "Rogério",
        "funcao": "Motorista",
        "senha": "290580",
        "salario": 0,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": False,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": True,
        "is_admin": False
    },
    "samuel": {
        "nome": "Samuel",
        "funcao": "Serrador",
        "senha": "Sophia2710",
        "salario": 0,
        "meta": 0,
        "comissao_pct": 0,
        "mostrar_salario": False,
        "mostrar_meta": False,
        "mostrar_comissao": False,
        "holerite_aviso": True,
        "is_admin": False
    }
}

WHATSAPP_NUMERO = "5541999013074"
WHATSAPP_SUPORTE = "5541999013074"

# ─────────────────────────────────────────────
# ARQUIVO DE PERSISTÊNCIA (JSON simples)
# ─────────────────────────────────────────────
DATA_FILE = "comstrukasa_data.json"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"pontos": {}, "documentos": []}

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────────
# HORÁRIO DE FUNCIONAMENTO
# ─────────────────────────────────────────────
def verificar_horario():
    tz = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(tz)
    dia = agora.weekday()   # 0=seg ... 6=dom
    hora = agora.time()

    seg_sex_inicio = time(7, 45)
    seg_sex_fim    = time(19, 0)
    sab_inicio     = time(7, 45)
    sab_fim        = time(13, 0)

    if 0 <= dia <= 4:          # Seg–Sex
        return seg_sex_inicio <= hora <= seg_sex_fim
    elif dia == 5:             # Sábado
        return sab_inicio <= hora <= sab_fim
    else:                      # Domingo
        return False

def texto_horario():
    return "Segunda a Sexta: 07:45 – 19:00  |  Sábado: 07:45 – 13:00"

# ─────────────────────────────────────────────
# BOTÃO WHATSAPP FLUTUANTE
# ─────────────────────────────────────────────
def render_wpp_float():
    link = f"https://wa.me/{WHATSAPP_SUPORTE}?text=Ol%C3%A1%2C%20preciso%20de%20suporte%20no%20COMSTRUKASA!"
    st.markdown(f"""
    <div class="wpp-float">
      <a href="{link}" target="_blank">
        💬 Suporte WhatsApp
      </a>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOGO
# ─────────────────────────────────────────────
def render_logo():
    st.markdown('<div class="logo-title">🏗️ COMSTRUKASA</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub">Materiais para Construção</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TELA DE ACESSO BLOQUEADO
# ─────────────────────────────────────────────
def tela_bloqueio():
    render_logo()
    st.markdown(f"""
    <div class="bloqueio-card">
        <div style="font-size:3rem;">🔒</div>
        <div class="bloqueio-title">Sistema Encerrado</div>
        <div class="bloqueio-sub">
            Nosso horário de atendimento é:<br><br>
            <b>Segunda a Sexta:</b> 07:45 – 19:00<br>
            <b>Sábado:</b> 07:45 – 13:00<br><br>
            Fora deste período o sistema permanece bloqueado.<br>
            Em caso de urgência, entre em contato pelo WhatsApp.
        </div>
        <br>
        <a href="https://wa.me/{WHATSAPP_SUPORTE}?text=Preciso+de+suporte+fora+do+hor%C3%A1rio!" target="_blank"
           style="background:#25D366;color:white;padding:10px 22px;border-radius:30px;text-decoration:none;font-weight:700;">
           💬 Falar no WhatsApp
        </a>
    </div>
    """, unsafe_allow_html=True)
    render_wpp_float()

# ─────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────
def tela_login():
    render_logo()

    st.markdown('<div class="aviso-normal">✅ Sistema operando normalmente — ' + texto_horario() + '</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Acesso ao Sistema")

        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha   = st.text_input("Senha", type="password", placeholder="Digite sua senha")

        if st.button("Entrar →", use_container_width=True, type="primary"):
            usuario_lower = usuario.lower().strip()
            if usuario_lower in FUNCIONARIOS:
                func = FUNCIONARIOS[usuario_lower]
                if func["senha"] == senha.strip():
                    st.session_state["usuario"] = usuario_lower
                    st.session_state["logado"] = True
                    st.rerun()
                else:
                    st.error("❌ Senha incorreta.")
            else:
                st.error("❌ Usuário não encontrado.")

        st.markdown("</div>", unsafe_allow_html=True)

    render_wpp_float()

# ─────────────────────────────────────────────
# HELPER: FORMATAR MOEDA
# ─────────────────────────────────────────────
def fmt_moeda(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ─────────────────────────────────────────────
# PONTO DIGITAL
# ─────────────────────────────────────────────
MARCACOES = ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída Café", "Retorno Café", "Saída"]
EMOJIS_PONTO = {"Entrada":"🟢","Saída Almoço":"🍽️","Retorno Almoço":"🔄","Saída Café":"☕","Retorno Café":"🔄","Saída":"🔴"}

def tela_ponto(usuario, dados):
    tz = pytz.timezone("America/Sao_Paulo")
    hoje = date.today().isoformat()

    if usuario not in dados["pontos"]:
        dados["pontos"][usuario] = {}
    if hoje not in dados["pontos"][usuario]:
        dados["pontos"][usuario][hoje] = {}

    registro_hoje = dados["pontos"][usuario][hoje]

    st.markdown(f"**📅 Hoje:** {datetime.now(tz).strftime('%d/%m/%Y %H:%M')}")

    # Próxima marcação
    proxima = None
    for m in MARCACOES:
        if m not in registro_hoje:
            proxima = m
            break

    if proxima:
        st.info(f"⏳ Próxima marcação: **{proxima}**")
        if st.button(f"{EMOJIS_PONTO[proxima]} Registrar {proxima}", use_container_width=True, type="primary"):
            agora_str = datetime.now(tz).strftime("%H:%M:%S")
            registro_hoje[proxima] = agora_str
            dados["pontos"][usuario][hoje] = registro_hoje
            salvar_dados(dados)

            # Enviar notificação WPP
            nome = FUNCIONARIOS[usuario]["nome"]
            msg = f"📋 PONTO COMSTRUKASA\n👤 {nome}\n⏰ {proxima}: {agora_str}\n📅 {hoje}"
            link = f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(msg)}"
            st.success(f"✅ {proxima} registrada às {agora_str}!")
            st.markdown(f'<a href="{link}" target="_blank" style="background:#25D366;color:white;padding:8px 18px;border-radius:20px;text-decoration:none;font-weight:700;font-size:.9rem;">📲 Enviar confirmação no WhatsApp</a>', unsafe_allow_html=True)
            st.rerun()
    else:
        st.success("✅ Todas as marcações do dia foram concluídas!")

    # Tabela do dia
    if registro_hoje:
        st.markdown("#### 📋 Registros de Hoje")
        for m in MARCACOES:
            hora = registro_hoje.get(m, "–")
            badge = "badge-ok" if hora != "–" else "badge-warn"
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #eee;"><span>{EMOJIS_PONTO[m]} {m}</span><span class="{badge}">{hora}</span></div>', unsafe_allow_html=True)

    # Histórico
    st.markdown("#### 📆 Histórico de Pontos")
    historico = dados["pontos"].get(usuario, {})
    datas_ord = sorted(historico.keys(), reverse=True)
    if len(datas_ord) > 1:
        for d in datas_ord[:10]:
            if d == hoje:
                continue
            reg = historico[d]
            with st.expander(f"📅 {d}"):
                for m in MARCACOES:
                    h = reg.get(m, "–")
                    st.write(f"{EMOJIS_PONTO[m]} **{m}**: {h}")
    else:
        st.caption("Nenhum histórico anterior disponível.")

# ─────────────────────────────────────────────
# PAINEL DO FUNCIONÁRIO
# ─────────────────────────────────────────────
def painel_funcionario(usuario, func, dados):
    st.markdown(f"""
    <div class="painel-header">
        <h2>👷 Olá, {func['nome']}!</h2>
        <p>🏗️ COMSTRUKASA &nbsp;|&nbsp; {func['funcao']}</p>
    </div>
    """, unsafe_allow_html=True)

    abas = ["📋 Livro Ponto", "💰 Financeiro", "📁 Documentos"]
    tab1, tab2, tab3 = st.tabs(abas)

    with tab1:
        tela_ponto(usuario, dados)

    with tab2:
        st.markdown("### 💰 Informações Financeiras")

        # Salário
        if func["mostrar_salario"] and func["salario"] > 0:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">Salário Mensal</div>
                <div class="info-card-value">{fmt_moeda(func['salario'])}</div>
            </div>""", unsafe_allow_html=True)
        elif func["holerite_aviso"]:
            st.markdown('<div class="holerite-aviso">📄 <b>Holerite:</b> Estará disponível ao fim do mês. Consulte o setor administrativo.</div>', unsafe_allow_html=True)

        # Meta
        if func["mostrar_meta"] and func["meta"] > 0:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">Meta Mensal</div>
                <div class="info-card-value">{fmt_moeda(func['meta'])}</div>
                <div class="info-card-sub">Atingir esta meta garante sua comissão</div>
            </div>""", unsafe_allow_html=True)

        # Comissão
        if func["mostrar_comissao"] and func["comissao_pct"] > 0:
            st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">Comissão sobre vendas acima da meta</div>
                <div class="info-card-value">{func['comissao_pct']}%</div>
                <div class="info-card-sub">Calculado sobre o valor excedente à meta</div>
            </div>""", unsafe_allow_html=True)

            if func["meta"] > 0:
                st.markdown("##### 🧮 Simulador de Comissão")
                vendas = st.number_input("Suas vendas no mês (R$)", min_value=0.0, step=100.0)
                if vendas > func["meta"]:
                    excedente = vendas - func["meta"]
                    comissao  = excedente * (func["comissao_pct"] / 100)
                    st.success(f"🎉 Comissão estimada: {fmt_moeda(comissao)} ({fmt_moeda(excedente)} acima da meta)")
                elif vendas > 0:
                    falta = func["meta"] - vendas
                    st.warning(f"⚠️ Faltam {fmt_moeda(falta)} para atingir a meta.")

    with tab3:
        tela_documentos(usuario, func, dados)

# ─────────────────────────────────────────────
# DOCUMENTOS
# ─────────────────────────────────────────────
TIPOS_DOC = ["Atestado Médico", "Admissão", "Demissão", "Declaração", "Comprovante", "Outro"]

def tela_documentos(usuario, func, dados):
    st.markdown("### 📁 Envio de Documentos")
    st.caption("Envie atestados, declarações, documentos de admissão/demissão e outros.")

    tipo = st.selectbox("Tipo de documento", TIPOS_DOC)
    obs  = st.text_area("Observação (opcional)", placeholder="Descreva o documento se necessário...")
    arq  = st.file_uploader("Anexar arquivo (PNG ou PDF)", type=["png", "pdf"])

    if st.button("📤 Enviar Documento", use_container_width=True):
        if arq is None:
            st.warning("⚠️ Selecione um arquivo antes de enviar.")
        else:
            nome = func["nome"]
            data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            msg = (f"📁 DOCUMENTO COMSTRUKASA\n"
                   f"👤 Funcionário: {nome}\n"
                   f"📄 Tipo: {tipo}\n"
                   f"📝 Obs: {obs or 'Sem observação'}\n"
                   f"📅 Data: {data_str}\n"
                   f"📎 Arquivo: {arq.name}")

            link = f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(msg)}"

            # Registrar localmente
            if "documentos" not in dados:
                dados["documentos"] = []
            dados["documentos"].append({
                "usuario": usuario,
                "nome": nome,
                "tipo": tipo,
                "obs": obs,
                "arquivo": arq.name,
                "data": data_str
            })
            salvar_dados(dados)

            st.success(f"✅ Documento registrado! Clique abaixo para enviar ao WhatsApp.")
            st.markdown(f'<a href="{link}" target="_blank" style="background:#25D366;color:white;padding:10px 22px;border-radius:24px;text-decoration:none;font-weight:700;">📲 Enviar via WhatsApp</a>', unsafe_allow_html=True)

    # Histórico de documentos do funcionário
    historico_docs = [d for d in dados.get("documentos", []) if d["usuario"] == usuario]
    if historico_docs:
        st.markdown("#### 📋 Histórico de Documentos Enviados")
        for d in reversed(historico_docs[-10:]):
            with st.expander(f"📄 {d['tipo']} — {d['data']}"):
                st.write(f"**Arquivo:** {d['arquivo']}")
                if d.get("obs"):
                    st.write(f"**Obs:** {d['obs']}")

# ─────────────────────────────────────────────
# PAINEL ADMIN
# ─────────────────────────────────────────────
def painel_admin(dados):
    st.markdown("""
    <div class="painel-header">
        <h2>🛡️ Painel Administrativo</h2>
        <p>COMSTRUKASA &nbsp;|&nbsp; Gustavo Steinwandt V. Soares</p>
    </div>
    """, unsafe_allow_html=True)

    abas = ["👥 Pontos de Todos", "📁 Documentos Recebidos", "📊 Resumo", "⚙️ Meu Ponto"]
    tab1, tab2, tab3, tab4 = st.tabs(abas)

    with tab1:
        st.markdown("### 👥 Livro Ponto — Todos os Funcionários")
        hoje = date.today().isoformat()

        for uid, func in FUNCIONARIOS.items():
            if func["is_admin"]:
                continue
            with st.expander(f"👤 {func['nome']} — {func['funcao']}"):
                registros = dados["pontos"].get(uid, {})
                datas = sorted(registros.keys(), reverse=True)
                if not datas:
                    st.caption("Nenhum registro encontrado.")
                else:
                    for d in datas[:15]:
                        st.markdown(f"**📅 {d}**")
                        reg = registros[d]
                        cols = st.columns(3)
                        for i, m in enumerate(MARCACOES):
                            h = reg.get(m, "–")
                            cols[i % 3].markdown(f"<small>{EMOJIS_PONTO[m]} **{m}**</small><br>{h}", unsafe_allow_html=True)
                        st.divider()

    with tab2:
        st.markdown("### 📁 Documentos Recebidos")
        docs = dados.get("documentos", [])
        if not docs:
            st.info("Nenhum documento enviado ainda.")
        else:
            for d in reversed(docs):
                with st.expander(f"📄 {d['nome']} — {d['tipo']} — {d['data']}"):
                    st.write(f"**Arquivo:** {d['arquivo']}")
                    st.write(f"**Obs:** {d.get('obs', '—')}")
                    msg = (f"📁 DOCUMENTO\n👤 {d['nome']}\n📄 {d['tipo']}\n"
                           f"📅 {d['data']}\n📎 {d['arquivo']}")
                    link = f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{link}" target="_blank" style="color:#25D366;font-weight:600;font-size:.85rem;">📲 Reenviar no WhatsApp</a>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### 📊 Resumo da Equipe")
        total = len([u for u in FUNCIONARIOS if not FUNCIONARIOS[u]["is_admin"]])
        hoje = date.today().isoformat()
        presentes = 0
        for uid, func in FUNCIONARIOS.items():
            if func["is_admin"]:
                continue
            reg = dados["pontos"].get(uid, {}).get(hoje, {})
            if "Entrada" in reg:
                presentes += 1

        c1, c2, c3 = st.columns(3)
        c1.metric("👥 Total de Funcionários", total)
        c2.metric("✅ Com entrada hoje", presentes)
        c3.metric("📁 Documentos totais", len(dados.get("documentos", [])))

        st.markdown("#### 👤 Situação de Hoje")
        for uid, func in FUNCIONARIOS.items():
            if func["is_admin"]:
                continue
            reg = dados["pontos"].get(uid, {}).get(hoje, {})
            ultima = list(reg.keys())[-1] if reg else None
            hora   = reg.get(ultima, "–") if ultima else "–"
            badge  = "badge-ok" if "Entrada" in reg else "badge-danger"
            status = f"{ultima}: {hora}" if ultima else "Sem registro"
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee;"><span>👤 {func["nome"]} <small style="color:#999">— {func["funcao"]}</small></span><span class="{badge}">{status}</span></div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("### 📋 Meu Livro Ponto")
        tela_ponto("admin", dados)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    dados = carregar_dados()

    # Estado de sessão
    if "logado" not in st.session_state:
        st.session_state["logado"] = False
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    # Verificar horário
    dentro_horario = verificar_horario()

    if not st.session_state["logado"]:
        if not dentro_horario:
            tela_bloqueio()
        else:
            tela_login()
        return

    # Usuário logado
    usuario = st.session_state["usuario"]
    func    = FUNCIONARIOS[usuario]

    # Sidebar com logout
    with st.sidebar:
        st.markdown(f"### 👤 {func['nome']}")
        st.caption(func["funcao"])
        st.divider()
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state["logado"] = False
            st.session_state["usuario"] = None
            st.rerun()

    render_wpp_float()

    if func["is_admin"]:
        painel_admin(dados)
    else:
        painel_funcionario(usuario, func, dados)

if __name__ == "__main__":
    main()
