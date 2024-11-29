from datetime import datetime
from flask import Flask, request, jsonify
from email_validator import validate_email, EmailNotValidError
from flask_cors import CORS
from validate_docbr import CPF
import uuid
import random

from services.payment_systems import PaymentSystems

app = Flask(__name__)


app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://lardorcas.web.app",
                "https://firego-82472.web.app",
                "http://localhost:5173",
                "http://localhost:5174",
                "http://localhost:4000",
            ]
        }
    },
)

def gerar_codigo_pix(amount):
    identificador = str(uuid.uuid4()).replace('-', '')[:20]
    valor_formatado = f"{amount:.2f}".replace('.', '')
    codigo_pix = f"00020126330014BR.GOV.BCB.PIX01145204000053039865404{valor_formatado}5802BR5913Nome do Estabelecimento6009SAO PAULO62070503{identificador}"
    return codigo_pix

def processar_pagamento_cartao(numero_cartao, validade, cvv, valor):
    if random.choice([True, False]):
        transacao_id = str(uuid.uuid4())
        return {
            "status": "Aprovado",
            "transacao_id": transacao_id,
            "valor": valor
        }
    else:
        return {
            "status": "Recusado",
            "motivo": "Transação não autorizada"
        }


@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/', methods=['POST', 'GET'])
def create_user():    
    return jsonify({
        "time": datetime.now().isoformat(),  
        "message": "Hello World!!!"          
    }), 201


def validar_cpf(cpf):
    cpf_obj = CPF()
    return cpf_obj.validate(cpf)

def validar_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

@app.route('/payment', methods=['POST'])
def generatePayment():
    try:
        data = request.json

        if 'name' not in data or 'email' not in data or 'cpf' not in data or 'amount' not in data or 'id_ref' not in data:
            return jsonify({"error": "Dados ausentes"}), 400

        cpf = data['cpf']
        name = data['name']
        email = data['email']
        value = data['amount']

        if not validar_cpf(cpf):
            return jsonify({"error": "CPF inválido"}), 400

        if not validar_email(email):
            return jsonify({"error": "E-mail inválido"}), 400
        

        classPay = PaymentSystems()
        response = classPay.gerar_pix({
                "cliente":{
                    "dataNascimento": "1993-12-16",
                    "nome": name,
                    "email": email,
                    "celular":"63987222161",
                    "cpf": cpf,
                    "clienteId":51594277
                },
                "descricao": data.get("id_ref"),
                "endereco":{
                    "cep":"69915-846",
                    "cidade":"Rio Branco",
                    "estado":"AC",
                    "logradouro":"Rua Projetada 1029",
                    "numero":892
                },
                "estabelecimentoId":158811,
                "tipoPagamentoId":5,
                "valor": value
            })

        return jsonify({"pix": response["pedido"]["qrCodePix"]})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Houve um erro para gerar pagamento, tente novamente mais tarde"}), 500

@app.route('/demo-criar-pagamento', methods=['POST'])
def demo_criar_pagamento():
    data = request.get_json()

    if 'name' not in data or 'email' not in data or 'cpf' not in data or 'amount' not in data or 'id_ref' not in data:
            return jsonify({"error": "Dados ausentes"}), 400

    cpf = data['cpf']
    name = data['name']
    email = data['email']
    value = data['amount']

    if not validar_cpf(cpf):
        return jsonify({"error": "CPF inválido"}), 400

    if not validar_email(email):
        return jsonify({"error": "E-mail inválido"}), 400

    codigo_pix = gerar_codigo_pix(value)

    return jsonify({
        "mensagem": "Pagamento Pix criado com sucesso.",
        "pix": codigo_pix,
        "amount": value
    }), 201


@app.route('/demo-criar-pagamento-cartao', methods=['POST'])
def criar_pagamento_cartao():
    dados = request.get_json()

    numero_cartao = dados.get('numero_cartao')
    validade = dados.get('validade')
    cvv = dados.get('cvv')
    valor = dados.get('amount')

    if not numero_cartao or not validade or not cvv or not valor:
        return jsonify({"erro": "Todos os dados do cartão e o valor são obrigatórios"}), 400

    resultado = processar_pagamento_cartao(numero_cartao, validade, cvv, valor)

    if resultado["status"] == "Aprovado":
        return jsonify({
            "mensagem": "Pagamento com cartão aprovado.",
            "transacao_id": resultado["transacao_id"],
            "valor": resultado["valor"]
        }), 201
    else:
        return jsonify({
            "mensagem": "Pagamento recusado.",
            "motivo": resultado["motivo"]
        }), 402