from flask import Flask, request, jsonify
from flask_cors import CORS
from services.demo_pay import DemoPay
from services.payment_systems import PaymentSystems
from services.validators import validar_cpf, validar_email
from datetime import datetime

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/*": {"origins": ["https://lardorcas.web.app", "http://localhost:5173"]}})

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

# --------------------------------------------------------------------------------------------------------- #

@app.route('/demo-payment-pix', methods=['POST'])
def generate_payment_pix_demo():
    try:
        data = request.json
        required_fields = ['name', 'email', 'cpf', 'amount', 'id_ref']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Dados ausentes"}), 400

        cpf, name, email, amount = data['cpf'], data['name'], data['email'], data['amount']

        if not validar_cpf(cpf) or not validar_email(email):
            return jsonify({"error": "CPF inválido ou E-mail inválido"}), 400

        payment__ = DemoPay()
        response = payment__.generate_pix({
            "amount": amount
        })

        return jsonify({"pix": response["code"]})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Erro ao gerar pagamento"}), 500


# --------------------------------------------------------------------------------------------------------- #


@app.route('/demo-payment-card', methods=['POST'])
def generate_payment_boleto_demo():
    try:
        data = request.json
        required_fields = ['name', 'card_number', 'expiration_date', 'cvv', 'amount', 'id_ref']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Dados ausentes"}), 400

        card_number, name, expiration_date, amount, cvv = data['card_number'], data['name'], data['expiration_date'], data['amount'], data['cvv']

        payment__ = DemoPay()
        response = payment__.process_card_payment(
            card_number, 
            expiration_date, 
            cvv, 
            amount
        )

        return jsonify({"card": response})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Erro ao gerar pagamento"}), 500

# --------------------------------------------------------------------------------------------------------- #


@app.route('/payment-systems-payment-pix', methods=['POST'])
def generate_payment_pix():
    try:
        data = request.json
        required_fields = ['name', 'email', 'cpf', 'amount', 'id_ref']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Dados ausentes"}), 400

        cpf, name, email, amount = data['cpf'], data['name'], data['email'], data['amount']

        if not validar_cpf(cpf) or not validar_email(email):
            return jsonify({"error": "CPF inválido ou E-mail inválido"}), 400

        payment__ = PaymentSystems()
        response = payment__.generate_pix({
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
                "valor": amount
            })

        return jsonify({"pix": response["code"]})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Erro ao gerar pagamento"}), 500



# @app.route('/payment', methods=['POST'])
# def generatePayment():
#     try:
#         data = request.json

#         if 'name' not in data or 'email' not in data or 'cpf' not in data or 'amount' not in data or 'id_ref' not in data:
#             return jsonify({"error": "Dados ausentes"}), 400

#         cpf = data['cpf']
#         name = data['name']
#         email = data['email']
#         value = data['amount']

#         if not validar_cpf(cpf):
#             return jsonify({"error": "CPF inválido"}), 400

#         if not validar_email(email):
#             return jsonify({"error": "E-mail inválido"}), 400
        

#         classPay = PaymentSystems()
#         response = classPay.gerar_pix
# ({
#                 "cliente":{
#                     "dataNascimento": "1993-12-16",
#                     "nome": name,
#                     "email": email,
#                     "celular":"63987222161",
#                     "cpf": cpf,
#                     "clienteId":51594277
#                 },
#                 "descricao": data.get("id_ref"),
#                 "endereco":{
#                     "cep":"69915-846",
#                     "cidade":"Rio Branco",
#                     "estado":"AC",
#                     "logradouro":"Rua Projetada 1029",
#                     "numero":892
#                 },
#                 "estabelecimentoId":158811,
#                 "tipoPagamentoId":5,
#                 "valor": value
#             })

#         return jsonify({"pix": response["pedido"]["qrCodePix"]})
#     except Exception as e:
#         return jsonify({"error": str(e), "message": "Houve um erro para gerar pagamento, tente novamente mais tarde"}), 500

# @app.route('/demo-criar-pagamento', methods=['POST'])
# def demo_criar_pagamento():
#     data = request.get_json()

#     if 'name' not in data or 'email' not in data or 'cpf' not in data or 'amount' not in data or 'id_ref' not in data:
#             return jsonify({"error": "Dados ausentes"}), 400

#     cpf = data['cpf']
#     name = data['name']
#     email = data['email']
#     value = data['amount']

#     if not validar_cpf(cpf):
#         return jsonify({"error": "CPF inválido"}), 400

#     if not validar_email(email):
#         return jsonify({"error": "E-mail inválido"}), 400

#     codigo_pix = gerar_codigo_pix(value)

#     return jsonify({
#         "mensagem": "Pagamento Pix criado com sucesso.",
#         "pix": codigo_pix,
#         "amount": value
#     }), 201


# @app.route('/demo-criar-pagamento-cartao', methods=['POST'])
# def criar_pagamento_cartao():
#     dados = request.get_json()

#     numero_cartao = dados.get('numero_cartao')
#     validade = dados.get('validade')
#     cvv = dados.get('cvv')
#     valor = dados.get('amount')

#     if not numero_cartao or not validade or not cvv or not valor:
#         return jsonify({"erro": "Todos os dados do cartão e o valor são obrigatórios"}), 400

#     resultado = processar_pagamento_cartao(numero_cartao, validade, cvv, valor)

#     if resultado["status"] == "Aprovado":
#         return jsonify({
#             "mensagem": "Pagamento com cartão aprovado.",
#             "transacao_id": resultado["transacao_id"],
#             "valor": resultado["valor"]
#         }), 201
#     else:
#         return jsonify({
#             "mensagem": "Pagamento recusado.",
#             "motivo": resultado["motivo"]
#         }), 402