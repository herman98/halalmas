import json
from datetime import datetime
# from jwcrypto import jwt, jwk
# from jose import jwt

# class Token:
#     def __init__(self, payload):
#         self.payload = payload
#         self.algorithm = 'oct'
#         self.header = {"alg": "HS256"}

#     def get_date_string(self, add=None):
#         now = datetime.now()
#         month = now.month
#         if add:
#             month += 1

#         date = datetime(
#             now.year,
#             now.month,
#             now.day)
#         return date.strftime('%m-%d-%Y')

#     def generate_key(self):
#         key = jwk.JWK(generate=self.algorithm, size=256)
#         return key

#     def generate_token_register(self):
#         self.payload['date_generate'] = self.get_date_string()
#         self.payload['date_expired'] = self.get_date_string(True)
#         key = json.loads(self.generate_key().export())['k']
#         token = jwt.encode(self.payload, key, algorithm='HS256')

#         return token, key


#     def verify_token_register(self):

#         decode = jwt.decode(self.payload['token'], self.payload['key'], algorithms=['HS256'])
#         return True, decode
