from flask import Flask, request, jsonify
import sqlite3
import jwt
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

SECRET_KEY = "a_key"  # You can replace this with any secret key
@app.route('/token', methods=['POST'])
def get_token():
    service_account_number = request.json.get('service_account_number')
    if not service_account_number:
        return jsonify({"msg": "Service Account Number is required"}), 400

    # validate the service account number
    # this is a placeholder, replace it with your own validation logic
    if service_account_number != 'valid_service_account_number':
        return jsonify({"msg": "Invalid Service Account Number"}), 401

    # if validation passes, create a token and return it
    token = jwt.encode({"service_account_number": service_account_number}, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

@app.route('/terminals', methods=['GET'])
def get_terminals():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"msg": "Token is required"}), 400

    # split the auth_header as it will be of the form "Bearer <token>"
    token_parts = auth_header.split()
    if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
        return jsonify({"msg": "Token is malformed"}), 400
    token = token_parts[1]

    # validate the token
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Invalid token"}), 401


    # if token is valid, fetch all terminals and return them
    conn = sqlite3.connect('terminals.db')
    c = conn.cursor()
    c.execute('SELECT * FROM terminals')
    terminals = c.fetchall()
    conn.close()

    return jsonify({"terminals": terminals})

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)

