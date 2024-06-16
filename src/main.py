import json
import os
from gui import app
import service


user_service = service.UserService()
app = app(user_service)

app.mainloop()