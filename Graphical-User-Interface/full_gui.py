#!/usr/bin/python3
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
import os
import sys
import time


TITLE_FONT = ("Arial Bold", 12)
LABEL_FONT = ("Arial Bold", 8)
FILE_FONT = ("Arial Bold", 8)

cfileCheck = False
afileCheck = False
dirCheck = False
config_list = {}



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

        for F in (MainPage, EncodePage, DecodePage, CompletePage):

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

        imgpath = r"C:/Users/Khang/Documents/BCIT-BTech_Practicum/LockedEnvelope.gif"
        photo = PhotoImage(file= imgpath)
        
        # create encode Button 
        encodeBtn = tk.Button(self, text="Encode", height="2", width="30",
               command=lambda: controller.show_frame(EncodePage))
        encodeBtn.pack(padx=5, pady=10)

        '''
        pic = tk.Label(self, image=photo)
        pic.image = photo
        pic.grid(row=3,column=1)
        #pic.pack(side=RIGHT)'''
                             
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

        global password

        #  Function: Browse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def browse():
            global datafile
            global cfileCheck
            global fileName
            global config_list
            global fileLabel

            file = ""
            datafile = ""
            
            file = filedialog.askopenfilename(initialdir="C:/Users/Khang/Documents/BCIT-BTech_Practicum",
                                              filetypes = (("Word Documents","*.docx"),("XML Files","*.xml"),
                                                           ("Word 97-2003 Documents","*.doc"),("Text Files","*.txt"),
                                                           ("PDF Files","*.pdf"),("all files","*.*")))

        
            datafile = str(file)
            if (len(datafile) == 0):
                messagebox.showerror("You have to select a file!")
            else:
                # Now we only want to display the filename and not the full path
                x = datafile.split("/")
                fileName = x[-1]
                fileLabel = tk.Label(self, text="", font=FILE_FONT)
                fileLabel.grid(row=1, column=1)
                fileLabel.configure(text=fileName)
                #print (datafile)
                cfileCheck = True
                config_list["datafile"] = datafile
        
        
        #  Function: carrierBrowse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def carrierBrowse():
            global audioCarrier
            global afileCheck
            global audioFilename
            global config_list
            global audioL

            audioFile = ""
            audioCarrier = ""
            
            audioFile = filedialog.askopenfilename(filetypes = (("Audio File","*.mp3"),("Wav Audio Files","*.wav"),("all files","*.*")))
            audioCarrier = str(audioFile)
            y = audioCarrier.split("/")
            audioFilename = y[-1]
            audioL = tk.Label(self, text="", font=FILE_FONT)
            audioL.grid(row=3, column=1)
            audioL.configure(text=audioFilename)
            afileCheck = True
            config_list["audioCarrier"] = audioCarrier
            return afileCheck


        def dirSave():
            global dirCheck
            global user_dir
            global directory
            global config_list
            global dirL

            directory = ""
            user_dir = ""
            
            directory = filedialog.askdirectory()
            dirL = tk.Label(self, text="", font=FILE_FONT)
            dirL.grid(row=4, column=1)
            dirL.configure(text=directory)
            user_dir = str(directory)
            dirCheck = True
            config_list["save_to_dir"] = user_dir
            return dirCheck
        
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

        
        fileL = tk.Label(self,text="Confidential File: ", font=LABEL_FONT, width=15, anchor='w')
        fileL.grid(row=1,column=0)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=browse)
        browseBtn.grid(row=1,column=2)

        carrierL = tk.Label(self,text="Carrier File: ", font=LABEL_FONT, width=15, anchor='w')
        carrierL.grid(row=3,column=0)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=carrierBrowse)
        browseBtn.grid(row=3,column=2, padx=4)

        dirL = tk.Label(self,text="Directory: ", font=LABEL_FONT, width=15, anchor='w')
        dirL.grid(row=4,column=0)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=dirSave)
        browseBtn.grid(row=4,column=2)

        keyL = tk.Label(self,text="Set Passphrase:", font=LABEL_FONT, width=15, anchor='w')
        keyL.grid(row=5,column=0, padx=3)

            
        password = tk.Entry(self, show="*")
        password.grid(row=5, column=1, padx=3)

        passReq = tk.Label(self,text="Minimum of length of 8 characters", font=LABEL_FONT, width=27, anchor='w')
        passReq.grid(row=6,column=1)


        def run_algorithm():
            os.system('random.py')
            
        #  This function is called when the Begin button is pressed
        #  Function saves all user input (both file paths and passphrase)
        def getFormInput():
            global line
            global config_file
            global passphrase
            global config_list
            
            config_file = "C:/Users/Khang/Documents/BCIT Semester 8/Project/config-file.txt"
            
            passphrase = password.get()
            config_list["password"] = passphrase
            if (len(passphrase) < 8) or (cfileCheck == False) or (afileCheck == False) or (dirCheck == False):
                # alert message informing user that no fields can be null
                messagebox.showerror("Error", "Cannot leave any fields empty, ie. Both files must be chosen and password cannot be null or less than 8 characters!")
            else:
                with open(config_file,"w") as configFile:
                    configFile.write(str(config_list))
                print ("List printed to file!")
                controller.show_frame(CompletePage)
                        

        # create a Begin Button
        beginBtn = tk.Button(self, text="Next", height="1", width="13", command=getFormInput)
        beginBtn.grid(row=8,column=1, padx=2, pady=13)

        # create Main Menu Button 
        menuBtn = tk.Button(self, text="Main Menu", height="1", width="12",
               command=lambda: controller.show_frame(MainPage))
        menuBtn.grid(row=8,column=2, padx=2, pady=13)

        # create Help Me Button 
        helpEBtn = tk.Button(self, text="Help", height="1", width="8",
               command=helpBox) #helpBox)
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

        #  Function: carrierBrowse()
        #  Purpose: Enables the user to browse from the file directory via filedialog
        def carrierBrowseD():
            audioFile = filedialog.askopenfilename(filetypes = (("Audio File","*.mp3"),("Wav Audio Files","*.wav"),("all files","*.*")))
            a = str(audioFile).split("/")
            audioName = a[-1]
            audioL = tk.Label(self, text="", font=FILE_FONT)
            audioL.grid(row=1, column=1)
            audioL.configure(text=audioName)

        def helpBox():
            messagebox.showinfo('Help', 'Audio File:  Choose the audio file that has been sent to you                         covertly.'
                                ' This file contains the embedded data file                       that you want to retrieve.'
                                '\n\nEnter Passphrase:  Please enter the shared key passphrase to                                    '
                                'unlock and retreive the hidden file                                     '
                                '\n\nBegin:  Click Begin to begin decoding the audio file to                           retrieve the secret file!')

        def run_decode():
            os.system('random.py')

        
        audioCarL = tk.Label(self,text="Audio File: ", font=LABEL_FONT, width=15, anchor='w')
        audioCarL.grid(row=1,column=0)
        
        # create a Browse File Directory Button 
        browseBtn = tk.Button(self, text="Browse", height="1", width="10",
               command=carrierBrowseD)
        browseBtn.grid(row=1,column=2)

        enterKeyL = tk.Label(self,text="Enter Passphrase:", font=LABEL_FONT, width=15, anchor='w')
        enterKeyL.grid(row=2,column=0, padx=3)

        password = tk.Entry(self, show="*")
        password.grid(row=2, column=1, padx=3)

        space = tk.Label(self,text="")
        space.grid(row=3, column=0, pady=10, padx=10)
            
        # create Main Menu Button 
        menuBtn = tk.Button(self, text="Main Menu", height="1", width="12",
               command=lambda: controller.show_frame(MainPage))
        menuBtn.grid(row=4, column=2, padx=10, pady=13)

        # create Help Me Button 
        helpEBtn = tk.Button(self, text="Help", height="1", width="8",
               command=helpBox)
        helpEBtn.grid(row=4,column=0, padx=10, pady=13)

         # create a Begin Button 
        beginBtn = tk.Button(self, text="Begin Decoding", height="1", width="12",
                             command=run_decode)
        beginBtn.grid(row=4,column=1, padx=10, pady=13)



'''
Page: Complete Page
Purpose: This page is created when the user completes either the encoding
         or decoding process. 
'''
class CompletePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent) #  parent class is "wireframe class"
        title = tk.Label(self, text="Encoding Stage", font=TITLE_FONT)
        title.pack(side=TOP, pady=10, padx=10)

        def run_algorithm():
            os.system('random.py')
                
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
                    global fileLabel
                    global audioL
                    global dirL
                    global password
                    global datafile
                    global audioCarrier
                    global menuBtn

                    #Reset form by clearing all labels and global variables
                    fileLabel.configure(text="")
                    audioL.configure(text="")
                    dirL.configure(text="")
                    password.delete(0, 'end')
                    datafile = ""
                    audioCarrier = ""
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
        

        
app = wireframe()
app.title("Khang's Audio Steganography Program")
#app.geometry("400x250")
#app.resizable(0,0)
app.mainloop()
