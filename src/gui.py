from tkinter import messagebox
import customtkinter as ctk
import service

ctk.set_appearance_mode("dark")

class app(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Jacob's Ultra Protected Password Manager")

        self.userService = service.UserService()

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {
            "InitialLoginFrame" : InitialLoginFrame(parent=self.container, controller=self, userService=self.userService),
        }
    
        self.current_frame = self.frames[InitialLoginFrame.__name__]
        self.current_frame.pack(expand=True, fill="both")

    def showFrame(self, frame):
        self.current_frame.pack_forget()
        self.current_frame = self.frames[frame.__name__]
        self.current_frame.pack(expand=True, fill="both")

    def addFrame(self, frame):
        self.frames[frame.__name__] = frame(parent=self.container, controller=self, userService=self.userService)

class InitialLoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, userService, **kwargs):
        super().__init__(parent, **kwargs)
        # self.pack(expand=True, fill="both")

        self.userService = userService
        self.controller = controller

        self.label = ctk.CTkLabel(self, text='Login',corner_radius=8, font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.usr_entry = ctk.CTkEntry(self, placeholder_text="Enter Username", height=35, width=150)
        self.usr_entry.pack(pady=3)

        self.pass_entry = ctk.CTkEntry(self,placeholder_text="Enter Password", height=35, width=150)
        self.pass_entry.pack(pady=3)

        self.submit_btn = ctk.CTkButton(self,text="Submit",command = self.retrieveUser, height=30, width=100)
        self.submit_btn.pack(pady=10)

    
    def retrieveUser(self):
        """Checks if user exists, if they don't then ask if they want to make new user. If the user does exists
            It compares passwords to gain access to account"""
        username = self.usr_entry.get()
        password = self.pass_entry.get()

        # checks if user exists using the userService class
        if(self.userService.checkUser(username)):
            if(self.userService.verifyUser(username, password)):
                print("correct Password")
                self.controller.addFrame(PasswordManagerContainer)
                self.controller.showFrame(PasswordManagerContainer)
                
            else: 
                print("incorrect password")
        else:
            response = messagebox.askyesno("No User Found", "Do you want to create a new user?")
            if response:
                self.userService.setUpUser(username, password)


class PasswordManagerContainer(ctk.CTkFrame):
    def __init__(self, parent, controller, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.userService = userService
        self.passwordDisplay = PasswordDisplayFrame(parent=self, userService=self.userService)
        self.passwordGenerator = PasswordGeneratorFrame(parent=self,userService=self.userService)
        self.passwordManager = PasswordManagerFrame(parent=self, userSerice=self.userService, width=450)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.passwordManager.grid(row=0, column=0, rowspan=3,sticky="nsw", padx= 5, pady=5)
        self.passwordDisplay.grid(row=0, column=1, rowspan=2, sticky="news", padx= 5, pady=5)
        self.passwordGenerator.grid(row=2, column=1, sticky="news", padx= 5, pady=5)
        self.passwordManager.propagate(False)
        self.passwordGenerator.propagate(True)
        self.passwordDisplay.propagate(False)
    
class PasswordDisplayFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        headers = ["Website", "Username", "Password"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self, text=header)
            label.grid(row=0, column=col, pady=10)
        
        entries = self.userService.getDisplayableData()
        for row, (website, username, password) in enumerate(entries, start=1):
            color = (lambda x: "#E0E0E0" if x % 2 == 0 else "#FFFFFF")(row)
            website_entry = ctk.CTkLabel(self, text=website, bg_color=color)
            website_entry.grid(row=row, column=0, padx=10, pady=5)
            username_entry = ctk.CTkLabel(self, text=username, bg_color=color)
            username_entry.grid(row=row, column=1, padx=10, pady=5)
            password_entry = ctk.CTkLabel(self, text=password, bg_color=color)
            password_entry.grid(row=row, column=2, padx=10, pady=5)
        


class PasswordGeneratorFrame(ctk.CTkFrame):
    def __init__(self,parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService
        self.label = ctk.CTkLabel(self, text="Password Generator")
        self.label.pack(expand=True, fill="both")

class PasswordManagerFrame(ctk.CTkFrame):
    def __init__(self, parent, userSerice, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userSerice

        self.label = ctk.CTkLabel(self,text="Manage Passwords")
        self.label.pack(expand=True, fill="both")


