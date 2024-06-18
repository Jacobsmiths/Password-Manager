import hashlib
import json
import os
import secrets
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# This class implements user class and aids in logic involing user applications
class UserService():
    def __init__(self):
        self.username = None
        self.user_data_file_local = None

    def setUsername(self, username):
        self.username = username
        self.user_data_file_local = os.path.join(DATA_DIR, '_'.join(username.split() + ['data.json']))

    def checkUser(self, username):
        self.setUsername(username=username)
        if (not os.path.exists(self.user_data_file_local)):
            print("No user found")
            return False
        else:
            print("User found")
            return True

    def setUpUser(self, username, passwordInput):
        if(not self.user_data_file_local):
            self.setUsername(username=username)

        if not os.path.exists(self.user_data_file_local):
            hashed_password, salt = self.hashPassword(passwordInput)
            with open(self.user_data_file_local, 'w') as f:
                user_data = {
                    "username": username,
                    "hashedPass": hashed_password,
                    "salt": salt,
                    "passwords": []
                }
                json.dump(user_data, f)
            print(f"User created")
        else:
            print(f"User already exists")

        
    def addPassword(self, username, password, website, webNickName=None):
        """ This method is called when you want to update or add a password to be stored"""
        data = self.getData(self.user_data_file_local)
        passwords = data.get("passwords")

        for entry in passwords:
            if entry.get('website') == website:
                entry['password'] = password
                entry['webNickName'] = webNickName
                entry['username'] = username
                break
            else:
                passwords.append({"website": website, "username":username, "password": password, "webNickName": webNickName})

        data["passwords"] = passwords
        with open(self.user_data_file_local, 'w') as f:
            json.dump(data, f)


    def getDisplayableData(self):
        data = self.getData()
        passwords = data.get("passwords")
        display = []
        for i in passwords:
            if(i["webNickName"]):
                display.append((i['webNickName'],i['username'], i['password']))
            else:
                display.append((i['website'],i['username'], i['password']))
        return display


    def getData(self):
        try:
            with open(file=self.user_data_file_local, mode='r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None
        

    def hashPassword(self, password):
        #this generates a salt used to add onto the end of passwords and this creats a 16 byte in hex (32 digits of hex)
        salt = secrets.token_hex(16)
        #this retrieves the hashed password
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return hashed_password, salt

    def verifyPassword(self, stored_password, stored_salt, provided_password):
        hashed_provided_password = hashlib.sha256((provided_password + stored_salt).encode('utf-8')).hexdigest()
        return stored_password == hashed_provided_password
    
    def verifyUser(self, username, passwrd):
        self.setUsername(username=username)
        data = self.getData()
        hashed_passwrd, salt = data['hashedPass'], data['salt']
        return self.verifyPassword(stored_password=hashed_passwrd, stored_salt=salt, provided_password=passwrd)
        

    def deriveKey(masterKey, salt):
        kdf = PBKDF2HMAC(
            algorithm= hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000
        )
        return kdf.derive(masterKey)

    def encrypt(key, valueToEncrypt):
        f = Fernet(key)
        encryptedKey = f.encrypt(valueToEncrypt.encode())
        return encryptedKey

    def decrypt(key, encryptedKey):
        f = Fernet(key)
        try:
            return f.decrypt(encryptedKey)
        except InvalidToken:
            return b''