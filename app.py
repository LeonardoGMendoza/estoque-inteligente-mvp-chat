import streamlit as st
import streamlit.components.v1 as components
import time
import random
import pandas as pd
import altair as alt
from stellar_integration import create_stellar_wallet, fund_wallet_with_friendbot, simulate_microcredit_loan, get_balance

# ─── Configuração da Página ────────────────────────────────────────────────────
st.set_page_config(page_title="Estoque Inteligente Copilot", page_icon="🤖", layout="wide")

# ─── Fundo Interstellar (estrelas puras CSS) ────────────────────────────────────
def gen_stars(n):
    return ", ".join(f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(n))

star_shadows_1 = gen_stars(700)
star_shadows_2 = gen_stars(200)
star_shadows_3 = gen_stars(100)

st.markdown(f"""
<style>
    .stars  {{ width:1px;  height:1px;  background:transparent; box-shadow:{star_shadows_1}; animation:animStar 50s  linear infinite; position:fixed; top:0; left:0; z-index:-999; }}
    .stars2 {{ width:2px;  height:2px;  background:transparent; box-shadow:{star_shadows_2}; animation:animStar 100s linear infinite; position:fixed; top:0; left:0; z-index:-999; }}
    .stars3 {{ width:3px;  height:3px;  background:transparent; box-shadow:{star_shadows_3}; animation:animStar 150s linear infinite; position:fixed; top:0; left:0; z-index:-999; }}
    .stars::after  {{ content:" "; position:absolute; top:2000px; width:1px;  height:1px;  background:transparent; box-shadow:{star_shadows_1}; }}
    .stars2::after {{ content:" "; position:absolute; top:2000px; width:2px;  height:2px;  background:transparent; box-shadow:{star_shadows_2}; }}
    .stars3::after {{ content:" "; position:absolute; top:2000px; width:3px;  height:3px;  background:transparent; box-shadow:{star_shadows_3}; }}
    @keyframes animStar {{ from {{ transform: translateY(0px); }} to {{ transform: translateY(-2000px); }} }}
</style>
<div class="stars"></div><div class="stars2"></div><div class="stars3"></div>
""", unsafe_allow_html=True)

# ─── CSS Global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp, header { background: transparent !important; color: #e5e7eb; }

    /* Login Box */
    [data-testid="stForm"] {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 20px; padding: 30px;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.2);
    }

    /* Métricas pulsantes */
    [data-testid="metric-container"] {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px; padding: 15px;
        transition: all 0.3s ease;
        animation: pulseGlow 3s infinite alternate;
    }
    @keyframes pulseGlow {
        0%   { box-shadow: 0 0 5px rgba(16, 185, 129, 0.1); transform: translateY(0px);  }
        50%  { box-shadow: 0 0 20px rgba(16, 185, 129, 0.5), 0 0 30px rgba(59, 130, 246, 0.2); transform: translateY(-3px); }
        100% { box-shadow: 0 0 5px rgba(16, 185, 129, 0.1); transform: translateY(0px);  }
    }

    /* Botões Neon */
    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #10B981, #059669);
        color: white; border: none; border-radius: 8px;
        font-weight: 600; letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.7);
        color: white;
    }

    /* Gráficos pulsando */
    @keyframes chartPulse {
        0%   { transform: scale(1);    filter: drop-shadow(0 0 0px #10B981); }
        50%  { transform: scale(1.01); filter: drop-shadow(0 0 8px #10B981); }
        100% { transform: scale(1);    filter: drop-shadow(0 0 0px #10B981); }
    }
    [data-testid="stArrowVegaLiteChart"] {
        animation: chartPulse 4s infinite ease-in-out;
        cursor: pointer;
    }

    /* Botão Analisar Concorrência */
    .btn-analisar {
        display:inline-block; background:linear-gradient(90deg,#10B981,#059669);
        color:white !important; padding:8px 15px; border-radius:6px;
        text-decoration:none; font-weight:bold;
        box-shadow:0 0 10px rgba(16,185,129,0.4); transition:0.3s;
        font-size:14px; text-align:center; width:100%; margin-top:10px;
    }
    .btn-analisar:hover { transform:translateY(-2px); box-shadow:0 0 20px rgba(16,185,129,0.7); }

    /* Modal Hacker (CSS :target) */
    .custom-modal { display:none; position:fixed; top:80px; right:20px; width:450px; z-index:999999; }
    .custom-modal:target { display:flex; }
    .modal-box {
        background:#0d1117; border:1px solid #10B981; border-radius:12px;
        padding:30px; width:100%;
        box-shadow:0 0 40px rgba(16,185,129,0.5); position:relative; font-family:monospace;
    }
    .close-btn { position:absolute; top:12px; right:18px; color:#10B981; text-decoration:none; font-size:28px; }
    .close-btn:hover { color:white; }
    .tw-line { overflow:hidden; white-space:nowrap; width:0; border-right:2px solid #10B981; color:#10B981; margin:10px 0; font-size:15px; }
    .custom-modal:target .line1 { animation: typing 1.5s steps(40,end) forwards, blink 0.5s step-end 3; }
    .custom-modal:target .line2 { animation: typing 2s   steps(40,end) 1.5s forwards, blink 0.5s step-end 4 1.5s; }
    .custom-modal:target .line3 { animation: typing 2s   steps(40,end) 3.5s forwards, blink 0.5s step-end infinite 3.5s; }
    .custom-modal:target .alert-box { animation: fadeIn 0.5s ease 5.5s forwards; opacity:0; }
    @keyframes typing { to { width:100%; } }
    @keyframes blink   { 50% { border-color:transparent; } }
    @keyframes fadeIn  { to { opacity:1; } }

    /* Upload Avatar */
    [data-testid="stFileUploader"] { border-radius:50%; overflow:hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Estado da Sessão ──────────────────────────────────────────────────────────
if 'logged_in'        not in st.session_state: st.session_state.logged_in        = False
if 'chat_step'        not in st.session_state: st.session_state.chat_step        = 0
if 'messages'         not in st.session_state: st.session_state.messages         = []
if 'balance'          not in st.session_state: st.session_state.balance          = 0.0
if 'public_key'       not in st.session_state: st.session_state.public_key       = None
if 'profile'          not in st.session_state: st.session_state.profile          = {}
if 'market_variation' not in st.session_state: st.session_state.market_variation = round(random.uniform(-8.5, -2.0), 1)
if 'loan_val'         not in st.session_state: st.session_state.loan_val         = 0.0
if 'show_chat'        not in st.session_state: st.session_state.show_chat        = True
if 'stellar_hash'     not in st.session_state: st.session_state.stellar_hash     = ""

# ─── TELA DE LOGIN ─────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div style="text-align:center"><img src="https://cryptologos.cc/logos/stellar-xlm-logo.png" width="60" style="filter:invert(1) drop-shadow(0 0 10px #fff)"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#9CA3AF'>Entre com seu e-mail para carregar os dados da sua empresa.</p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6B7280;font-size:0.85em;text-align:center'>Dica: Use <b>desenvolvimento3000@outlook.com</b> para o perfil demo!</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("E-mail", placeholder="desenvolvimento3000@outlook.com")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")
            submit_login = st.form_submit_button("Entrar no Sistema", use_container_width=True)

            if submit_login:
                if email:
                    with st.spinner("Autenticando e buscando dados do ERP..."):
                        time.sleep(1.2)
                        el = email.lower()
                        if "desenvolvimento3000" in el:
                            st.session_state.profile = {"name":"Leonardo Gonzales","biz":"Indústria Robótica (Parceria com Elon Musk)","prod":"Robôs Humanoides Optimus","cost":15000.0,"market":25000.0,"stock":3,"sales":1500000,"items":60,"competitor_name":"Mercado Chinês","icon":"🤖"}
                        elif "roupa" in el:
                            st.session_state.profile = {"name":"Carlos","biz":"Boutique Elegance","prod":"Camisetas Premium","cost":15.0,"market":35.0,"stock":25,"sales":45000,"items":1200,"competitor_name":"Concorrência (Média)","icon":"👗"}
                        elif "oficina" in el:
                            st.session_state.profile = {"name":"Pedro","biz":"Oficina do Pedro","prod":"Pneus Aro 15","cost":80.0,"market":120.0,"stock":4,"sales":125000,"items":450,"competitor_name":"Concorrência (Média)","icon":"🔧"}
                        else:
                            st.session_state.profile = {"name":"Maria","biz":"Cafeteria Central","prod":"Sacos de Café (50kg)","cost":30.0,"market":45.0,"stock":10,"sales":32000,"items":800,"competitor_name":"Concorrência (Média)","icon":"☕"}
                        st.session_state.market_variation = round(random.uniform(-8.5, -2.0), 1)
                        st.session_state.logged_in = True
                        st.rerun()
                else:
                    st.error("Preencha o e-mail para entrar.")

# ─── DASHBOARD PRINCIPAL ───────────────────────────────────────────────────────
else:
    P = st.session_state.profile   # alias curto

    # Sidebar
    lang_opt  = st.sidebar.radio("🌐 Idioma / Language", ["PT","EN","ES"], horizontal=True)
    live_mode = st.sidebar.checkbox("🔴 Live Market Mode", value=False)

    if 'live_sales'  not in st.session_state: st.session_state.live_sales  = P['sales']
    if 'live_market' not in st.session_state: st.session_state.live_market = P['market']
    if 'live_pie'    not in st.session_state: st.session_state.live_pie    = [65, 25, 10]
    if 'avatar_bytes' not in st.session_state: st.session_state.avatar_bytes = None

    # Avatar (persistente em disco)
    import os, hashlib
    avatar_dir = os.path.join(os.path.dirname(__file__), "avatars")
    os.makedirs(avatar_dir, exist_ok=True)
    avatar_key = hashlib.md5(P['name'].encode()).hexdigest()
    avatar_path = os.path.join(avatar_dir, f"{avatar_key}.png")

    # Carrega do disco se existir e session_state estiver vazio
    if st.session_state.avatar_bytes is None and os.path.exists(avatar_path):
        st.session_state.avatar_bytes = open(avatar_path, "rb").read()

    col_i1, col_i2, col_i3 = st.sidebar.columns([1,2,1])
    with col_i2:
        avatar_src = st.session_state.avatar_bytes if st.session_state.avatar_bytes else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        if "Maria" in P['name']:
            avatar_src = st.session_state.avatar_bytes if st.session_state.avatar_bytes else "https://cdn-icons-png.flaticon.com/512/4140/4140047.png"
        st.image(avatar_src, use_container_width=True)
        if st.session_state.avatar_bytes is None:
            up = st.file_uploader("", type=['png','jpg','jpeg'], label_visibility="collapsed")
            if up:
                img_bytes = up.getvalue()
                st.session_state.avatar_bytes = img_bytes
                # Salva no disco para persistir entre sessões
                with open(avatar_path, "wb") as f:
                    f.write(img_bytes)
                st.rerun()

    st.sidebar.markdown(f"<h3 style='text-align:center;margin-top:-10px'>{P['name']}</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='text-align:center;color:gray'>{P['biz']}</p>", unsafe_allow_html=True)
    st.sidebar.divider()

    # Labels traduzidos da sidebar
    sidebar_labels = {
        "PT": {"config": "⚙️ Configurações", "logout": "🚪 Sair / Cambiar Empresa"},
        "EN": {"config": "⚙️ Settings", "logout": "🚪 Logout / Switch Company"},
        "ES": {"config": "⚙️ Configuración", "logout": "🚪 Salir / Cambiar Empresa"},
    }
    sl = sidebar_labels[lang_opt]

    st.sidebar.title(sl["config"])
    if st.sidebar.button(sl["logout"], use_container_width=True):
        for k in ['logged_in','chat_step','messages','public_key','profile','avatar_bytes','live_sales','live_market','live_pie']:
            st.session_state.pop(k, None)
        st.rerun()

    # Traduções
    T = {
        "PT": {
            "title":"📊 Monitor de Performance & Copilot IA",
            "warning":"Conecte sua carteira Stellar para ativar os gráficos e a IA.",
            "btn_connect":"🔑 Conectar Carteira Stellar e Ativar IA",
            "metric_sales":"💰 Receita Total (Mês)","metric_vol":"📦 Volume (Itens)",
            "metric_comp":"📈 Concorrência","metric_bal":"💳 Saldo Stellar (XLM)",
            "chart_sales":"Performance de Vendas","chart_live":"Mercado ao Vivo",
            "chart_pie":"Concentração de Lucro",
            "greeting":"Olá {name}! Conectei sua carteira Stellar. Analisei o ERP da **{biz}**.",
            "alert":"🚨 **ALERTA**: Seus *{prod}* vão esgotar amanhã. A concorrência cobra **US$ {market:.2f}** (-{variation}% desde ontem)!\n\nPosso tokenizar seu estoque para levantar capital de giro agora?",
            "calc":"Você tem **{stock}** unidades de *{prod}* (custo US$ {cost:.2f}). Tokenizando com **LTV de 70%**, seu limite é **US$ {loan:,.2f}**.\n\nDeseja emitir o contrato Soroban na Testnet Stellar?",
            "success":"✅ **Sucesso!** Smart Contract executado! Hash: `{hash}`\n\n**US$ {loan:,.2f}** creditados na sua carteira Stellar. Reposição garantida!",
            "end":"Obrigado! Acompanhe os gráficos — as vendas vão subir amanhã!",
            "default":"Entendido! Estou monitorando o mercado em tempo real. Como posso ajudar?",
            "placeholder":"Fale com o Copilot...",
            "js_bot_title":"Pronto para conversar",
            "js_sim_resp":"⏳ Conectando na Stellar Testnet...\\n\\n🔗 Executando Smart Contract Soroban...\\n\\n✅ **Contrato liquidado!**\\nHash: `TESTNET_DEMO`\\n\\n💸 **US$ {loan_val}** creditados na sua carteira!",
            "js_sim_badge":"💳 {loan_xlm} XLM ✅ ATUALIZADO",
            "js_comp_resp":"📊 **Análise de Concorrência**\\n\\n**{comp}** reduziu preços {var}% desde ontem.\\n\\n⚠️ Recomendo ação imediata! Digite **SIM** para tokenizar via Stellar.",
            "js_credit_resp":"🚀 **Crédito RWA via Stellar!**\\n\\nPosso tokenizar **{stk} unidades de {prd}** agora.\\n\\nLimite: **US$ {loan_val}** (LTV 70%)\\n\\nDigite **SIM** para emitir o contrato Soroban!",
            "js_default_resp":"🤖 Estou monitorando **{prd}** em tempo real.\\n\\nPosso ajudar com:\\n• Vendas e performance\\n• Análise de concorrência\\n• Crédito via tokenização Stellar\\n\\nComo posso ajudar?",
        },
        "EN": {
            "title":"📊 Performance Monitor & AI Copilot",
            "warning":"Connect your Stellar wallet to activate charts and AI.",
            "btn_connect":"🔑 Connect Stellar Wallet & Activate AI",
            "metric_sales":"💰 Total Revenue (Month)","metric_vol":"📦 Volume (Items)",
            "metric_comp":"📈 Competitors","metric_bal":"💳 Stellar Balance (XLM)",
            "chart_sales":"Sales Performance","chart_live":"Live Market",
            "chart_pie":"Profit Concentration",
            "greeting":"Hello {name}! I connected your Stellar wallet. I analyzed **{biz}** ERP.",
            "alert":"🚨 **ALERT**: Your *{prod}* will run out tomorrow. Competitors charge **US$ {market:.2f}** (-{variation}% since yesterday)!\n\nCan I tokenize your stock to raise working capital now?",
            "calc":"You have **{stock}** units of *{prod}* (cost US$ {cost:.2f}). With a **70% LTV**, your limit is **US$ {loan:,.2f}**.\n\nDo you want to issue the Soroban contract on Stellar Testnet?",
            "success":"✅ **Success!** Smart Contract executed! Hash: `{hash}`\n\n**US$ {loan:,.2f}** credited to your Stellar wallet. Stock replenishment guaranteed!",
            "end":"Thank you! Watch your charts — sales will go up tomorrow!",
            "default":"Understood! I'm monitoring the market in real-time. How can I help?",
            "placeholder":"Talk to Copilot...",
            "js_bot_title":"Ready to chat",
            "js_sim_resp":"⏳ Connecting to Stellar Testnet...\\n\\n🔗 Executing Soroban Smart Contract...\\n\\n✅ **Contract settled!**\\nHash: `TESTNET_DEMO`\\n\\n💸 **US$ {loan_val}** credited to your wallet!",
            "js_sim_badge":"💳 {loan_xlm} XLM ✅ UPDATED",
            "js_comp_resp":"📊 **Competitor Analysis**\\n\\n**{comp}** reduced prices {var}% since yesterday.\\n\\n⚠️ Immediate action recommended! Type **YES** to tokenize via Stellar.",
            "js_credit_resp":"🚀 **RWA Credit via Stellar!**\\n\\nI can tokenize **{stk} units of {prd}** now.\\n\\nLimit: **US$ {loan_val}** (70% LTV)\\n\\nType **YES** to issue the Soroban contract!",
            "js_default_resp":"🤖 I'm monitoring **{prd}** in real-time.\\n\\nI can help with:\\n• Sales & performance\\n• Competitor analysis\\n• Credit via Stellar tokenization\\n\\nHow can I help?",
        },
        "ES": {
            "title":"📊 Monitor de Rendimiento & Copilot IA",
            "warning":"Conecta tu billetera Stellar para activar los gráficos y la IA.",
            "btn_connect":"🔑 Conectar Billetera Stellar y Activar IA",
            "metric_sales":"💰 Ingresos Totales (Mes)","metric_vol":"📦 Volumen (Artículos)",
            "metric_comp":"📈 Competencia","metric_bal":"💳 Saldo Stellar (XLM)",
            "chart_sales":"Rendimiento de Ventas","chart_live":"Mercado en Vivo",
            "chart_pie":"Concentración de Lucro",
            "greeting":"¡Hola {name}! Conecté tu billetera Stellar. Analicé el ERP de **{biz}**.",
            "alert":"🚨 **ALERTA**: Tus *{prod}* se agotarán mañana. La competencia cobra **US$ {market:.2f}** (-{variation}% desde ayer)!\n\n¿Puedo tokenizar tu stock para levantar capital de trabajo ahora?",
            "calc":"Tienes **{stock}** unidades de *{prod}* (costo US$ {cost:.2f}). Con **LTV del 70%**, tu límite es **US$ {loan:,.2f}**.\n\n¿Deseas emitir el contrato Soroban en la Testnet de Stellar?",
            "success":"✅ **¡Éxito!** ¡Contrato Soroban ejecutado! Hash: `{hash}`\n\n**US$ {loan:,.2f}** acreditados en tu billetera Stellar. ¡Reposición garantizada!",
            "end":"¡Gracias! ¡Mira tus gráficos, las ventas subirán mañana!",
            "default":"¡Entendido! Estoy monitoreando el mercado en tiempo real. ¿Cómo puedo ayudar?",
            "placeholder":"Habla con el Copilot...",
            "js_bot_title":"Listo para chatear",
            "js_sim_resp":"⏳ Conectando a Stellar Testnet...\\n\\n🔗 Ejecutando Smart Contract Soroban...\\n\\n✅ **¡Contrato liquidado!**\\nHash: `TESTNET_DEMO`\\n\\n💸 **US$ {loan_val}** acreditados en tu billetera!",
            "js_sim_badge":"💳 {loan_xlm} XLM ✅ ACTUALIZADO",
            "js_comp_resp":"📊 **Análisis de Competencia**\\n\\n**{comp}** redujo precios {var}% desde ayer.\\n\\n⚠️ ¡Acción inmediata recomendada! Escribe **SIM** o **YES** para tokenizar vía Stellar.",
            "js_credit_resp":"🚀 **¡Crédito RWA vía Stellar!**\\n\\nPuedo tokenizar **{stk} unidades de {prd}** ahora.\\n\\nLímite: **US$ {loan_val}** (LTV 70%)\\n\\n¡Escribe **SIM** o **YES** para emitir el contrato Soroban!",
            "js_default_resp":"🤖 Estoy monitoreando **{prd}** en tiempo real.\\n\\nPuedo ayudar con:\\n• Ventas y rendimiento\\n• Análisis de competencia\\n• Crédito vía tokenización Stellar\\n\\n¿Cómo puedo ayudar?",
        }
    }
    t = T[lang_opt]

    # Live mode
    if live_mode:
        st.session_state.live_sales  += random.randint(-5000, 15000)
        st.session_state.live_market += random.uniform(-0.5, 0.5)
        st.session_state.market_variation += round(random.uniform(-0.2, 0.2), 1)
        pie = st.session_state.live_pie
        st.session_state.live_pie = [max(1, pie[0]+random.randint(-2,2)), max(1, pie[1]+random.randint(-1,1)), 10]

    # Header
    st.title(t["title"])

    # Conectar Stellar
    if st.session_state.public_key is None:
        st.warning(t["warning"])
        if st.button(t["btn_connect"]):
            with st.spinner("Conectando à Blockchain Stellar Testnet..."):
                pub, sec = create_stellar_wallet()
                st.session_state.public_key = pub
                ok = fund_wallet_with_friendbot(pub)
                bal = get_balance(pub) if ok else 10000.0
                st.session_state.balance = bal
                greeting = t["greeting"].format(name=P['name'], biz=P['biz'])
                alert = t["alert"].format(prod=P['prod'], market=st.session_state.live_market, variation=abs(round(st.session_state.market_variation,1)))
                st.session_state.messages = [
                    {"role":"assistant","content": greeting},
                    {"role":"assistant","content": alert},
                ]
                st.session_state.chat_step = 1
                st.rerun()
        st.stop()

    # Modal da Concorrência (CSS :target trick)
    competitor = P.get('competitor_name', 'Mercado')
    modal_html = f"""
    <style>
    .custom-modal {{ display:none; position:fixed; top:80px; right:20px; width:460px; z-index:999999; }}
    .custom-modal:target {{ display:flex; }}
    .modal-box {{
        background:#0d1117; border:1px solid #10B981; border-radius:14px;
        padding:28px; width:100%;
        box-shadow:0 0 50px rgba(16,185,129,0.5); position:relative; font-family:monospace;
    }}
    .close-btn {{ position:absolute; top:12px; right:18px; color:#10B981; text-decoration:none; font-size:28px; }}
    .close-btn:hover {{ color:white; }}
    .tw-line {{ overflow:hidden; white-space:nowrap; width:0; border-right:2px solid #10B981; color:#10B981; margin:10px 0; font-size:14px; }}
    .custom-modal:target .line1 {{ animation: typing 1.5s steps(40,end) forwards, blink 0.5s step-end 3; }}
    .custom-modal:target .line2 {{ animation: typing 2s   steps(40,end) 1.5s forwards, blink 0.5s step-end 4 1.5s; }}
    .custom-modal:target .line3 {{ animation: typing 2s   steps(40,end) 3.5s forwards, blink 0.5s step-end infinite 3.5s; }}
    .custom-modal:target .alert-box {{ animation: fadeIn 0.5s ease 5.5s forwards; opacity:0; }}
    @keyframes typing {{ to {{ width:100%; }} }}
    @keyframes blink   {{ 50% {{ border-color:transparent; }} }}
    @keyframes fadeIn  {{ to {{ opacity:1; }} }}
    .btn-analisar {{
        display:inline-block; background:linear-gradient(90deg,#10B981,#059669);
        color:white !important; padding:8px 14px; border-radius:6px;
        text-decoration:none; font-weight:bold;
        box-shadow:0 0 10px rgba(16,185,129,0.4); transition:0.3s;
        font-size:14px; text-align:center; width:100%; margin-top:10px;
        display:block;
    }}
    .btn-analisar:hover {{ transform:translateY(-2px); box-shadow:0 0 20px rgba(16,185,129,0.7); }}
    </style>

    <div id="comp-modal" class="custom-modal">
      <div class="modal-box">
        <a href="#" class="close-btn">&times;</a>
        <h2 style="color:white;margin-top:0;font-family:'Inter',sans-serif">📊 Análise: {competitor}</h2>
        <div style="background:black;padding:18px;border-radius:8px;min-height:180px;border:1px solid #333">
          <div class="tw-line line1">&gt; COLETANDO DADOS PÚBLICOS DE MERCADO... [OK]</div>
          <div class="tw-line line2">&gt; DETECTADO DUMPING EM {P.get('prod','').upper()[:20]}. MARGEM: 4.2%</div>
          <div class="tw-line line3">&gt; PREÇO {competitor.upper()[:20]}: US$ {st.session_state.live_market:.2f} — QUEDA {abs(round(st.session_state.market_variation,1))}%</div>
          <div class="alert-box" style="margin-top:18px;padding:10px;background:rgba(239,68,68,0.2);border-left:4px solid #EF4444;color:#FCA5A5">
            ⚠️ IA RECOMENDA: Tokenizar estoque via Soroban para garantir capital de giro imediatamente.
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(modal_html, unsafe_allow_html=True)

    # ── Métricas ───────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t["metric_sales"], f"US$ {int(st.session_state.live_sales):,}")
    col2.metric(t["metric_vol"],   f"{P['items']}")
    with col3:
        st.metric(competitor, f"US$ {st.session_state.live_market:.2f}", f"{st.session_state.market_variation:.1f}% vs Ontem")
        st.markdown(f'<a href="#comp-modal" class="btn-analisar">🔎 Analisar Concorrência</a>', unsafe_allow_html=True)
    col4.metric(t["metric_bal"], f"{st.session_state.balance:,.2f} XLM")

    st.divider()

    # ── Gráficos ───────────────────────────────────────────────────────────────
    col_c1, col_c2, col_c3 = st.columns(3)

    with col_c1:
        st.subheader(t["chart_sales"])
        df_s = pd.DataFrame({
            "Mês": ["Jan","Fev","Mar","Abr","Mai","Jun"],
            "Vendas": [P['sales']*x for x in [0.6,0.7,0.65,0.8,0.9,st.session_state.live_sales/P['sales']]]
        })
        st.altair_chart(
            alt.Chart(df_s).mark_area(opacity=0.5, line={'color':'#10B981'}, color='#10B981').encode(
                x=alt.X("Mês", sort=None),
                y=alt.Y("Vendas", scale=alt.Scale(zero=False))
            ).properties(height=250),
            use_container_width=True
        )

    with col_c2:
        st.subheader(t["chart_live"])
        df_m = pd.DataFrame({
            "Métrica": ["Seu Custo","Seu Preço", competitor],
            "Valor":   [P['cost'], P['cost']*1.5, st.session_state.live_market]
        })
        st.altair_chart(
            alt.Chart(df_m).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
                x=alt.X("Métrica", sort=None, axis=alt.Axis(labelAngle=0)),
                y="Valor",
                color=alt.condition(
                    alt.datum.Métrica == competitor,
                    alt.value('#EF4444'), alt.value('#3B82F6')
                )
            ).properties(height=250),
            use_container_width=True
        )

    with col_c3:
        st.subheader(t["chart_pie"])
        df_p = pd.DataFrame({
            "Produto":    [P['prod'], "Outros","Serviços"],
            "Percentual": st.session_state.live_pie
        })
        st.altair_chart(
            alt.Chart(df_p).mark_arc(innerRadius=40).encode(
                theta="Percentual",
                color=alt.Color("Produto", scale=alt.Scale(scheme="set2"), legend=alt.Legend(orient="bottom")),
                tooltip=["Produto","Percentual"]
            ).properties(height=250),
            use_container_width=True
        )
        # Clique na pizza → abre modal
        components.html("""
        <script>
        try {
            var charts = window.parent.document.querySelectorAll('[data-testid="stArrowVegaLiteChart"]');
            if (charts.length > 0) {
                var pie = charts[charts.length-1];
                pie.title = 'Clique para analisar a Concorrência';
                pie.addEventListener('click', function(){
                    window.parent.location.hash = 'comp-modal';
                });
            }
        } catch(e) {}
        </script>""", height=0, width=0)

    st.divider()

    # ─── CHAT FLUTUANTE HTML PURO (Igual Lions Agent) ──────────────────────────
    import json

    # Serializa variáveis Python → JSON para injetar no JS de forma segura
    # Regenera as mensagens iniciais no idioma ATUAL (para acompanhar troca de idioma)
    greeting_now = t["greeting"].format(name=P['name'], biz=P['biz'])
    alert_now    = t["alert"].format(prod=P['prod'], market=st.session_state.live_market, variation=abs(round(st.session_state.market_variation,1)))
    
    # Monta a lista: mensagens iniciais traduzidas + mensagens do usuário (chat_step > 0)
    translated_msgs = [
        {"role": "assistant", "text": greeting_now},
        {"role": "assistant", "text": alert_now},
    ]
    # Adiciona mensagens extras do usuário (se existirem além das 2 iniciais)
    if len(st.session_state.messages) > 2:
        for m in st.session_state.messages[2:]:
            translated_msgs.append({"role": m.get("role","assistant"), "text": m.get("content","")})
    
    msgs_json = json.dumps(translated_msgs, ensure_ascii=False)

    placeholder_txt = t.get("placeholder","Fale com o Copilot...")
    pub_key_short   = (st.session_state.public_key[:8] + "..." + st.session_state.public_key[-4:]) if st.session_state.public_key else ""
    bal_display     = f"{st.session_state.balance:,.0f} XLM"
    loan_amount     = round((P['stock'] * P['cost']) * 0.70, 2)
    new_balance_override = st.session_state.balance + loan_amount

    lion_fab        = '☕' if P.get('prod','') and 'café' in P.get('prod','').lower() else ('🦁' if '🤖' == P.get('icon','🤖') else P.get('icon','🦁'))
    competitor_js   = json.dumps(P.get('competitor_name','Mercado'))
    prod_js         = json.dumps(P.get('prod','produto'))
    stock_js        = P['stock']
    variation_js    = abs(round(st.session_state.market_variation, 1))

    # CSS da interface do chat
    chat_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }
body { background:transparent; overflow:hidden; }
#fab {
  position:fixed; bottom:20px; right:20px;
  width:62px; height:62px; border-radius:50%;
  background:linear-gradient(135deg,#EAB308,#D97706);
  border:2px solid rgba(255,255,255,0.3); font-size:28px; cursor:pointer;
  box-shadow:0 4px 20px rgba(234,179,8,0.6);
  display:flex; align-items:center; justify-content:center;
  transition:all 0.3s; z-index:99999;
}
#fab:hover { transform:scale(1.12); box-shadow:0 4px 30px rgba(234,179,8,1); }
#chat-panel {
  position:fixed; bottom:92px; right:20px; width:360px; max-height:520px;
  background:rgba(13,10,5,0.97); border:2px solid #EAB308; border-radius:18px;
  box-shadow:0 10px 40px rgba(0,0,0,0.9),0 0 20px rgba(234,179,8,0.3);
  display:flex; flex-direction:column; z-index:99998; overflow:hidden; transition:all 0.3s ease;
}
#chat-panel.hidden { display:none; }
.chat-header {
  display:flex; align-items:center; gap:10px; padding:12px 16px;
  border-bottom:1px solid rgba(234,179,8,0.3); background:rgba(20,15,5,0.8);
}
.chat-avatar { font-size:26px; }
.chat-title { flex:1; }
.chat-title h4 { color:#FFF; font-size:14px; font-weight:700; }
.chat-title p  { color:#10B981; font-size:11px; }
.chat-close { color:#EAB308; font-size:20px; cursor:pointer; padding:4px; border-radius:50%; }
.chat-close:hover { color:#fff; background:rgba(234,179,8,0.2); }
.wallet-badge {
  background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);
  border-radius:6px; padding:6px 12px; margin:8px; font-size:11px; color:#10B981; text-align:center;
}
#chat-messages {
  flex:1; overflow-y:auto; padding:8px 10px; display:flex; flex-direction:column; gap:8px;
}
#chat-messages::-webkit-scrollbar { width:3px; }
#chat-messages::-webkit-scrollbar-thumb { background:#EAB308; border-radius:3px; }
.msg { max-width:85%; border-radius:12px; padding:10px 13px; font-size:13px; line-height:1.5; }
.msg.assistant {
  background:rgba(30,25,5,0.9); border-left:3px solid #EAB308;
  color:#e5e7eb; align-self:flex-start; border-radius:4px 12px 12px 12px;
}
.msg.user {
  background:linear-gradient(135deg,#10B981,#059669);
  color:#fff; align-self:flex-end; border-radius:12px 4px 12px 12px;
}
.chat-input-row {
  display:flex; gap:6px; padding:10px;
  border-top:1px solid rgba(234,179,8,0.2); background:rgba(10,8,2,0.9);
}
#chat-input {
  flex:1; background:#111; border:1px solid #EAB308; color:#fff;
  border-radius:8px; padding:8px 12px; font-size:13px; outline:none;
}
#chat-input::placeholder { color:#666; }
#send-btn {
  background:#EAB308; color:#000; border:none;
  border-radius:8px; padding:8px 14px; cursor:pointer; font-size:16px; font-weight:bold; transition:0.2s;
}
#send-btn:hover { background:#FBBF24; }
</style>"""

    # HTML da estrutura do chat
    chat_html = f"""<!DOCTYPE html>
<html>
<head>{chat_css}</head>
<body>
<div id="fab" onclick="toggleChat()" title="Abrir Copilot IA">🦁</div>
<div id="chat-panel">
  <div class="chat-header">
    <div class="chat-avatar">🦁</div>
    <div class="chat-title"><h4>Lions Agent</h4><p>🟢 {t["js_bot_title"]}</p></div>
    <div class="chat-close" onclick="toggleChat()">✕</div>
  </div>
  <div class="wallet-badge" id="bal-badge">🔗 {pub_key_short} &nbsp;|&nbsp; 💳 {bal_display}</div>
  <div id="chat-messages"></div>
  <div class="chat-input-row">
    <input id="chat-input" type="text" placeholder="{placeholder_txt}" onkeydown="if(event.key==='Enter') sendMsg()">
    <button id="send-btn" onclick="sendMsg()">➤</button>
  </div>
</div>
<script>
var msgs = {msgs_json};
var competitor = {competitor_js};
var prod       = {prod_js};
var stock      = {stock_js};
var loan       = {loan_amount};
var variation  = {variation_js};

function toggleChat() {{
  document.getElementById('chat-panel').classList.toggle('hidden');
}}

function fmt(s) {{
  return String(s)
    .replace(/\\n/g, '<br>')
    .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
    .replace(/\\*(.*?)\\*/g, '<i>$1</i>')
    .replace(/`([^`]+)`/g, '<code style="background:#1a1a1a;padding:2px 4px;border-radius:3px">$1</code>');
}}

function render() {{
  var c = document.getElementById('chat-messages');
  c.innerHTML = '';
  msgs.forEach(function(m) {{
    var d = document.createElement('div');
    d.className = 'msg ' + m.role;
    d.innerHTML = fmt(m.text);
    c.appendChild(d);
  }});
  c.scrollTop = c.scrollHeight;
}}

function addMsg(role, text) {{
  msgs.push({{role: role, text: text}});
  render();
}}

function sendMsg() {{
  var inp = document.getElementById('chat-input');
  var txt = inp.value.trim();
  if (!txt) return;
  inp.value = '';
  addMsg('user', txt);

  setTimeout(function() {{
    var lower = txt.toLowerCase();
    var resp;
    var loanStr = loan.toLocaleString('en-US', {{minimumFractionDigits:2, maximumFractionDigits:2}});
    var loanXlm = Math.round(loan).toLocaleString('en-US');
    if (lower.includes('sim') || lower.includes('yes') || lower.includes('tokeniz') || lower.includes('sacar')) {{
      resp = '{t["js_sim_resp"]}'.replace('{{loan_val}}', loanStr);
      setTimeout(function() {{
        var b = document.getElementById('bal-badge');
        if (b) {{ b.innerHTML = '{t["js_sim_badge"]}'.replace('{{loan_xlm}}', loanXlm); b.style.color = '#10B981'; b.style.borderColor = '#10B981'; }}
        
        // Ativa o OVERRIDE VISUAL absoluto no documento pai (Streamlit)
        window.parent.stellar_new_balance = {new_balance_override};
      }}, 1500);
    }} else if (lower.includes('concorr') || lower.includes('competitor') || lower.includes('competencia')) {{
      resp = '{t["js_comp_resp"]}'.replace('{{comp}}', competitor).replace('{{var}}', variation);
    }} else if (lower.includes('stellar') || lower.includes('credito') || lower.includes('dinheiro') || lower.includes('money') || lower.includes('loan')) {{
      resp = '{t["js_credit_resp"]}'.replace('{{stk}}', stock).replace('{{prd}}', prod).replace('{{loan_val}}', loanStr);
    }} else {{
      resp = '{t["js_default_resp"]}'.replace('{{prd}}', prod);
    }}
    addMsg('assistant', resp);
  }}, 800);
}}

// LOOP DE SOBREPOSIÇÃO VISUAL (Garante que o Streamlit mostre o saldo atualizado mesmo com st.rerun)
setInterval(function() {{
    if (window.parent.stellar_new_balance) {{
        var metrics = window.parent.document.querySelectorAll('[data-testid="stMetricValue"] div');
        for (var k = 0; k < metrics.length; k++) {{
            if (metrics[k].innerText.includes('XLM')) {{
                metrics[k].innerText = window.parent.stellar_new_balance.toLocaleString('en-US', {{minimumFractionDigits: 2, maximumFractionDigits: 2}}) + ' XLM';
            }}
        }}
    }}
}}, 100);

render();
</script>
</body>
</html>"""

    components.html(chat_html, height=640, scrolling=False)

    # Loop Live Mode
    if live_mode:
        time.sleep(1.5)
        st.rerun()

