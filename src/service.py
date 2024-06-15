import hashlib
import json
import os
import secrets


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')



# This class implements user class and aids in logic involing user applications
class UserService:
    def __init__(self):
        self.user_data_file_local = None

    def checkUser(self, username):
        user_data_file = '_'.join(username.split() + ['data.json'])
        self.user_data_file_local = os.path.join(DATA_DIR, user_data_file)
        if (not os.path.exists(self.user_data_file_local)):
            print("No user found")
            return False
        else:
            print("User found")
            return True

    def setUpUser(self, username, passwordInput, authService):
        if(not self.user_data_file_local):
            user_data_file = '_'.join(username.split() + ['data.json'])
            self.user_data_file_local = os.path.join(DATA_DIR, user_data_file)

        if not os.path.exists(self.user_data_file_local):
            hashed_password, salt = authService.hashPassword(passwordInput)
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


# this class aids in password/ encryption management and authentication
class AuthService:
    def __init__(self):
        self.user_data_file_local = None

    def hashPassword(self, password):
        #this generates a salt used to add onto the end of passwords and this creats a 16 byte in hex (32 digits of hex)
        salt = secrets.token_hex(16)
        #this retrieves the hashed password
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return hashed_password, salt

    def verifyPassword(self, stored_password, stored_salt, provided_password):
        #this unhase
        hashed_provided_password = hashlib.sha256((provided_password + stored_salt).encode('utf-8')).hexdigest()
        return stored_password == hashed_provided_password
    
    def verifyUser(self, username, passwrd):
        user_data_file = '_'.join(username.split() + ['data.json'])
        self.user_data_file_local = os.path.join(DATA_DIR, user_data_file)
        data = self.getUsrData()
        hashed_passwrd, salt = data['hashedPass'], data['salt']
        return self.verifyPassword(stored_password=hashed_passwrd, stored_salt=salt, provided_password=passwrd)

    def getUsrData(self):
        if os.path.exists(self.user_data_file_local):
            with open(self.user_data_file_local, 'r') as f:
                user_data = json.load(f)
                return user_data
        else:
            print("No user data file found for user:")
            return None
