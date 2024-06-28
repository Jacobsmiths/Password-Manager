import hashlib
import json
import os
import secrets
import base64
import string
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import csv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# This class implements user class and aids in logic involing user applications
class UserService():
    def __init__(self):
        self.username = None
        self.user_data_file_local = None
        self.masterKey = None


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


    def verifyUser(self, username, passwrd):
        self.setUsername(username=username)
        data = self.getData()
        hashed_passwrd, salt = data['hashedPass'], data['salt']
        if(self.verifyPassword(stored_password=hashed_passwrd, stored_salt=salt, provided_password=passwrd)):
            self.masterKey = self.deriveKey(passwrd, salt=bytes.fromhex(salt))
            return True
        else:
            return False
    

    def setUpUser(self, username, passwordInput): # TODO is create key when given password
        if(not self.user_data_file_local):
            self.setUsername(username=username)
        hashed_password, salt = self.hashPassword(passwordInput)
        self.masterKey = self.deriveKey(passwordInput, salt=bytes.fromhex(salt))
        if not os.path.exists(self.user_data_file_local):
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
        data = self.getData()
        passwords = data.get("passwords",[])
        passwordToStore = self.encrypt(self.masterKey, valueToEncrypt=password)
        
        for entry in passwords:
            if entry.get('website') == website:
                entry['password'] = passwordToStore
                entry['webNickName'] = webNickName
                entry['username'] = username
                break
        else:
            passwords.append({"website": website, "username": username, "password": passwordToStore, "webNickName": webNickName})

        with open(self.user_data_file_local, 'w') as f:
            data["passwords"] = passwords
            json.dump(data, f)
        print("Stuff stored")
        
        
    def deletePassword(self, entryToDelete, getSelected):
        data = self.getData()
        selectedList = getSelected
        passwords = data.get('passwords')
        
        if(entryToDelete is not None):
            for entry in passwords:
                if (entry.get('website') == entryToDelete or entry.get('webNickName') == entryToDelete):
                    passwords.remove(entry)
                    break
        if(selectedList is not None):
            for i in list(selectedList[::-1]):
                del passwords[i]
        with open(self.user_data_file_local, 'w') as f:
            data['passwords'] = passwords
            json.dump(data, f)


    def getDisplayableData(self):
        data = self.getData()
        passwords = data.get("passwords")
        display = []
        for i in passwords:
            if(i["webNickName"]):
                display.append((i['webNickName'],i['username'], self.decrypt(self.masterKey,i['password'])))
            else:
                display.append((i['website'],i['username'], self.decrypt(self.masterKey,i['password'])))
        return display
    
    def searchInfo(self, wanted):
        data = self.getData()
        passwords = data.get("passwords")
        if(wanted[-3:] == "..."):
            wanted = wanted[:-3]
        for entry in passwords:
            if(entry['webNickName'] is None):
                if(wanted in entry['website']):
                    return (entry['username'], self.decrypt(self.masterKey,entry['password']), entry['website'])
            elif(wanted in entry['webNickName'] or wanted in entry['website']):
                return (entry['username'], self.decrypt(self.masterKey,entry['password']), entry['website'])


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


    def deriveKey(self, masterPass, salt):
        kdf = PBKDF2HMAC(
            algorithm= hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(masterPass.encode()))
        return key

    def encrypt(self, key, valueToEncrypt):
        f = Fernet(key)
        encryptedValue = f.encrypt(valueToEncrypt.encode())
        return encryptedValue.hex()

    def decrypt(self, key, valueToDecrypt):
        f = Fernet(key)
        valueAsBytes = bytes.fromhex(valueToDecrypt)
        return f.decrypt(valueAsBytes).decode('utf-8')
    
    def generatePassword(self, start='', end='', lengthIn=14):
        alphabet = string.ascii_letters + string.digits + "!#$%^.'/?&*()_-"
        length = lengthIn - len(start) - len(end)
        password = start + ''.join(secrets.choice(alphabet) for _ in range(length)) + end
        return password
        
    def importData(self, file_path):
        credentials = []
        try:
            with open(file_path, newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader) 
                for row in csvreader:
                    if len(row) >= 4:
                        website = row[1]
                        username = row[2]
                        password = row[3]
                        credentials.append((username, password, website))
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        
        for (username, password, website) in credentials:
            self.addPassword(username=username, website=website, password=password)