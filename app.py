import sqlite3
from flask import Flask, request, jsonify
from jose import jwt

app = Flask(__name__)

@app.route('/token', methods=['POST'])
def get_token():
    service_account_number = request.json.get('service_account_number')
    if not service_account_number:
        return jsonify({"msg": "Service Account Number is required"}), 400

    # validate the service account number
    conn = sqlite3.connect('terminals.db')
    c = conn.cursor()
    c.execute('SELECT * FROM service_accounts WHERE service_account_number = ?', (service_account_number,))
    account = c.fetchone()
    conn.close()

    if not account:
        return jsonify({"msg": "Invalid Service Account Number"}), 401

    # if validation passes, create a token and return it
    # use the secret from the service_accounts table to sign the token
    secret_key = account[1]  # Assuming secret is the second field in the table
    token = jwt.encode({"service_account_number": service_account_number}, secret_key, algorithm="HS256")
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
    # first, we need to fetch the associated secret_key
    unverified_claims = jwt.get_unverified_claims(token)
    service_account_number = unverified_claims.get("service_account_number")
    conn = sqlite3.connect('terminals.db')
    c = conn.cursor()
    c.execute('SELECT * FROM service_accounts WHERE service_account_number = ?', (service_account_number,))
    account = c.fetchone()
    if not account:
        return jsonify({"msg": "Invalid Service Account Number"}), 401

    secret_key = account[1]  # Assuming secret is the second field in the table

    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.JWTError:
        return jsonify({"msg": "Invalid token"}), 401

    # if token is valid, fetch all terminals and return them
    conn = sqlite3.connect('terminals.db')
    c = conn.cursor()
    c.execute('SELECT * FROM terminals')
    terminals = [dict((c.description[i][0], value) \
               for i, value in enumerate(row)) for row in c.fetchall()]
    conn.close()

    return jsonify({"terminals": terminals})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
