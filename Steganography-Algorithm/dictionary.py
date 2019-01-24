#!/usr/bin/python2
global config_list
import ast

content = {}
dataF = ""
audioC = ""
save_to_dir = ""
password = ""
config_file = "C:/Users/Khang/Documents/BCIT Semester 8/Project/config-file.txt"

def getConfigFile():
    with open(config_file, 'r') as f:
        s = f.read()
        content = ast.literal_eval(s)

    # Since content is intialized as a dictionary, we are going to use the keys content[key],
    # grab the value from the key, and put it into the variable that will be used later on
    dataF = content["datafile"]
    audioC = content["audioCarrier"]
    save_to_dir = content["save_to_dir"]
    password = content["password"]

    print("This is our datafile --> " + dataF)
    print("This is our audio carrier file --> " + audioC)
    print("This is where the embedded file will be stored --> " + save_to_dir)
    print("This is the password --> " + password)

getConfigFile()
