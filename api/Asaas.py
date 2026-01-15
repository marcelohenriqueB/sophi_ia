
URL_ASAAS = 'https://sandbox.asaas.com/api/v3'
from users.models import Client
import requests

class Asaas: 
    def __init__(self, client: Client):
        self.api_key = client.config_viagem.token_asaas if client.config_viagem else None
        
        self.headers = {
            'access_token': self.api_key,
            'Content-Type': 'application/json'
        }
        
    def create_customer(self, nome, email, telefone, cpf_cnpj=None):
        url = f"{URL_ASAAS}/customers"
        payload = {
            "name": nome,
            "email": email,
            "phone": telefone,
            "cpfCnpj": cpf_cnpj
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def criar_cobranca_pix(self, customer_id, valor, descricao, vencimento):
        url = f"{URL_ASAAS}/payments"
        payload = {
            "customer": customer_id,
            "value": valor,
            "description": descricao,
            "dueDate": vencimento,
            "billingType": "PIX"
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def link_cobranca(self, cobranca_id):
        url = f"{URL_ASAAS}/payments/{cobranca_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def pixQrCode(self, cobranca_id):
        url = f"{URL_ASAAS}/payments/{cobranca_id}/pixQrCode"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    