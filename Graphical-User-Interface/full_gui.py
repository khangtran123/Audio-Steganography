#!/usr/bin/python3
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
#from audio_steg import *
from encryption import *
from decryption import *
from key_generator import create_keys
from dictionary import getConfigFile
#from WAV_to_MP3 import *
import os
import sys
import time
import platform
import re


TITLE_FONT = ("Arial Bold", 12)
LABEL_FONT = ("Arial Bold", 8)
FILE_FONT = ("Arial Bold", 8)

cfileCheck = False
aFileCheck = False
dirCheck = False
aCheck = False
pkCheck = False
pukCheck = False
config_encode = {}
config_decode= {}
# platform.system() gets the current OS of the system running the script
platform = str(platform.system())

config_file = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/config.txt"

'''
Class: Wireframe
Purpose: This creates the window structure that other window classes will inherit 
'''
class wireframe(tk.Tk):

    #  now we want to initialize the window and the necessary components when the GUI is started
    def __init__(self, *args, **kwargs):
        global container
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        #  pack --> You can nest frames with widgets in different directions freely
        container.pack(fill="both", expand = True)

        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(1, weight=1)

        #  we create and declare an array --> frames that will allow the application to have
        #  multiple pages in one window rather than multiple window dialogs
        self.frames = {}

        for F in (MainPage, EncodePage, DecodePage, CompleteEncodePage, CompleteDecodePage):

            #  Start with initial MainPage frame that will lead to encode or decode frame based
            #  what the user picks
            frame = F(container, self)

            self.frames[F] = frame

            #  grid --> When you want to have more structure in where you want your frames and
            #           features according to the grid layout of the window (rows and columns)
            #           This layout is very structured and allows better orgranization of different
            #           widgets in a window accordingly
            #  sticky = nsew --> North, South, East, West --> Alignment plus stretch
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    #  now we have a function that orgranizes the frame struct
    def show_frame(self, controller):

        frame = self.frames[controller]
        frame.tkraise() #  tkraise() --> raise it to the front page


'''
Page: Main Page
Purpose: This page is the main menu page that gives the user the options to either encode or decode
'''
class MainPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) #  parent class is "wireframe class"
        title = tk.Label(self, text="Khang's Audio Steganography Program", font=TITLE_FONT)
        title.pack(side=TOP, pady=10, padx=10)
        
        # create encode Button 
        encodeBtn = tk.Button(self, text="Encode", height="2", width="30",
               command=lambda: controller.show_frame(EncodePage))
        encodeBtn.pack(padx=5, pady=10)
                             
         # create Decode Button 
        decodeBtn = tk.Button(self, text="Decode", height="2", width="30",
               command=lambda: controller.show_frame(DecodePage))
        decodeBtn.pack(padx=5, pady=10)


'''
Page: Encode Page
Purpose: This page is created when the user wants to begin embedding
         a confidential file into a carrier file. 
'''
class EncodePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) #  parent class is "wireframe class"
        label = tk.Label(self, text="Encode", font=TITLE_FONT)
        label.grid(row=0, column=1,pady=10, padx=10)

        global password, fileLabel, audioL, dirL, platform
        

        #  Function: Browse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def browse():
            
            global datafile, cfileCheck, fileName, config_encode, fileLabel, platform 

            file = ""
            datafile = ""
            
            if (platform == "Windows"):
                print (platform)
                file = filedialog.askopenfilename(title = "Select a Data File",
                                                  initialdir="C:/",
                                                  filetypes = (("Word Documents","*.docx"),("XML Files","*.xml"),
                                                               ("Word 97-2003 Documents","*.doc"),("Text Files","*.txt"),
                                                               ("PDF Files","*.pdf"),("all files","*.*")))
            elif(platform == "Linux"):
                file = filedialog.askopenfilename(title = "Select a Data File",
                                                  initialdir="/",
                                                  filetypes = (("Word Documents","*.docx"),("XML Files","*.xml"),
                                                               ("Word 97-2003 Documents","*.doc"),("Text Files","*.txt"),
                                                               ("PDF Files","*.pdf"),("all files","*.*")))
            else:
                return
        
            datafile = str(file)
            if (len(datafile) == 0):
                messagebox.showwarning("No File Selected Warning","Remember, you have to select a data file to embed!")
            else:
                # Now we only want to display the filename and not the full path
                x = datafile.split("/")
                fileName = x[-1]
                fileLabel.configure(text=fileName)
                #print (datafile)
                cfileCheck = True
                config_encode["datafile"] = datafile
        
        
        #  Function: carrierBrowse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def carrierBrowse():
            
            global audioCarrier, afileCheck, audioFilename, config_encode, audioL, platform

            audioFile = ""
            audioCarrier = ""

            if (platform == "Windows"):
                #print (platform)
                audioFile = filedialog.askopenfilename( title = "Select an Audio File",
                                                        initialdir="C:/",
                                                        filetypes = (("Audio File","*.mp3"),("Wav Audio Files","*.wav"),("all files","*.*")))
                audioCarrier = str(audioFile)
            elif (platform == "Linux"):
                audioFile = filedialog.askopenfilename( title = "Select an Audio File",
                                                        initialdir="/",
                                                        filetypes = (("Audio File","*.mp3"),("Wav Audio Files","*.wav"),("all files","*.*")))
                audioCarrier = str(audioFile)
                
            if (len(audioCarrier) == 0):
                messagebox.showwarning("No File Selected Warning","Remember, you have to select an audio file to be the carrier!")
            else:
                y = audioCarrier.split("/")
                audioFilename = y[-1]
                audioL.configure(text=audioFilename)
                afileCheck = True
                config_encode["audioCarrier"] = audioCarrier


        def dirSave():
            
            global dirCheck, user_dir, directory, config_encode, dirL, platform

            directory = ""
            user_dir = ""

            if (platform == "Windows"):
                #print (platform)
                directory = filedialog.askdirectory(title= "Select a Directory", initialdir="C:/")
                user_dir = str(directory)
            elif (platform == "Linux"):
                directory = filedialog.askdirectory(title="Select a Directory", initialdir="/")
                user_dir = str(directory)
                
            if (len(user_dir) == 0):
                messagebox.showwarning("No Directory Selected Warning","Remember, you have to select a directory!")
            else:
                dirL.configure(text=directory)
                dirCheck = True
                config_encode["save_to_dir"] = user_dir
                #return dirCheck
        
        def helpBox():
            messagebox.showinfo('Help', 'Confidential File:  The file you want to hide into the audio                                       '
                                'carrier file. You can choose any recognized                                   '
                                'file format.'
                                '\n\n Carrier File:  Please choose a MP3 or WAV audio file that will                          '
                                'act as the carrier file that holds the embedded                             '
                                'file.'
                                '\n\n Directory: Please choose a folder destination to save the                             audio output.'
                                '\n\n Set Passphrase:  Please pick a password you would like to                                     '
                                'lock this scheme. Only the other third-party                                '
                                'person who obtains this password can                                         '
                                'unlock the file to retrieve the hidden file'
                                '\n\n Begin:  Click Begin to begin embedding the data file into the                '
                                'audio carrier file.')

        def password_req():
            messagebox.showinfo('Password Requirement Checklist', 'Primary conditions for password validation :'

                                '\n\n   1. Minimum 8 characters and Maiximum 12 characters.'
                                '\n\n   2 .The alphabets must be between [a-z]'
                                '\n\n   3. At least one alphabet should be of Upper Case [A-Z]'
                                '\n\n   4. At least 1 number or digit between [0-9].'
                                '\n\n   5. At least 1 character from [ _ or @ or $ or ! ].')

        def backToM():
            
            global fileLabel, audioL, dirL, password, datafile, audioCarrier, menuBtn

            #Reset form by clearing all labels and global variables
            if (fileLabel.winfo_exists() == 1):
                fileLabel.configure(text="")           
            if (audioL.winfo_exists() == 1):
                audioL.configure(text="")
            if (dirL.winfo_exists() == 1):
                dirL.configure(text="")
            if (len(password.get()) != 0):
                password.delete(0, 'end')

            datafile = ""
            audioCarrier = ""
            controller.show_frame(MainPage)

        def gen_keys():
            
            global passphrase, private_key, public_key, status
    
            flag = 0
            
            passphrase = password.get()

            while True:   
                if (len(passphrase) < 8): 
                    flag = -1
                    break
                elif (len(passphrase) > 12):
                    flag = -1
                    break
                elif not re.search("[a-z]", passphrase): 
                    flag = -1
                    break
                elif not re.search("[A-Z]", passphrase): 
                    flag = -1
                    break
                elif not re.search("[0-9]", passphrase): 
                    flag = -1
                    break
                elif not re.search("[_@$!]", passphrase): 
                    flag = -1
                    break
                elif re.search("\s", passphrase): 
                    flag = -1
                    break
                else: 
                    flag = 0
                    break
            
            if (flag == -1):
                # alert message informing user that no fields can be null
                status = "Keys-Not-Generated"
                messagebox.showerror("Passphrase Error", "Password must meet all requirements!")
            else:
                private_key, public_key = create_keys(passphrase)
                status = "Keys-Generated"
                messagebox.showinfo("Sucessful", "Password Accepted and Private & Public Keys Generated!")

        
        fileL = tk.Label(self,text="Confidential File: ", font=LABEL_FONT, width=15, anchor='w')
        fileL.grid(row=1,column=0)

        fileLabel = tk.Label(self, text="", font=FILE_FONT)
        fileLabel.grid(row=1, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=browse)
        browseBtn.grid(row=1,column=2)

        carrierL = tk.Label(self,text="Carrier File: ", font=LABEL_FONT, width=15, anchor='w')
        carrierL.grid(row=3,column=0)

        audioL = tk.Label(self, text="", font=FILE_FONT)
        audioL.grid(row=3, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=carrierBrowse)
        browseBtn.grid(row=3,column=2, padx=4)

        label = tk.Label(self,text="Directory: ", font=LABEL_FONT, width=15, anchor='w')
        label.grid(row=4,column=0)

        dirL = tk.Label(self, text="", font=FILE_FONT)
        dirL.grid(row=4, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=dirSave)
        browseBtn.grid(row=4,column=2)

        keyL = tk.Label(self,text="Set Passphrase:", font=LABEL_FONT, width=15, anchor='w')
        keyL.grid(row=5,column=0, padx=3)

            
        password = tk.Entry(self, show="*")
        password.grid(row=5, column=1, padx=3)

        # create a Browse File Directory Button 
        keyBtn = tk.Button(self, text="Generate Keys", height="1", width="12",
               command=gen_keys)
        keyBtn.grid(row=5,column=2)

        passReq = tk.Button(self,text="       Passphrase Requirements", height="1",
                            width="27", anchor='w', font = ('Arial Bold', '8','bold'),
                            bg="SkyBlue2", command=password_req)
        passReq.grid(row=6,column=1)

            
        #  This function is called when the Begin button is pressed
        #  Function saves all user input (both file paths and passphrase)
        def getFormInput():
            
            global line, config_file, passphrase, config_encode, output, status
            
            config_file = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/config.txt"
            flag = 0
            
            passphrase = password.get()

            while True:   
                if (len(passphrase) < 8): 
                    flag = -1
                    break
                elif (len(passphrase) > 12):
                    flag = -1
                    break
                elif not re.search("[a-z]", passphrase): 
                    flag = -1
                    break
                elif not re.search("[A-Z]", passphrase): 
                    flag = -1
                    break
                elif not re.search("[0-9]", passphrase): 
                    flag = -1
                    break
                elif not re.search("[_@$!]", passphrase): 
                    flag = -1
                    break
                elif re.search("\s", passphrase): 
                    flag = -1
                    break
                else: 
                    flag = 0
                    break
            
            if (flag == -1) or (cfileCheck == False) or (afileCheck == False) or (dirCheck == False) or (status == "Keys-Not-Generated") :
                # alert message informing user that no fields can be null
                messagebox.showerror("Error", "Cannot leave any fields empty, ie. Both files must be chosen and password must meet all requirements!"
                                              "  Remember that you must generate your public & private key before proceeding!")
            else:
                config_encode["password_lock"] = passphrase
                with open(config_file,"w") as configFile:
                    configFile.write(str(config_encode))

                af = config_encode["audioCarrier"]
                output = af.replace(".wav", ".mp3")
                controller.show_frame(CompleteEncodePage)

                
        # create a Begin Button
        beginBtn = tk.Button(self, text="Next", height="1", width="13", command=getFormInput)
        beginBtn.grid(row=8,column=1, padx=2, pady=13)

        # create Main Menu Button 
        menuBtn = tk.Button(self, text="Main Menu", height="1", width="12",
               command=backToM)
        menuBtn.grid(row=8,column=2, padx=2, pady=13)

        # create Help Me Button 
        helpEBtn = tk.Button(self, text="Help", height="1", width="8",
               command=helpBox)
        helpEBtn.grid(row=8,column=0, padx=8, pady=13)


'''
Page: Decode Page
Purpose: This page is created when the user receives an audio file and
         wishes to retreive the hidden data file. 
'''
class DecodePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) #  parent class is "wireframe class"
        label = tk.Label(self, text="Decode", font=TITLE_FONT)
        label.grid(row=0, column=1,pady=10, padx=10)

        global passwordU, pickedAudio, priv_keyL, public_keyL, direL

        #  Function: carrierBrowse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def carrierBrowseD():
            
            global audioF, aFileCheck, audioFilename, config_decode, pickedAudio, platform
            
            audioFile = ""
            audioF = ""

            if (platform == "Windows"):
                #print (platform)
                audioFile = filedialog.askopenfilename( title = "Select an Audio File",
                                                        initialdir="C:/",
                                                        filetypes = (("Audio File","*.mp3"),("Wav Audio Files","*.wav"),("all files","*.*")))
                audioF = str(audioFile)
            elif (platform == "Linux"):
                audioFile = filedialog.askopenfilename( title = "Select an Audio File",
                                                        initialdir="/",
                                                        filetypes = (("Audio File","*.mp3"),("Wav Audio Files","*.wav"),("all files","*.*")))
                audioF = str(audioFile)
                
            if (len(audioF) == 0):
                messagebox.showwarning("No File Selected Warning","Remember, you have to select an audio file to be the carrier!")
            else:
                y = audioF.split("/")
                audioFilename = y[-1]
                pickedAudio.configure(text=audioFilename)
                aFileCheck = True
                config_decode["audioF"] = audioF
                return aFileCheck


        def dirToSave():
            
            global dirCheck, user_dir, directory, config_decode, direL, platform

            directory = ""
            user_dir = ""

            if (platform == "Windows"):
                #print (platform)
                directory = filedialog.askdirectory(title= "Select a Directory", initialdir="C:/")
                user_dir = str(directory)
            elif (platform == "Linux"):
                directory = filedialog.askdirectory(title="Select a Directory", initialdir="/")
                user_dir = str(directory)
                
            if (len(user_dir) == 0):
                messagebox.showwarning("No Directory Selected Warning","Remember, you have to select a directory!")
            else:
                print (directory)
                direL.configure(text=directory)
                dirCheck = True
                config_decode["save_to_dir"] = user_dir
                return dirCheck


        #  Function: privateKey_browse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def privateKey_browse():
            
            global pk, pkCheck, pkFilename, config_decode, private_keyL, platform 

            private_key = ""
            pk = ""

            if (platform == "Windows"):
                private_key = filedialog.askopenfilename( title = "Select a Private Key File",
                                                        initialdir="C:/",
                                                        filetypes = (("Pem","*.pem"),("Key","*.key"),("all files","*.*")))
                pk = str(private_key)
            elif (platform == "Linux"):
                private_key = filedialog.askopenfilename( title = "Select a Private Key File",
                                                        initialdir="/",
                                                        filetypes = (("Pem","*.pem"),("Key","*.key"),("all files","*.*")))
                pk = str(private_key)
                
            if (len(pk) == 0):
                messagebox.showwarning("No File Selected Warning","Remember, you have to select a key file!")
            else:
                y = pk.split("/")
                pkFilename = y[-1]
                priv_keyL.configure(text=pkFilename)
                pkCheck = True
                config_decode["private_key"] = pk
                return pkCheck
            

        #  Function: publicKey_browse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def publicKey_browse():
            
            global puk, pukCheck, pukFilename, config_decode, public_keyL, platform 

            public_key = ""
            puk = ""

            if (platform == "Windows"):
                #print (platform)
                public_key = filedialog.askopenfilename( title = "Select a Public Key File",
                                                        initialdir="C:/",
                                                        filetypes = (("Pem","*.pem"),("Key","*.key"),("all files","*.*")))
                puk = str(public_key)
            elif (platform == "Linux"):
                public_key = filedialog.askopenfilename( title = "Select a Public Key File",
                                                        initialdir="/",
                                                        filetypes = (("Pem","*.pem"),("Key","*.key"),("all files","*.*")))
                puk = str(public_key)
                
            if (len(puk) == 0):
                messagebox.showwarning("No File Selected Warning","Remember, you have to select a key file!")
            else:
                y = puk.split("/")
                pukFilename = y[-1]
                public_keyL.configure(text=pukFilename)
                pukCheck = True
                config_decode["public_key"] = puk
                return pukCheck
                
        
        def helpBox():
            messagebox.showinfo('Help', 'Audio File:  Choose the audio file that has been sent to you                         covertly.'
                                ' This file contains the embedded data file                       that you want to retrieve.'
                                '\n\nDirectory:  Choose a directory to save the output file to'
                                '\n\nPrivate Key:  Choose the private key that will be used to unlock                      the extracted data file'
                                '\n\nPublic Key:  Choose the public key that will be used to                                   authenticate the sender.'
                                '\n\nEnter Passphrase:  Please enter the shared key passphrase to                                    '
                                'unlock and retreive the hidden file                                     '
                                '\n\nBegin:  Click Begin to begin decoding the audio file to                           retrieve the secret file!')
        

        def back():
            
            global pickedAudio, dirL, priv_keyL, public_keyL, passwordU, audioFile, directory, private_key, public_key

            #Reset form by clearing all labels and global variables
            if (pickedAudio.winfo_exists() == 1):
                pickedAudio.configure(text="")
            if (dirL.winfo_exists() == 1):
                dirL.configure(text="")
            if (priv_keyL.winfo_exists() == 1):
                priv_keyL.configure(text="")
            if (public_keyL.winfo_exists() == 1):
                public_keyL.configure(text="")
            if (len(passwordU.get()) != 0):
                passwordU.delete(0, 'end')
                
            audioFile = ""
            directory = ""
            private_key = ""
            public_key = ""
            controller.show_frame(MainPage)

        
        audioCarL = tk.Label(self,text="Audio File: ", font=LABEL_FONT, width=15, anchor='w')
        audioCarL.grid(row=1,column=0)

        pickedAudio = tk.Label(self, text="", font=FILE_FONT)
        pickedAudio.grid(row=1, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=carrierBrowseD)
        browseBtn.grid(row=1,column=2, padx=6)

        label = tk.Label(self,text="Directory to Save: ", font=LABEL_FONT, width=15, anchor='w')
        label.grid(row=2,column=0)

        direL = tk.Label(self, text="", font=FILE_FONT)
        direL.grid(row=2, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=dirToSave)
        browseBtn.grid(row=2,column=2)

        label = tk.Label(self,text="Private Key: ", font=LABEL_FONT, width=15, anchor='w')
        label.grid(row=3,column=0)

        priv_keyL = tk.Label(self, text="", font=FILE_FONT)
        priv_keyL.grid(row=3, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=privateKey_browse)
        browseBtn.grid(row=3,column=2)

        label = tk.Label(self,text="Public Key:", font=LABEL_FONT, width=15, anchor='w')
        label.grid(row=4,column=0)

        public_keyL = tk.Label(self, text="", font=FILE_FONT)
        public_keyL.grid(row=4, column=1)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=publicKey_browse)
        browseBtn.grid(row=4,column=2)

        enterKeyL = tk.Label(self,text="Passphrase:", font=LABEL_FONT, width=15, anchor='w')
        enterKeyL.grid(row=5,column=0, padx=5)

        passwordU = tk.Entry(self, show="*")
        passwordU.grid(row=5, column=1, padx=3)

        space = tk.Label(self,text="")
        space.grid(row=5, column=0, pady=10, padx=10)

        #  This function is called when the Begin button is pressed
        #  Function saves all user input (file path and passphrase)
        def getFormInput():
            
            global line, config_file, passphrase_unlock, config_decode, aFileCheck, pkCheck, pukCheck, dirCheck
            
            passphrase_unlock = passwordU.get()
            config_decode["password_unlock"] = passphrase_unlock
                    
            if (len(passphrase_unlock) == 0) or (aFileCheck == False) or (pkCheck == False) or (pukCheck == False) or (dirCheck == False):
                # alert message informing user that no fields can be null
                messagebox.showerror("Empty Field Error", "Cannot leave any fields empty, ie. File must be chosen and password cannot be null")
            else:
                with open(config_file,"w") as configFile:
                    configFile.write(str(config_decode))
                controller.show_frame(CompleteDecodePage)
                
            
        # create Main Menu Button 
        menuBtn = tk.Button(self, text="Main Menu", height="1", width="12",
               command=back)
        menuBtn.grid(row=6, column=2, padx=17, pady=13)

        # create Help Me Button 
        helpEBtn = tk.Button(self, text="Help", height="1", width="8",
               command=helpBox)
        helpEBtn.grid(row=6,column=0, padx=17, pady=13)

         # create a Begin Button 
        beginBtn = tk.Button(self, text="Begin Decoding", height="1", width="12",
                             command=getFormInput)
        beginBtn.grid(row=6,column=1, padx=17, pady=13)



'''
Page: Completed Encode Page
Purpose: This page is created when the user completes either the encoding
         or decoding process. 
'''
class CompleteEncodePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) #  parent class is "wireframe class"
        title = tk.Label(self, text="Encoding Stage", font=TITLE_FONT)
        title.pack(side=TOP, pady=10, padx=10)

        def run_encode_algorithm():
            #  This is where I will call the functions in algorithm script
            return
                
        '''
        Function Percentage
        Case 1: What is x % of y? 
        Case 2: x is what % of y?
        Case 3: What is the percentage increase/decrease from x to y
        '''
        def percentage_calculator(x,y,case=1):
            if (case == 1):
                r = x/100*y
                return r
            elif (case == 2):
                r = x/y*100
                return r
            elif (case == 3):
                r = (y-x)/x*100
                return r
            else:
                raise Exception("Only case 1, 2, or 3 are available!")

        def progress_bar_process(progress, runButton):
            
            global output, config_encode, private_key, public_key
            
            runButton.config(state="disabled")
            # create the countdown measurements of 10 seconds
            alist = range(10)
            try:
                # This section involves using my hybrid crypto-system
                # Private and Public keys are now generated
                #private_key, public_key = create_keys(pwd)
                # Get config variables from config file and load them into specific var
                dataF, audioC, save_to_dir, pwd = getConfigFile()
                # Hash the password to meet AES-128 bit criteria
                password = hashlib.sha256(pwd.encode('utf-8')).digest()
                # Begin File encryption and then lock file
                file_encryption(private_key, public_key, password, dataF, save_to_dir)
                p = 0
                for i in alist:
                    p += 1
                    # Case2: x is what percent of y?
                    unit = percentage_calculator(p, len(alist), case=2) 

                    time.sleep(1)

                    progress['value'] = unit
                    percent['text'] = "{}%".format(int(unit))

                    container.update()

                messagebox.showinfo('Info', "Process completed!")
                
                def reset():
                    
                    global fileLabel, audioL, dirL, password, datafile, audioCarrier, output, menuBtn

                    #Reset form by clearing all labels and global variables
                    fileLabel.configure(text="")
                    audioL.configure(text="")
                    dirL.configure(text="")
                    password.delete(0, 'end')
                    datafile = ""
                    audioCarrier = ""
                    output = ""
                    menuBtn.pack_forget()
                    runButton.config(state="active")
                    controller.show_frame(MainPage)
                
                
                # create back to Main Menu Button
                global menuBtn
                menuBtn = tk.Button(self, text="Main Menu", height="1", width="12",
                       command=reset)
                menuBtn.pack(side=BOTTOM, pady = 15)
                
            except Exception as e:
                messagebox.showinfo('Info', "ERROR: {}".format(e))
                sys.exit()       
        
        
        percent = tk.Label(self,text="", anchor=S)
        percent.pack()

        progress = Progressbar(self,length=400, mode='determinate')
        progress.pack()

        runButton = tk.Button(self, text='Begin Embedding',
                           command=(lambda: progress_bar_process(progress, runButton)))
        runButton.pack(pady=15)

        status = tk.Label(self,text="Please wait until the process is complete to produce the outputted audio file", relief=SUNKEN, anchor=W, bd=2)
        status.pack(side=BOTTOM, fill=X)

'''
Page: Completed Encode Page
Purpose: This page is created when the user completes either the encoding
         or decoding process. 
'''
class CompleteDecodePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) #  parent class is "wireframe class"
        title = tk.Label(self, text="Decoding Stage", font=TITLE_FONT)
        title.pack(side=TOP, pady=10, padx=10)

        def run_decode_algorithm():
            #  This is where I will call the functions in algorithm script
            return
                
        '''
        Function Percentage
        Case 1: What is x % of y? 
        Case 2: x is what % of y?
        Case 3: What is the percentage increase/decrease from x to y
        '''
        def percentage_calculator(x,y,case=1):
            if (case == 1):
                r = x/100*y
                return r
            elif (case == 2):
                r = x/y*100
                return r
            elif (case == 3):
                r = (y-x)/x*100
                return r
            else:
                raise Exception("Only case 1, 2, or 3 are available!")

        def progress_bar_process(progress, runButton):
            runButton.config(state="disabled")
            # create the countdown measurements of 10 seconds
            alist = range(10)
            # Run Stego Algorithm Script
            #run_algorithm()
            try:
                # This section involves using my hybrid crypto-system
                # Private and Public keys are now generated
               # private_key, public_key = create_keys()
                # Get config variables from config file and load them into specific var
                locked_file, directory, private_key, public_key, pwd = getConfigFile()
                # Hash the password to meet AES-128 bit criteria
                password = hashlib.sha256(pwd.encode('utf-8')).digest()
                # We first need to extract the files from the all file sent by the sender
                extraction(locked_file)
                # Now that all files are extracted, we want to decrypt the file
                decrypt(private_key, public_key, password, locked_file, directory)
                p = 0
                for i in alist:
                    p += 1
                    # Case2: x is what percent of y?
                    unit = percentage_calculator(p, len(alist), case=2) 

                    time.sleep(1)

                    progress['value'] = unit
                    percent['text'] = "{}%".format(int(unit))

                    container.update()

                messagebox.showinfo('Info', "Retrieval Process Complete! Hidden data is in the same directory as the original audio output directory")
                
                def reset():

                    global pickedAudio, direL, priv_keyL, public_keyL, passwordU, audioFile, audioF, directory, private_key, public_key

                    #Reset form by clearing all labels and global variables
                    pickedAudio.configure(text="")
                    direL.configure(text="")
                    priv_keyL.configure(text="")
                    public_keyL.configure(text="")
                    passwordU.delete(0, 'end')
                    audioF = ""
                    audioFile = ""
                    pk = ""
                    puk = ""
                    private_key = ""
                    public_key = ""
                    directory = ""
                    menuBtn.pack_forget()
                    runButton.config(state="active")
                    controller.show_frame(MainPage)
                
                
                # create back to Main Menu Button
                global menuBtn
                menuBtn = tk.Button(self, text="Main Menu", height="1", width="12",
                       command=reset)
                menuBtn.pack(side=BOTTOM, pady = 15)
                
            except Exception as e:
                messagebox.showinfo('Info', "ERROR: {}".format(e))
                sys.exit()       
        
        
        percent = tk.Label(self,text="", anchor=S)
        percent.pack()

        progress = Progressbar(self,length=400, mode='determinate')
        progress.pack()

        runButton = tk.Button(self, text='Begin Decoding',
                           command=(lambda: progress_bar_process(progress, runButton)))
        runButton.pack(pady=15)

        status = tk.Label(self,text="Please wait until the process is complete to retrieve the hidden data file", relief=SUNKEN, anchor=W, bd=2)
        status.pack(side=BOTTOM, fill=X)
        

#  This condition makes sure that the user is either operating in Windows or Linux as we don't support any other OS at the moment
if ((platform == "Windows") or (platform == "Linux")):
    app = wireframe()
    app.title("Khang's Audio Steganography Program")
    app.resizable(False,False)
    app.mainloop()
else:
    print ("This Application does not support " + platform + " at the moment!")
