from flask import Flask, request, jsonify
import json
from src.service import UserService

app = Flask(__name__)
userService = UserService()


@app.route('/verify_user', methods=['POST'])
def handle_data():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if(userService.checkUser(username)):
        if(userService.verifyUser(username, password)):
            return jsonify({'valid': True})
        else: 
            return jsonify({'valid': False, 'message': 'Password cannot be empty'}), 401
    else:
        return jsonify({'valid': False, 'message': 'Password cannot be empty'}), 404


# Example endpoint to get passwords
@app.route('/get_passwords', methods=['GET'])
def get_passwords():
    # Logic to read and decrypt passwords from your JSON file
    # Example:
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
    # Decrypt passwords if necessary
    return jsonify(passwords)

# Example endpoint to store a password
@app.route('/store_password', methods=['POST'])
def store_password():
    # Logic to receive encrypted password and store it in JSON
    # Example:
    data = request.get_json()
    with open('passwords.json', 'w') as f:
        json.dump(data, f)
    return 'Password stored successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)