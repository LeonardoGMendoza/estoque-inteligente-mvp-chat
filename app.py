import streamlit as st
import time
from stellar_integration import create_stellar_wallet, fund_wallet_with_friendbot, simulate_microcredit_loan

# Configuração da Página
st.set_page_config(page_title="Estoque Inteligente Copilot", page_icon="🤖", layout="centered")

# CSS Customizado para o Chat
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    /* Balão de IA */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 3px solid #10B981;
    }
    /* Balão do Usuário */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(37, 99, 235, 0.1);
        border-right: 3px solid #2563EB;
    }
    /* Estilo do Botão do Chat */
    .chat-btn > button {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%);
        color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; width: 100%; margin-top: 10px;
    }
    .chat-btn > button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# Inicializando Estado
if 'chat_step' not in st.session_state: st.session_state.chat_step = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'balance' not in st.session_state: st.session_state.balance = 0.0
if 'public_key' not in st.session_state: st.session_state.public_key = None

st.title("🤖 Copilot de Estoque (IA)")
st.caption("Seu assistente financeiro Web3 inteligente")

# Área da Carteira Oculta/Compacta no topo
if st.session_state.public_key is None:
    st.info("Para o Copilot funcionar, conecte sua carteira empresarial.")
    if st.button("🔑 Gerar Carteira Stellar (Testnet)"):
        with st.spinner("Conectando à Blockchain..."):
            pub, sec = create_stellar_wallet()
            st.session_state.public_key = pub
            fund_wallet_with_friendbot(pub)
            st.session_state.balance = 10000.0
            # IA inicia a conversa
            st.session_state.messages.append({"role": "assistant", "content": "Olá! Conectei sua carteira com sucesso. Analisei os dados de vendas da sua loja nas últimas horas."})
            st.session_state.messages.append({"role": "assistant", "content": "🚨 **ALERTA**: Notei que seus *Sacos de Café (50kg)* vão esgotar em apenas **1 dia**. Se não repormos o estoque urgente, você perderá vendas e clientes amanhã. Posso te ajudar a levantar capital de giro agora mesmo?"})
            st.session_state.chat_step = 1
            st.rerun()
    st.stop()
else:
    col1, col2 = st.columns(2)
    col1.markdown(f"**Carteira:** `{st.session_state.public_key[:6]}...{st.session_state.public_key[-4:]}`")
    col2.markdown(f"**Saldo:** `${st.session_state.balance:,.2f} USDC`")
    st.divider()

# Exibir Mensagens Anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Fluxo da Conversa Roteirizada
if st.session_state.chat_step == 1:
    prompt = st.chat_input("Digite sua resposta...")
    if prompt:
        # Salva o que o usuário digitou
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # IA Responde simulando processamento
        with st.chat_message("assistant"):
            with st.spinner("Calculando Garantias DeFi..."):
                time.sleep(1.5)
                reply = """Você tem 10 unidades físicas no estoque. Com o valor de custo de US$ 30,00 por unidade, eu posso **tokenizar** esse estoque na rede Stellar e usá-lo como garantia (Real World Asset).
                
Com uma trava de 70% (LTV), seu limite de crédito instantâneo pré-aprovado é de **US$ 210,00**."""
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.chat_step = 2
                st.rerun()

elif st.session_state.chat_step == 2:
    st.markdown('<div class="chat-btn">', unsafe_allow_html=True)
    if st.button("🚀 Sim, Tokenizar Estoque e Sacar US$ 210,00"):
        st.markdown('</div>', unsafe_allow_html=True)
        # Salva a ação do usuário no chat
        st.session_state.messages.append({"role": "user", "content": "Sim, Tokenizar Estoque e Sacar US$ 210,00"})
        with st.chat_message("user"):
            st.markdown("🚀 Sim, Tokenizar Estoque e Sacar US$ 210,00")
            
        # IA executa o contrato e responde
        with st.chat_message("assistant"):
            with st.spinner("Comunicando com Smart Contract Soroban..."):
                simulate_microcredit_loan(210.0)
                st.session_state.balance += 210.0
                reply_final = "✅ **Sucesso!** O contrato inteligente foi executado. O microcrédito de US$ 210,00 já caiu na sua carteira Stellar. Suas compras com o fornecedor estão garantidas para amanhã! Precisa de mais alguma coisa?"
                st.markdown(reply_final)
                st.balloons()
                st.session_state.messages.append({"role": "assistant", "content": reply_final})
                st.session_state.chat_step = 3
                time.sleep(1)
                st.rerun()

elif st.session_state.chat_step == 3:
    prompt = st.chat_input("Diga algo para encerrar...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": "Estou sempre à disposição! Mantenha suas vendas em alta."})
        st.rerun()
