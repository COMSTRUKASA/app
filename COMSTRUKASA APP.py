import streamlit as st
import json
import os
import hashlib
from datetime import datetime, date
import pandas as pd
from pathlib import Path
import base64
import shutil

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="COMSTRUKASA – Gestão de Funcionários",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Caminhos de dados ───────────────────────────────────────────────────────
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE      = DATA_DIR / "users.json"
PONTO_FILE      = DATA_DIR / "ponto.json"
DOCS_DIR        = DATA_DIR / "documentos"
DOCS_DIR.mkdir(exist_ok=True)

# ── Helpers de persistência ─────────────────────────────────────────────────
def load_json(path, default):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# ── Seed de usuários padrão ─────────────────────────────────────────────────
def seed_users():
    users = load_json(USERS_FILE, {})
    if not users:
        users = {
            "Gustavo": {
                "nome": "Gustavo",
                "senha": hash_pw("Senha572011"),
                "role": "admin",
                "funcao": "Assistente Administrativo",
                "salario": 650.00,
                "meta_vendas": 0.00,
            },
            "joao.silva": {
                "nome": "João Silva",
                "senha": hash_pw("joao123"),
                "role": "funcionario",
                "funcao": "Vendedor",
                "salario": 2500.00,
                "meta_vendas": 20000.00,
            },
            "maria.souza": {
                "nome": "Maria Souza",
                "senha": hash_pw("maria123"),
                "role": "funcionario",
                "funcao": "Caixa",
                "salario": 2200.00,
                "meta_vendas": 15000.00,
            },
        }
        save_json(USERS_FILE, users)
    return users

# ── Estilos CSS ─────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800&family=Barlow+Condensed:wght@700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

    /* Background geral */
    .stApp { background: #0f1923; color: #e8e0d4; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #162130 !important;
        border-right: 2px solid #e8520a;
    }
    section[data-testid="stSidebar"] * { color: #e8e0d4 !important; }

    /* Cards */
    .card {
        background: #1a2b3c;
        border: 1px solid #2a3f52;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: border-color .2s;
    }
    .card:hover { border-color: #e8520a; }
    .card-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.1rem; font-weight: 700;
        color: #e8520a; text-transform: uppercase;
        letter-spacing: .08em; margin-bottom: .5rem;
    }
    .card-value {
        font-size: 2rem; font-weight: 800; color: #e8e0d4;
    }

    /* Botões Streamlit */
    .stButton > button {
        background: #e8520a !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Barlow', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: .04em !important;
        transition: opacity .2s !important;
    }
    .stButton > button:hover { opacity: .85 !important; }

    /* Inputs */
    input, textarea, select {
        background: #1a2b3c !important;
        color: #e8e0d4 !important;
        border-color: #2a3f52 !important;
        border-radius: 8px !important;
    }

    /* Header hero */
    .hero {
        background: linear-gradient(135deg, #e8520a 0%, #c43d00 100%);
        border-radius: 14px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.2rem; font-weight: 800;
        color: #fff; margin: 0; letter-spacing: .04em;
    }
    .hero p { color: rgba(255,255,255,.8); margin: .3rem 0 0; font-size: .95rem; }

    /* Tabela ponto */
    .ponto-row {
        display: flex; align-items: center; gap: 1rem;
        background: #1a2b3c; border-radius: 10px;
        padding: .7rem 1rem; margin-bottom: .5rem;
        border-left: 4px solid #e8520a;
    }
    .ponto-label { font-weight: 700; min-width: 160px; color: #b0bec5; font-size: .85rem; text-transform: uppercase; letter-spacing: .06em; }
    .ponto-time  { font-size: 1.2rem; font-weight: 800; color: #e8e0d4; }
    .ponto-ok    { color: #4caf50; font-size: 1.2rem; }
    .ponto-pend  { color: #e8520a; font-size: 1.2rem; }

    /* Badge role */
    .badge {
        display: inline-block; padding: .2rem .7rem;
        border-radius: 20px; font-size: .78rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: .06em;
    }
    .badge-admin { background: #e8520a22; color: #e8520a; border: 1px solid #e8520a; }
    .badge-func  { background: #1565c022; color: #64b5f6; border: 1px solid #1565c0; }

    /* Progress bar meta */
    .meta-bar-bg {
        background: #0f1923; border-radius: 20px; height: 14px; margin-top: .5rem;
    }
    .meta-bar-fill {
        background: linear-gradient(90deg, #e8520a, #ff7043);
        border-radius: 20px; height: 14px; transition: width .6s ease;
    }

    /* Divider */
    hr { border-color: #2a3f52 !important; }

    /* File uploader */
    [data-testid="stFileUploader"] { border-color: #2a3f52 !important; background: #1a2b3c !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: #162130; border-radius: 10px; }
    .stTabs [data-baseweb="tab"]      { color: #b0bec5 !important; font-weight: 600; }
    .stTabs [aria-selected="true"]    { color: #e8520a !important; border-bottom: 2px solid #e8520a !important; }

    /* Selectbox label */
    label { color: #b0bec5 !important; font-size: .85rem !important; }
    </style>
    """, unsafe_allow_html=True)

# ── Login ───────────────────────────────────────────────────────────────────
def page_login(users):
    st.markdown("""
    <div style='display:flex;justify-content:center;margin-top:3rem;'>
      <div style='background:#1a2b3c;border-radius:16px;padding:2.5rem 2.8rem;width:100%;max-width:420px;border:1px solid #2a3f52;'>
        <div style='text-align:center;margin-bottom:1.8rem;'>
          <span style='font-size:3rem;'>🏗️</span>
          <h1 style='font-family:"Barlow Condensed",sans-serif;font-weight:800;color:#e8e0d4;font-size:1.8rem;margin:.4rem 0 0;'>COMSTRUKASA</h1>
          <p style='color:#b0bec5;font-size:.9rem;margin:.3rem 0 0;'>Sistema de Gestão de Funcionários</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("##### Acesse sua conta")
        usuario = st.text_input("👤 Usuário", placeholder="ex: joao.silva")
        senha   = st.text_input("🔒 Senha", type="password", placeholder="••••••••")
        if st.button("Entrar →", use_container_width=True):
            if usuario in users and users[usuario]["senha"] == hash_pw(senha):
                st.session_state["user"] = usuario
                st.session_state["user_data"] = users[usuario]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
        st.caption("💡 o Aplicativo se encontra em fase de Desenvolvimento, se encontrar algum erro contate: +55 (43) 99696-0065")

# ── Sidebar ─────────────────────────────────────────────────────────────────
def sidebar_menu(user_data):
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:.8rem 0 1.2rem;'>
          <div style='font-size:2rem;text-align:center;'>🏗️</div>
          <div style='text-align:center;font-family:"Barlow Condensed",sans-serif;font-size:1.3rem;font-weight:800;color:#e8520a;'>ConstroApp</div>
          <hr style='margin:.6rem 0;'/>
          <div style='font-size:.95rem;font-weight:700;color:#e8e0d4;'>{user_data["nome"]}</div>
          <div style='font-size:.8rem;color:#b0bec5;'>{user_data["funcao"]}</div>
          <span class='badge {"badge-admin" if user_data["role"]=="admin" else "badge-func"}'>
            {"Admin" if user_data["role"]=="admin" else "Funcionário"}
          </span>
        </div>
        """, unsafe_allow_html=True)

        pagina = st.radio("Navegar", [
            "🏠 Painel",
            "⏱️ Livro Ponto",
            "📄 Documentos",
            *(["👥 Administração"] if user_data["role"] == "admin" else []),
        ])
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            for k in ["user","user_data"]:
                st.session_state.pop(k, None)
            st.rerun()
    return pagina

# ── Painel ──────────────────────────────────────────────────────────────────
def page_painel(username, user_data):
    st.markdown(f"""
    <div class='hero'>
      <h1>Olá, {user_data["nome"].split()[0]}! 👋</h1>
      <p>{date.today().strftime("%A, %d de %B de %Y")} · {user_data["funcao"]}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class='card'>
          <div class='card-title'>💰 Salário Mensal</div>
          <div class='card-value'>R$ {user_data["salario"]:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        meta = user_data["meta_vendas"]
        st.markdown(f"""
        <div class='card'>
          <div class='card-title'>🎯 Meta de Vendas</div>
          <div class='card-value'>R$ {meta:,.2f}</div>
          <div style='color:#b0bec5;font-size:.8rem;margin-top:.3rem;'>Mês atual</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='card'>
          <div class='card-title'>🪪 Função</div>
          <div class='card-value' style='font-size:1.4rem;'>{user_data["funcao"]}</div>
        </div>""", unsafe_allow_html=True)

    # Progresso de vendas (simulado)
    st.markdown("#### 📊 Progresso da Meta")
    vendas_key = f"vendas_{username}"
    vendas_atuais = st.session_state.get(vendas_key, 0.0)
    vendas_input = st.number_input(
        "Atualizar vendas do mês (R$):", min_value=0.0,
        value=vendas_atuais, step=100.0, format="%.2f", key="v_input"
    )
    if st.button("💾 Salvar vendas"):
        st.session_state[vendas_key] = vendas_input
        st.success("Vendas atualizadas!")
        st.rerun()

    pct = min(vendas_atuais / user_data["meta_vendas"] * 100, 100) if user_data["meta_vendas"] > 0 else 0
    cor = "#4caf50" if pct >= 100 else "#e8520a"
    st.markdown(f"""
    <div style='margin-top:.3rem;'>
      <div style='display:flex;justify-content:space-between;font-size:.85rem;color:#b0bec5;'>
        <span>R$ {vendas_atuais:,.2f}</span><span>{pct:.1f}%</span>
      </div>
      <div class='meta-bar-bg'>
        <div class='meta-bar-fill' style='width:{pct}%;background:linear-gradient(90deg,{cor},{cor}99);'></div>
      </div>
      <div style='font-size:.8rem;color:#b0bec5;margin-top:.3rem;'>Meta: R$ {user_data["meta_vendas"]:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Último ponto
    st.markdown("---")
    st.markdown("#### ⏱️ Ponto de Hoje")
    ponto = load_json(PONTO_FILE, {})
    hoje  = str(date.today())
    reg   = ponto.get(username, {}).get(hoje, {})
    marcacoes = [
        ("Entrada",          "entrada"),
        ("Saída Café (manhã)", "saida_cafe_manha"),
        ("Retorno Café",      "retorno_cafe_manha"),
        ("Saída Almoço",      "saida_almoco"),
        ("Retorno Almoço",    "retorno_almoco"),
        ("Saída Café (tarde)", "saida_cafe_tarde"),
        ("Retorno Café (tarde)","retorno_cafe_tarde"),
        ("Saída",             "saida"),
    ]
    cols = st.columns(4)
    for i, (label, key) in enumerate(marcacoes):
        with cols[i % 4]:
            val = reg.get(key, "—")
            icone = "✅" if val != "—" else "⏳"
            st.markdown(f"""
            <div class='card' style='padding:.8rem;text-align:center;'>
              <div class='card-title' style='font-size:.7rem;'>{label}</div>
              <div style='font-size:1.3rem;'>{icone}</div>
              <div style='font-size:.95rem;font-weight:700;color:#e8e0d4;'>{val}</div>
            </div>""", unsafe_allow_html=True)

# ── Livro Ponto ─────────────────────────────────────────────────────────────
def page_ponto(username, user_data):
    st.markdown(f"""
    <div class='hero'>
      <h1>⏱️ Livro Ponto Digital</h1>
      <p>Registre sua jornada · {date.today().strftime("%d/%m/%Y")}</p>
    </div>
    """, unsafe_allow_html=True)

    ponto = load_json(PONTO_FILE, {})
    hoje  = str(date.today())
    if username not in ponto:
        ponto[username] = {}
    if hoje not in ponto[username]:
        ponto[username][hoje] = {}
    reg = ponto[username][hoje]

    marcacoes = [
        ("🟢 Entrada",              "entrada"),
        ("☕ Saída Café (manhã)",    "saida_cafe_manha"),
        ("🔙 Retorno Café",          "retorno_cafe_manha"),
        ("🍽️ Saída Almoço",          "saida_almoco"),
        ("🔙 Retorno Almoço",        "retorno_almoco"),
        ("☕ Saída Café (tarde)",    "saida_cafe_tarde"),
        ("🔙 Retorno Café (tarde)",  "retorno_cafe_tarde"),
        ("🔴 Saída",                 "saida"),
    ]

    st.markdown("### Marcações de Hoje")
    for label, key in marcacoes:
        val = reg.get(key)
        col_l, col_v, col_b = st.columns([3, 2, 2])
        with col_l:
            st.markdown(f"<div style='padding:.5rem 0;font-weight:600;color:#e8e0d4;'>{label}</div>", unsafe_allow_html=True)
        with col_v:
            if val:
                st.markdown(f"<div style='padding:.5rem 0;color:#4caf50;font-weight:700;font-size:1.1rem;'>✅ {val}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='padding:.5rem 0;color:#e8520a;'>⏳ Não marcado</div>", unsafe_allow_html=True)
        with col_b:
            if not val:
                if st.button(f"Marcar agora", key=f"btn_{key}"):
                    agora = datetime.now().strftime("%H:%M:%S")
                    ponto[username][hoje][key] = agora
                    save_json(PONTO_FILE, ponto)
                    st.success(f"Marcado: {agora}")
                    st.rerun()
            else:
                st.caption("Registrado")
        st.markdown("<hr style='margin:.2rem 0;border-color:#1e3046;'>", unsafe_allow_html=True)

    # Histórico
    st.markdown("---")
    st.markdown("### 📅 Histórico de Pontos")
    historico = ponto.get(username, {})
    if historico:
        rows = []
        for dia, regs in sorted(historico.items(), reverse=True):
            rows.append({"Data": dia, **{k: v for k, v in regs.items()}})
        df = pd.DataFrame(rows).fillna("—")
        df.columns = [c.replace("_", " ").title() for c in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado.")

# ── Documentos ──────────────────────────────────────────────────────────────
def page_documentos(username):
    st.markdown("""
    <div class='hero'>
      <h1>📄 Documentos</h1>
      <p>Envie e gerencie seus documentos</p>
    </div>
    """, unsafe_allow_html=True)

    TIPOS = ["Atestado Médico", "Declaração", "Admissão", "Demissão", "Outros"]
    tipo = st.selectbox("Tipo de documento", TIPOS)
    arq  = st.file_uploader("Selecione o arquivo (PDF ou PNG/JPG)", type=["pdf","png","jpg","jpeg"])

    if st.button("📤 Enviar Documento") and arq:
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino  = DOCS_DIR / username
        destino.mkdir(exist_ok=True)
        nome_arq = f"{ts}_{tipo.replace(' ','_')}_{arq.name}"
        with open(destino / nome_arq, "wb") as f:
            f.write(arq.getbuffer())
        st.success(f"✅ Documento enviado: {nome_arq}")

    st.markdown("---")
    st.markdown("### 📁 Meus Documentos")
    pasta = DOCS_DIR / username
    if pasta.exists():
        arquivos = sorted(pasta.iterdir(), reverse=True)
        if arquivos:
            for arq_path in arquivos:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"📎 **{arq_path.name}**")
                with col2:
                    with open(arq_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                    ext = arq_path.suffix.lower()
                    mime = "application/pdf" if ext == ".pdf" else "image/png"
                    href = f'<a href="data:{mime};base64,{b64}" download="{arq_path.name}" style="color:#e8520a;font-weight:700;">⬇ Baixar</a>'
                    st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("Nenhum documento enviado ainda.")
    else:
        st.info("Nenhum documento enviado ainda.")

# ── Administração ────────────────────────────────────────────────────────────
def page_admin():
    st.markdown("""
    <div class='hero'>
      <h1>👥 Administração</h1>
      <p>Gerenciar funcionários e registros</p>
    </div>
    """, unsafe_allow_html=True)

    users = load_json(USERS_FILE, {})
    tabs  = st.tabs(["📋 Funcionários", "⏱️ Pontos Geral", "➕ Novo Funcionário", "✏️ Editar Funcionário"])

    # ── Tab 1: lista
    with tabs[0]:
        rows = []
        for u, d in users.items():
            rows.append({
                "Usuário": u, "Nome": d["nome"], "Função": d["funcao"],
                "Salário (R$)": f'{d["salario"]:,.2f}',
                "Meta (R$)": f'{d["meta_vendas"]:,.2f}',
                "Perfil": d["role"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ── Tab 2: pontos
    with tabs[1]:
        ponto = load_json(PONTO_FILE, {})
        rows  = []
        for user, dias in ponto.items():
            nome = users.get(user, {}).get("nome", user)
            for dia, regs in dias.items():
                rows.append({"Funcionário": nome, "Data": dia, **regs})
        if rows:
            df = pd.DataFrame(rows).fillna("—")
            df.columns = [c.replace("_"," ").title() for c in df.columns]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum ponto registrado.")

    # ── Tab 3: novo funcionário
    with tabs[2]:
        with st.form("novo_func"):
            col1, col2 = st.columns(2)
            with col1:
                n_user  = st.text_input("Login (sem espaços)", placeholder="ana.lima")
                n_nome  = st.text_input("Nome completo")
                n_senha = st.text_input("Senha inicial", type="password")
            with col2:
                n_func  = st.text_input("Função", placeholder="Vendedor")
                n_sal   = st.number_input("Salário (R$)", min_value=0.0, step=100.0, format="%.2f")
                n_meta  = st.number_input("Meta de vendas (R$)", min_value=0.0, step=500.0, format="%.2f")
            n_role  = st.selectbox("Perfil", ["funcionario", "admin"])
            if st.form_submit_button("✅ Cadastrar"):
                if n_user and n_nome and n_senha:
                    if n_user in users:
                        st.error("Usuário já existe!")
                    else:
                        users[n_user] = {
                            "nome": n_nome, "senha": hash_pw(n_senha),
                            "role": n_role, "funcao": n_func,
                            "salario": n_sal, "meta_vendas": n_meta,
                        }
                        save_json(USERS_FILE, users)
                        st.success(f"Funcionário {n_nome} cadastrado!")
                else:
                    st.error("Preencha login, nome e senha.")

    # ── Tab 4: editar
    with tabs[3]:
        sel = st.selectbox("Selecionar funcionário", list(users.keys()))
        ud  = users[sel]
        with st.form("edit_func"):
            col1, col2 = st.columns(2)
            with col1:
                e_nome  = st.text_input("Nome", value=ud["nome"])
                e_func  = st.text_input("Função", value=ud["funcao"])
                e_senha = st.text_input("Nova senha (deixe em branco p/ manter)", type="password")
            with col2:
                e_sal   = st.number_input("Salário (R$)", value=ud["salario"], step=100.0, format="%.2f")
                e_meta  = st.number_input("Meta (R$)", value=ud["meta_vendas"], step=500.0, format="%.2f")
                e_role  = st.selectbox("Perfil", ["funcionario","admin"],
                                       index=0 if ud["role"]=="funcionario" else 1)
            if st.form_submit_button("💾 Salvar alterações"):
                users[sel]["nome"]       = e_nome
                users[sel]["funcao"]     = e_func
                users[sel]["salario"]    = e_sal
                users[sel]["meta_vendas"]= e_meta
                users[sel]["role"]       = e_role
                if e_senha:
                    users[sel]["senha"] = hash_pw(e_senha)
                save_json(USERS_FILE, users)
                st.success("Alterações salvas!")
                st.rerun()

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    users = seed_users()

    if "user" not in st.session_state:
        page_login(users)
        return

    username  = st.session_state["user"]
    user_data = load_json(USERS_FILE, {}).get(username, st.session_state["user_data"])
    pagina    = sidebar_menu(user_data)

    if   "Painel"        in pagina: page_painel(username, user_data)
    elif "Livro Ponto"   in pagina: page_ponto(username, user_data)
    elif "Documentos"    in pagina: page_documentos(username)
    elif "Administração" in pagina: page_admin()

if __name__ == "__main__":
    main()
