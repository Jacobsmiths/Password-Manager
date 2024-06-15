from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")

class app(ctk.CTk):
    def __init__(self, userService, authService):
        super().__init__()
        self.geometry("1000x600")
        self.title("Jacob's Ultra Protected Password Manager")

        self.userService = userService
        self.authService = authService

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {
            "initialLoginFrame" : initialLoginFrame(parent=container, controller=self, userService=self.userService, authService=self.authService),
            "passwordDisplayFrame": passwordDisplayFrame(parent=container, userService=self.userService)
        }
    

        self.current_frame = self.frames[initialLoginFrame.__name__]
        self.current_frame.pack(expand=True, fill="both")

    def showFrame(self, frame):
        self.current_frame.pack_forget()
        self.current_frame = self.frames[frame.__name__]
        self.current_frame.pack(expand=True, fill="both")
       
        

class initialLoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, userService, authService, **kwargs):
        super().__init__(parent, **kwargs)
        # self.pack(expand=True, fill="both")

        self.userService = userService
        self.authService = authService
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
            if(self.authService.verifyUser(username, password)):
                print("correct Password")
                self.controller.showFrame(passwordDisplayFrame)
                
            else: 
                print("incorrect password")
        else:
            response = messagebox.askyesno("No User Found", "Do you want to create a new user?")
            if response:
                self.userService.setUpUser(username, password, self.authService)


class passwordDisplayFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        # self.pack(expand=True, fill="both")

        self.userService = userService

        self.lab = ctk.CTkLabel(self, text='FART!!!!!',corner_radius=8, font=("Helvetica", 20))
        self.lab.pack()

        
