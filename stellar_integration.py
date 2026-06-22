import time
from stellar_sdk import Keypair

def create_stellar_wallet():
    """Gera um novo par de chaves (pública e privada) na rede Stellar."""
    keypair = Keypair.random()
    return keypair.public_key, keypair.secret

def fund_wallet_with_friendbot(public_key):
    """
    Simula o Friendbot adicionando 10.000 XLM na Testnet.
    (No MVP usaremos tempo de espera simulado para ser mais rápido e confiável no vídeo).
    """
    time.sleep(1) # Simula delay de rede
    return True

def simulate_microcredit_loan(amount):
    """
    Simula a execução do Smart Contract (Soroban) e liberação de crédito USDC/XLM.
    """
    time.sleep(2) # Simula o processamento do contrato RWA na Blockchain
    return True
