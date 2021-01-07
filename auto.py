from pyad import *
import tkinter as tk
from tkinter import font as tkfont


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")

       
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.title("Automation")
        label = tk.Label(self, text="Menu", font=controller.title_font)
        label.grid(row=0,column=0)

        currentuser = tk.Label(self, text="current User:")
        currentuser.grid(row=1,column=0)
        pyad.set_defaults(ldap_server="geek.local", username="",password="")
        user = pyad.aduser.ADUser.from_cn("Administrator")
        username = tk.Label(self, text=user.get_attribute("Name"))
        username.grid(row=1,column=1)

        button1 = tk.Button(self, text="Add User",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Delete User",
                            command=lambda: controller.show_frame("PageTwo"))
        
        button1.grid(row=2,column=1)
        button2.grid(row=2,column=2)

        quit = tk.Button(self, text="Quit", command=controller.destroy)
        quit.grid(row=2,column=0)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Add User", font=controller.title_font)
        label.grid(row=0,column=0)

# First Name Entry
        FirstName_Label = tk.Label(self, text="First Name")
        global FirstName_Entry
        FirstName_Entry = tk.Entry(self)
        FirstName_Label.grid(row=1,column=1)
        FirstName_Entry.grid(row=1,column=2)

# Last Name Entry
        LastName_Label = tk.Label(self, text="Last Name")
        global LastName_Entry
        LastName_Entry = tk.Entry(self)
        LastName_Label.grid(row=2,column=1)
        LastName_Entry.grid(row=2,column=2)        
                
# Password Entry
        Password_Label = tk.Label(self, text="Enter Password")
        global Password_Entry
        Password_Entry = tk.Entry(self, show="*")
        Password_Label.grid(row=6,column=1)
        Password_Entry.grid(row=6,column=2)
        ConfirmPassword_Label = tk.Label(self, text="Confirm Password")
        global ConfirmPassword_Entry
        ConfirmPassword_Entry = tk.Entry(self, show="*")
        ConfirmPassword_Label.grid(row=7,column=1)      
        ConfirmPassword_Entry.grid(row=7,column=2)
            

# Department Entry
        Department_Label = tk.Label(self, text="Select Department")
        Department_Label.grid(row=5,column=1)
        OptionList = [
        "Einkauf",
        "Finanzen",
        "Geschäftsführung",
        "IT",
        "Lager",
        "Personal",
        "Verkauf",
        "Verwaltung"
        ]
        global dep
        dep = tk.StringVar(self)
        dep.set(OptionList[0])

        Department_Entry = tk.OptionMenu(self, dep, *OptionList)
        Department_Entry.grid(row=5,column=2)
        
        button = tk.Button(self, text="Go to the Menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=99,column=1)
        save_button = tk.Button(self, text="Save",command=self.saveuser)
        save_button.grid(row=99,column=2)
        quit = tk.Button(self, text="Quit", command=controller.destroy)
        quit.grid(row=99,column=0)

            
    def saveuser(self):
        if Password_Entry.get() == ConfirmPassword_Entry.get():
            department = dep.get()
            ou = pyad.adcontainer.ADContainer.from_dn("OU=Ben_"+department+",OU=Benutzer,OU=GEEK-Fitness,DC=geek,DC=local")
            givenName = FirstName_Entry.get()
            sn = LastName_Entry.get()
            global sAMAccountName
            sAMAccountName = sn[:4].lower() + givenName[:2].lower()
            displayName = givenName + " " + sn
            userPrincipalName = sAMAccountName + "@geek.local"
            profilePath = r"\\geek-dc-1\Profile$\%username%"
            homeDrive = "H:"
            homeDirectory = r"\\geek-dc-1\Homes$\%username%"
            password = Password_Entry.get()
            distinguishedName = "CN="+displayName+",OU=Ben_"+department+",OU=Benutzer,OU=GEEK-Fitness,DC=geek,DC=local"
            new_user = pyad.aduser.ADUser
            new_user = pyad.aduser.ADUser.create(displayName, ou, password=password, upn_suffix=None, enable=True, optional_attributes={"userPrincipalName":userPrincipalName,"sAMAccountName":sAMAccountName,"givenName":givenName,"displayName":displayName,"sn":sn,"homeDirectory":homeDirectory,"homeDrive":homeDrive})
            group = pyad.adgroup.ADGroup.from_cn("Grp_"+department)
            group.add_members([new_user])
            usercreate_Label = tk.Label(self, text="User created")
            usercreate_Label.grid(row=98,column=2)
        else:
            passerror = tk.Label(self, text="not the same password")
            passerror.grid(row=98,column=2)
            

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Delete User", font=controller.title_font)
        label.grid(row=0,column=0)
        Cred_Label = tk.Label(self, text="Enter Username")
        global Cred_Entry
        Cred_Entry = tk.Entry(self)
        Cred_Label.grid(row=3,column=1)
        Cred_Entry.grid(row=3,column=2)

        button = tk.Button(self, text="Go to the Menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=99,column=1)
        delete_button = tk.Button(self, text="Delete", command=self.deleteuser)
        delete_button.grid(row=99,column=2)
        quit = tk.Button(self, text="Quit", command=controller.destroy)
        quit.grid(row=99,column=0)

    def deleteuser(self):
        deluser = Cred_Entry.get()
        try:
            pyad.aduser.ADUser.from_cn(deluser).delete()
            print("User deleted")
            del_Label = tk.Label(self, text="User deleted")
            del_Label.grid(row=98,column=2)
        except:
            error_Label = tk.Label(self, text="User not found")
            error_Label.grid(row=98,column=2)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
