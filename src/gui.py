from tkinter import messagebox
import customtkinter as ctk
import service

ctk.set_appearance_mode("dark")
Header1 = ("Helvetica", 25)
Header2 = ("Helvetica", 18, 'bold')
Text = ("Helvetica", 15)

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

        self.label = ctk.CTkLabel(self, text='Login',corner_radius=8, font=Header1)
        self.label.pack(pady=20)

        self.usr_entry = ctk.CTkEntry(self, placeholder_text="Enter Username", height=60, width=220, font=Text)
        self.usr_entry.pack(pady=3)

        self.pass_entry = ctk.CTkEntry(self,placeholder_text="Enter Password", height=60, width=220, font=Text)
        self.pass_entry.pack(pady=3)

        self.submit_btn = ctk.CTkButton(self,text="Submit",command = self.retrieveUser, height=60, width=200, font=Text)
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
        self.refresher = self.passwordDisplay.updateGrid

        self.passwordGenerator = PasswordGeneratorFrame(parent=self,userService=self.userService)
        self.passwordManager = PasswordManagerFrame(parent=self, userSerice=self.userService, passwordUpdated=self.refresher)

        self.grid_columnconfigure(0, weight=0, minsize=550)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.passwordManager.grid(row=0, column=0, rowspan=3, sticky="nesw", padx= 3, pady=3)
        self.passwordDisplay.grid(row=0, column=1, rowspan=2, sticky="news", padx= 3, pady=3)
        self.passwordGenerator.grid(row=2, column=1, sticky="news", padx= 3, pady=3)
        self.passwordManager.propagate(False)
        self.passwordGenerator.propagate(False)
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

        self.updateGrid()
    

    def updateGrid(self):
        entries = self.userService.getDisplayableData()
        for i in range(1, len(entries)):
            self.grid_rowconfigure(i, weight=0)

        for row, (website, username, password) in enumerate(entries, start=1):
            self.grid_rowconfigure(row, weight=0, )
            color = (lambda x: "#3A3B3C" if x % 2 == 0 else "transparent")(row)
            website_entry = ctk.CTkLabel(self, text=website, bg_color=color)
            website_entry.grid(row=row, column=0, sticky='nesw')
            username_entry = ctk.CTkLabel(self, text=username, bg_color=color)
            username_entry.grid(row=row, column=1, sticky='nesw')
            password_entry = ctk.CTkLabel(self, text=password, bg_color=color)
            password_entry.grid(row=row, column=2, sticky='nesw')



class PasswordGeneratorFrame(ctk.CTkFrame):
    def __init__(self,parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService
        self.label = ctk.CTkLabel(self, text="Password Generator", font=Text)
        self.label.pack(expand=True, fill="both")


class PasswordManagerFrame(ctk.CTkFrame):
    def __init__(self, parent, userSerice, passwordUpdated, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userSerice
        self.passwordUpdated = passwordUpdated
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.addpasswordFrame = AddPasswordFrame(self, self.userService, passwordUpdated=passwordUpdated, fg_color='transparent')
        self.deletePasswordFrame = DeletePasswordFrame(self, self.userService, passwordUpdated=passwordUpdated, fg_color='transparent')
        self.title = ctk.CTkLabel(self,text="Manage Passwords", font=Header1)
        
        self.addpasswordFrame.grid(row=1, column=0, padx=5, pady=10)
        self.deletePasswordFrame.grid(row=2, column=0,padx=5, pady=10)
        self.title.grid(row=0, column=0, padx=5, pady=10, sticky='ew')


class AddPasswordFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, passwordUpdated, **kwargs):
        super().__init__(parent,**kwargs)

        self.userService = userService
        self.passwordUpdated = passwordUpdated

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.addPasswordTitle = ctk.CTkLabel(self, text="Add Password", font=Header2)
        self.addPasswordTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.websiteLabel = ctk.CTkLabel(self, text="Website:", font=Text)
        self.websiteEntry = ctk.CTkEntry(self, placeholder_text="Website", font=Text)
        self.websiteLabel.grid(row=1, column=0, pady=5, sticky='ew', padx=(0, 10))
        self.websiteEntry.grid(row=1, column=1, pady=5, sticky='ew', padx=(10, 0))

        self.usernameLabel = ctk.CTkLabel(self, text="Username:", font=Text)
        self.usernameEntry = ctk.CTkEntry(self, placeholder_text="Username", font=Text)
        self.usernameLabel.grid(row=2, column=0, pady=5, sticky='ew', padx=(0, 10))
        self.usernameEntry.grid(row=2, column=1, pady=5, sticky='ew', padx=(10, 0))

        self.passwordLabel = ctk.CTkLabel(self, text="Password:", font=Text)
        self.passwordEntry = ctk.CTkEntry(self, placeholder_text="Password", font=Text)
        self.passwordLabel.grid(row=3, column=0, pady=5, sticky='ew', padx=(0, 10))
        self.passwordEntry.grid(row=3, column=1, pady=5, sticky='ew', padx=(10, 0))

        self.displayNameLabel = ctk.CTkLabel(self, text="Site Display:", font=Text)
        self.displayNameEntry = ctk.CTkEntry(self, placeholder_text="Display Name", font=Text)
        self.displayNameLabel.grid(row=4, column=0, pady=5, sticky='ew', padx=(0, 10))
        self.displayNameEntry.grid(row=4, column=1, pady=5, sticky='ew', padx=(10, 0))

        self.submitButton = ctk.CTkButton(self, text="Store Information",command=self.addPassword, font=Text)
        self.submitButton.grid(row=5, column=0, columnspan=2, padx=5, pady=15)

    def addPassword(self):
        username=self.usernameEntry.get()
        password=self.passwordEntry.get()
        website=self.websiteEntry.get()
        siteDisplay=self.displayNameEntry.get()
        self.userService.addPassword(username=username, password=password, website=website, webNickName=siteDisplay)
        self.usernameEntry.delete(0, ctk.END)
        self.passwordEntry.delete(0, ctk.END)
        self.websiteEntry.delete(0, ctk.END)
        self.displayNameEntry.delete(0, ctk.END)
        self.passwordUpdated()


class DeletePasswordFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, passwordUpdated, **kwargs):
        super().__init__(parent,**kwargs)
        self.userService = userService
        self.passwordUpdated = passwordUpdated

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.deletePasswordTitle = ctk.CTkLabel(self, text="Delete Password", font=Header2)
        self.deletePasswordTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.websiteLabel = ctk.CTkLabel(self, text="Enter Site to Delete:", font=Text)
        self.websiteEntry = ctk.CTkEntry(self, placeholder_text="URL or Display Name", font=Text, width=200)
        self.websiteLabel.grid(row=1,column=0, pady=5, sticky='ew', padx=(0, 10))
        self.websiteEntry.grid(row=1, column=1, pady=5, sticky='ew', padx=(10, 0))

        self.deleteButton = ctk.CTkButton(self, text="Delete", command=self.deletePassword, font=Text)
        self.deleteButton.grid(row=2, column=0, columnspan=2, padx=5, pady=10)


    def deletePassword(self):
        entryToDelete = self.websiteEntry.get()
        self.userService.deletePassword(entryToDelete=entryToDelete)
        self.websiteEntry.delete(0, ctk.END)
        self.passwordUpdated()




