import uuid
import random

class DemoPay:
    def generate_pix(self, data):
        identifier = str(uuid.uuid4()).replace('-', '')[:20]
        formatted_value = f"{data['amount']:.2f}".replace('.', '')
        transaction_id = str(uuid.uuid4())
        pix_code = f"00020126330014BR.GOV.BCB.PIX01145204000053039865404{formatted_value}5802BR5913Store Name6009SAO PAULO62070503{identifier}"
        return {"code": pix_code, "transaction_id": transaction_id}
    
    def process_card_payment(self, card_number, expiration_date, cvv, amount):
        if random.choice([True, False]):
            transaction_id = str(uuid.uuid4())
            return {
                "status": "Approved",
                "transaction_id": transaction_id,
                "amount": amount
            }
        else:
            raise ValueError("Transaction not authorized")
