# 🤖 Estoque Inteligente Copilot (AI Agent MVP)

O **Estoque Inteligente Copilot** é uma evolução do nosso MVP original para o PULSO Hackathon (Stellar). 
Transformamos o complexo painel de controle financeiro em um **Agente de IA Autônomo e Conversacional**, focado em oferecer a experiência mais simples e mágica possível para microempreendedores da América Latina.

Em vez de analisar gráficos, o usuário interage via chat com o Agente de IA, que proativamente avisa sobre riscos de ruptura de estoque e aciona contratos inteligentes (Smart Contracts) para liberar **Microcrédito Colateralizado (RWA)** na rede Stellar em apenas 1 clique.

---

## 📸 Screenshots da Experiência Conversacional

*(Adicione suas screenshots da conversa com a IA aqui)*

| Agente Analisando Risco | Aprovação RWA na Stellar (1 Clique) |
|:---:|:---:|
| `<img src="caminho/imagem1.png" width="400"/>` | `<img src="caminho/imagem2.png" width="400"/>` |

---

## 🧠 Como Funciona o Copilot?
1. **Contexto Ativo:** O Agente sabe quem você é, o que você vende e qual é o nível do seu estoque físico.
2. **Abordagem Proativa:** A IA avisa no chat que o café vai acabar nos próximos dias e que você vai perder clientes.
3. **Ponte para o DeFi:** A IA calcula automaticamente o seu LTV (Loan-to-Value) com base no estoque restante e oferece a solução: *"Quer que eu tokenize o resto do seu estoque e pegue US$ 210,00 emprestado para repormos a mercadoria?"*
4. **Execução Web3 Roteirizada:** Ao clicar "Sim" direto no chat, o Streamlit usa o `stellar-sdk` para falar com a blockchain, simular a trava de garantia (collateral) e transferir os dólares (USDC/XLM) para a carteira instantaneamente.

## 🚀 Tecnologias
* **Frontend:** Python, Streamlit (Elementos nativos de Chat UI)
* **Integração Blockchain:** `stellar-sdk` na Testnet
* **Agente IA:** Mock de Lógica Decisional para MVP de 2 minutos perfeito (Segurança contra alucinações durante o pitch de hackathon).

## 💻 Como Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/LeonardoGMendoza/estoque-inteligente-mvp-chat.git
cd estoque-inteligente-mvp-chat
```

2. Instale as dependências:
```bash
pip install streamlit stellar-sdk
```

3. Execute o Agente:
```bash
streamlit run app.py
```
