from email_validator import validate_email, EmailNotValidError
from validate_docbr import CPF

def validar_cpf(cpf):
    cpf_obj = CPF()
    return cpf_obj.validate(cpf)

def validar_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False