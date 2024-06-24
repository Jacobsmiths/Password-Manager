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
        self.geometry("1300x800")
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

        self.passwordDisplay = PasswordScrollableFrame(parent=self, userService=self.userService)
        self.refresher = self.passwordDisplay.getUpdateMethod()
        self.getSelected = self.passwordDisplay.getSelectedMethod()

        self.passwordGenerator = PasswordGeneratorFrame(parent=self,userService=self.userService)
        self.passwordManager = PasswordManagerFrame(parent=self, userSerice=self.userService, passwordUpdated=self.refresher, getSelected=self.getSelected)

        self.grid_columnconfigure(0, weight=0, minsize=500)
        self.grid_columnconfigure(1, weight=0, minsize= 400)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1, minsize=100)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.passwordManager.grid(row=0, column=0, rowspan=3, sticky="nesw", padx= 3, pady=3)
        self.passwordDisplay.grid(row=0, column=1, rowspan=2, columnspan=2, sticky="news", padx= 3, pady=3)
        self.passwordGenerator.grid(row=2, column=1, sticky="news", padx= 3, pady=3)
        self.passwordManager.propagate(False)
        self.passwordGenerator.propagate(False)
        self.passwordDisplay.propagate(False)


class PasswordScrollableFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService

        # Create a canvas
        self.canvas = ctk.CTkCanvas(self, bd=0, highlightthickness=0, bg='#2B2B2B')
        self.canvas.pack(side='left', fill='both', expand=True)

        # Create a frame inside the canvas
        self.scrollable_frame = PasswordDisplayFrame(self.canvas, self.userService)
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Add a CTkScrollbar
        self.scrollbar = ctk.CTkScrollbar(self, orientation='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind the canvas scroll event
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        # Bind mousewheel events for different platforms
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def on_frame_configure(self, event=None):
        # Update scroll region to match the size of the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event=None):
        # Resize the inner frame to match the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.scrollable_frame_id, width=canvas_width)
        # Ensure the height is updated to match the content
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units") 
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def getUpdateMethod(self):
        return self.scrollable_frame.updateGrid
    
    def getSelectedMethod(self):
        return self.scrollable_frame.getSelectedCheckBoxes
    

class PasswordDisplayFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService
        self.updateGrid()
        
    
    def updateGrid(self):
        for widget in self.winfo_children():
            widget.grid_remove()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0, minsize=30)
        self.grid_columnconfigure(4, weight=0, minsize=10)
        self.grid_rowconfigure(0, weight=0)

        headers = ["Website", "Username", "Password"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self, text=header, font=Header2)
            label.grid(row=0, column=col, pady=15, sticky="new")

        checkAll = ctk.CTkLabel(self, text="Select\nAll")
        checkAll.grid(row=0, column=3, sticky='w', padx=(0, 10))
    
        self.masterVar = ctk.StringVar(value="off")
        checks = ctk.CTkCheckBox(self, variable=self.masterVar, width=10, onvalue='on', offvalue="off", text='', corner_radius=2, command=self.selectAll)
        checks.grid(row=0, column=4, sticky='news')

        self.entries = self.userService.getDisplayableData()
        self.checkboxes = []

        for row, (website, username, password) in enumerate(self.entries, start=1):
            self.grid_rowconfigure(row, weight=0)
            web=self.truncateText(website)
            color = (lambda x: "transparent" if x % 2 == 0 else "#3A3B3C")(row)
            webVar = ctk.StringVar(self, value=web)
            userVar = ctk.StringVar(self, value=username)
            passVar = ctk.StringVar(self, value=password)
            website_entry = ctk.CTkEntry(self, textvariable=webVar, font=Text, state='readonly', border_width=0, corner_radius=0, fg_color=color, bg_color=color, justify=ctk.CENTER)
            website_entry.grid(row=row, column=0, sticky='nesw')
            username_entry = ctk.CTkEntry(self, textvariable=userVar, font=Text, state='readonly', border_width=0, corner_radius=0, fg_color=color, bg_color=color, justify=ctk.CENTER)
            username_entry.grid(row=row, column=1, sticky='nesw')
            password_entry = ctk.CTkEntry(self, textvariable=passVar, font=Text, state='readonly', border_width=0, corner_radius=0, fg_color=color, bg_color=color, justify=ctk.CENTER)
            password_entry.grid(row=row, column=2, sticky='nesw')
            blank = ctk.CTkLabel(self, text='', bg_color=color)
            blank.grid(row=row, column=3, sticky='news')
            var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(self, variable=var, width=10, onvalue="on", offvalue="off", bg_color=color, text='', corner_radius=2)
            checkbox.grid(row=row, column=4, sticky='news')
            self.checkboxes.append((checkbox, var))

    def truncateText(self, text):
        if len(text) > 30:
            return text[:30] + "..."  
        else:
            return text

    def selectAll(self):
        for checkbox, var in self.checkboxes:
            if self.masterVar.get() == "on":
                var.set("on")
            else:
                var.set("off")

    def getSelectedCheckBoxes(self):
        temp = []
        for i, (checkbox, var) in enumerate(self.checkboxes, start=0):
            if var.get() =="on":
                temp.append(i)
        return temp


class PasswordGeneratorFrame(ctk.CTkFrame):
    def __init__(self,parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)
        self.grid_rowconfigure(5,weight=1)



        self.label = ctk.CTkLabel(self, text="Password Generator", font=Header2)
        self.label.grid(row=0, column=0, columnspan=2)

        self.generateButton = ctk.CTkButton(self, text="Generate", command=self.generatePassword, font=Text)
        self.generateButton.grid(row=1, column=0, columnspan=2)

        self.passwordVar = ctk.StringVar()
        self.passwordEntry = ctk.CTkEntry(self, textvariable=self.passwordVar, font=Text, height=40, width=200, justify=ctk.CENTER, state='readonly')
        self.passwordEntry.grid(row=2, column=0, columnspan=2, pady=5)

        self.startCheckbox= ctk.CTkCheckBox(self, variable=ctk.StringVar(value="off"), onvalue='on', offvalue='off', width=5, text='Add as Begining:', corner_radius=2, font=Text)
        self.startCheckbox.grid(row=3, column=0, sticky='ns', pady=5)
        self.startEntry = ctk.CTkEntry(self,placeholder_text="add to start")
        self.startEntry.grid(row=3, column=1, sticky='w', pady=5)

        self.endCheckbox= ctk.CTkCheckBox(self, variable=ctk.StringVar(value="off"), onvalue='on', offvalue='off', width=5, text='Add as Ending:', corner_radius=2, font=Text)
        self.endCheckbox.grid(row=4, column=0, sticky='ns', pady=5)
        self.endEntry = ctk.CTkEntry(self,placeholder_text="add to end")
        self.endEntry.grid(row=4, column=1, sticky='w', pady=5)

        self.lengthCheckbox= ctk.CTkCheckBox(self, variable=ctk.StringVar(value="off"), onvalue='on', offvalue='off', width=5, text='Length (14 default):', corner_radius=2, font=Text)
        self.lengthCheckbox.grid(row=5,column=0,sticky='ns', pady=5)
        self.lengthEntry = ctk.CTkEntry(self,placeholder_text="Length")
        self.lengthEntry.grid(row=5,column=1,sticky='w', pady=5)

    def generatePassword(self):
        start=''
        end=''
        length=14
        if(self.lengthCheckbox.get()=='on'):
            length= int(self.lengthEntry.get())
        if(self.startCheckbox.get()=="on"):
            start=self.startEntry.get()
        if(self.endCheckbox.get()=='on'):
            end=self.endEntry.get()
        self.passwordVar.set(self.userService.generatePassword(start=start, end=end,lengthIn=length))
        


class PasswordManagerFrame(ctk.CTkFrame):
    def __init__(self, parent, userSerice, passwordUpdated, getSelected, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userSerice
        self.passwordUpdated = passwordUpdated
        self.getSelected = getSelected
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)

        self.addpasswordFrame = AddPasswordFrame(self, self.userService, passwordUpdated=passwordUpdated, fg_color='transparent')
        self.deletePasswordFrame = DeletePasswordFrame(self, self.userService, passwordUpdated=passwordUpdated, getSelected=self.getSelected , fg_color='transparent')
        self.title = ctk.CTkLabel(self,text="Manage Passwords", font=Header1)
        self.searchPasswordFrame = SearchPasswordFrame(self, self.userService, fg_color='transparent')

        self.searchPasswordFrame.grid(row=1, column=0, padx=5,pady=5)
        self.addpasswordFrame.grid(row=2, column=0, padx=5, pady=5)
        self.deletePasswordFrame.grid(row=3, column=0,padx=5, pady=5)
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky='ew')



class SearchPasswordFrame(ctk.CTkFrame):
    def __init__(self, parent, userService, **kwargs):
        super().__init__(parent, **kwargs)
        self.userService = userService

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.findPasswordTitle = ctk.CTkLabel(self, text='Find Password', font=Header2)
        self.findPasswordTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=2)

        self.findPasswordLabel = ctk.CTkLabel(self, text='(Enter Website or Display Name)')
        self.findPasswordLabel.grid(row=1, column=0, columnspan=2, padx=5, pady=2)

        self.searchEntry = ctk.CTkEntry(self, placeholder_text="Enter", font=Text)
        self.searchEntry.grid(row=2, column=0, columnspan=2, padx= 5, pady=8)

        self.searchButton = ctk.CTkButton(self, text='Search', width=140, height=32, command=self.searchInfo)
        self.searchButton.grid(row=3, column=0, columnspan=2, padx= 5, pady=5)

        self.passwordVar = ctk.StringVar()
        self.usernameVar = ctk.StringVar()
        self.passwordDisplayEntry = ctk.CTkEntry(self, textvariable=self.passwordVar, font=Text, justify=ctk.CENTER, state='readonly', placeholder_text='Password', bg_color='#3A3B3C', border_width=1, corner_radius=0,fg_color='#3A3B3C')
        self.usernameDisplayEntry = ctk.CTkEntry(self, textvariable=self.usernameVar, font=Text, justify=ctk.CENTER, state='readonly', placeholder_text='Username', bg_color='#3A3B3C', border_width=1, corner_radius=0, fg_color='#3A3B3C')
        self.passwordDisplayEntry.grid(row=4, column=1, pady=5)
        self.usernameDisplayEntry.grid(row=4, column=0, pady=5)

    def searchInfo(self):
        if(self.searchEntry.get() is not None):
            username, password = self.userService.searchInfo(wanted=self.searchEntry.get())
            self.usernameVar.set(username)
            self.passwordVar.set(password) 

        
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
    def __init__(self, parent, userService, passwordUpdated, getSelected, **kwargs):
        super().__init__(parent,**kwargs)
        self.userService = userService
        self.passwordUpdated = passwordUpdated
        self.getSelected = getSelected

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.deletePasswordTitle = ctk.CTkLabel(self, text="Delete Password", font=Header2)
        self.deletePasswordTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.websiteLabel = ctk.CTkLabel(self, text="Enter Site to Delete:\n(or deletes selected entries)", font=Text)
        self.websiteEntry = ctk.CTkEntry(self, placeholder_text="URL or Display Name", font=Text, width=200)
        self.websiteLabel.grid(row=1,column=0, pady=5, sticky='ew', padx=(0, 10))
        self.websiteEntry.grid(row=1, column=1, pady=5, sticky='ew', padx=(10, 0))

        self.deleteButton = ctk.CTkButton(self, text="Delete", command=self.deletePassword, font=Text)
        self.deleteButton.grid(row=2, column=0, columnspan=2, padx=5, pady=10)


    def deletePassword(self):
        entryToDelete = self.websiteEntry.get()
        self.userService.deletePassword(entryToDelete=entryToDelete, getSelected=self.getSelected())
        self.websiteEntry.delete(0, ctk.END)
        self.passwordUpdated()




