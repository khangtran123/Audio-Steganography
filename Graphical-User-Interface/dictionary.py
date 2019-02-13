#!/usr/bin/python3
import ast

content = {}
dataF = ""
audioC = ""
save_to_dir = ""
password = ""
audioF = ""
password_unlock = ""
config_file = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/config.txt"

def getConfigFile():
    global dataF, audioC, save_to_dir, password, audioF, password_unlock
    
    with open(config_file, 'r') as f:
        s = f.read()
        content = ast.literal_eval(s)

    # There can be two dictionaries in config file: 1) Encoding, 2) Decoding
    if ("password_lock" in content):

        # Since content is intialized as a dictionary, we are going to use the keys content[key],
        # grab the value from the key, and put it into the variable that will be used later on
        dataF = content["datafile"]
        audioC = content["audioCarrier"]
        save_to_dir = content["save_to_dir"]
        password = content["password_lock"]
        
        #print("This is our datafile --> " + dataF)
        #print("This is our audio carrier file --> " + audioC)
        #print("This is where the embedded file will be stored --> " + save_to_dir)
        #print("This is the password --> " + password)
        return dataF,audioC,save_to_dir,password
        
    elif ("password_unlock" in content):
        audioF = content["audioF"]
        password_unlock = content["password_unlock"]

        #print ("This is the audio file for decoding --> " + audioF)
        #print ("This is the password to unlock --> " + password_unlock)
        return audioF, password_unlock
    else:
        print ("No other dictionaries exist")
        return

#getConfigFile()
