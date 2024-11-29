from datetime import datetime
from flask import Flask, request, jsonify
from email_validator import validate_email, EmailNotValidError
from flask_cors import CORS
from validate_docbr import CPF

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
