from tkinter import messagebox
import customtkinter as ctk
import service

ctk.set_appearance_mode("dark")

class app(ctk.CTk):
    def __init__(self, userService, authService, user):
        super().__init__()
        self.geometry("1000x600")
        self.title("Jacob's Ultra Protected Password Manager")

        self.userService = userService
        self.authService = authService
        self.user = user

        self.current_frame = initialLoginFrame(self,self.userService, self.authService, self.user)

        self.mainloop()
        

class initialLoginFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, authService, user, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(expand=True, fill="both")

        self.userService = userService
        self.authService = authService
        self.user = user

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
        
        if(self.user.password):
            self.user.setUsername(self.usr_entry.get())
            self.user.setPassword(self.authService(self.pass_entry.get()))

        # checks if user exists using the userService class
        if(self.userService.checkUser(self.user.username)):
            self.authService.verifyUser(self.user.passowrd, self.userService.user_data_file_local)
        else:
            response = messagebox.askyesno("No User Found", "Do you want to create a new user?")
            if response:
                self.userService.setUpUser(usr, passwrd, self.authService)


class newUserFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService
        self.pack(expand=True, fill="Both")

        
