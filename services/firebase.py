from firebase_config import db

def get_payment(payment_id):
    try:
        ref = db.collection("payments").document(payment_id)
        data = ref.get()
        if data.exists:
            return data.to_dict()
        else:
            return {"error": "Data not found"}
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


def update_payment(payment_id, updated_data):
    try:
        ref = db.collection("payments").document(payment_id)
        ref.update(updated_data)
        return {"message": "Payment updated successfully", "payment_id": payment_id}
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
