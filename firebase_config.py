import os
import firebase_admin
from firebase_admin import credentials, firestore

current_directory = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_directory, "lar-dorcas-dbaf9-firebase-adminsdk-3ie4l-d4b9e7a2ce.json")

cred = credentials.Certificate(json_path)
app = firebase_admin.initialize_app(cred)
db = firestore.client()
