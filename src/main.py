import json
import os
from gui import app
import service

user = service.User()
user_service = service.UserService(user)
auth_service = service.AuthService(user)
app = app(user_service, auth_service, user)