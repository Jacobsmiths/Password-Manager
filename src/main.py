import json
import os
from gui import app
import service


user_service = service.UserService()
auth_service = service.AuthService()
app = app(user_service, auth_service)

app.mainloop()