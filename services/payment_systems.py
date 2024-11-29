import requests
import time

ESTABELECIMENTO_ID_ZIX=46415
BASE_URL_ZIX="https://api.zsystems.com.br/"
BASE_EMAIL_ZIX="dimmycarter@zixpay.com.br"
BASE_PASSWORD_ZIX="Zixpay1281@"

class PaymentSystems:

    def __init__(self):
        self.token = None

    def login(self):
        """
        Realiza o login na API e obtém o token de autenticação.
        """
        login_url = f"{BASE_URL_ZIX}createToken"
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(login_url, json={
            'email': BASE_EMAIL_ZIX,
            'password': BASE_PASSWORD_ZIX
        }, headers=headers)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data['token']
        else:
            raise Exception("Falha no login, verifique suas credenciais.")

    
    def gerar_pagamento_cartao(self, payment_data):
        ...

    def generate_pix(self, payment_data):
        """
        Processa o pagamento utilizando a API.
        """
        self.login()
        
        payment_url = f"{BASE_URL_ZIX}vendas"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        }

        response = requests.post(payment_url, json=payment_data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao processar pagamento: {response.status_code}, {response.text}")