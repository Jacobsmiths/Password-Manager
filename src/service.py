import hashlib
import json
import os
import secrets


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# This class implements user class and aids in logic involing user applications
class UserService:
    def __init__(self, user):
        self.user_data_file_local = None
        self.user = user

    def checkUser(self):
        if (not os.path.exists(self.user.getFileLocal())):
            print("No user found")
            return False
        else:
            print("User found")
            return True

    def setUpUser(self, authService):
        if not os.path.exists(self.user.getFileLocal()):
            hashed_password, salt = authService.hashPassword(self.user.getPassword())
            with open(self.user.getFileLocal(), 'w') as f:
                user_data = {
                    "username": self.user.getUsername(),
                    "hashedPass": hashed_password,
                    "salt": salt,
                    "passwords": []
                }
                json.dump(user_data, f)
            print(f"User {self.user.getUsername()} created at {self.user.getFileLocal()}")
        else:
            print(f"User {self.user.getUsername()} already exists at {self.user.getFileLocal()}")


# this class aids in password/ encryption management and authentication
class AuthService:
    def __init__(self, user):
        self.user = user

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
    
    def verifyUser(self, passwrd, user_data_file_local):
        data = self.getUsrData(user_data_file_local)
        hashed_passwrd, salt = data['hashedPass'], data['salt']
        # self.verifyPassword(stored_password=hashed_passwrd, stored_salt=salt, provided_password=passwrd)
        return hashed_passwrd

    def getUsrData(self, user_data_file_local):
        if os.path.exists(user_data_file_local):
            with open(user_data_file_local, 'r') as f:
                user_data = json.load(f)
                return user_data
        else:
            print("No user data file found for user:")
            return None

# This is just a way to manage attributes of a user to communicate between service classes
# stores username, password and file location of user, all logic should not be held in this class
class User:
    def __init__(self, usr=None, password=None ,salt=None):
        self.username = usr
        self.password = password
        if(not self.username):
            user_data_file = '_'.join(self.username.split() + ['data.json'])
            self.user_data_file_local = os.path.join(DATA_DIR, user_data_file)

    def setUsername(self, username):
        self.username = username
        if(not self.username):
            user_data_file = '_'.join(self.username.split() + ['data.json'])
            self.user_data_file_local = os.path.join(DATA_DIR, user_data_file)

    def setPassword(self, password, salt):
        self.password = password
        self.salt = salt

    def getFileLocal(self):
        return self.user_data_file_local

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password