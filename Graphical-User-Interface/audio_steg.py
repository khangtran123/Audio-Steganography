#!/usr/bin/python3
global config_list
import ast
import wav
import audio_framework

'''
Variables from Config
********************************************************************
Encoding

dataF --> Data File
audioC --> Audio Carrier File
save_to_dir --> Selected Directory to save embedded audio output file
password --> password used to lock the audio file
********************************************************************
Decoding

audioF --> Audio File that will be decoded for file retrieval
password_unlock --> Password used to unlock audio file
'''

content = {}
dataF = ""
audioC = ""
save_to_dir = ""
password = ""
audioF = ""
password_unlock = ""
config_file = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/config.txt"

def config():
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
    

'''
An audio frame, or sample, contains amplitude (loudness)
information at that particular point in time. To produce
sound, tens of thousands of frames are played in sequence
to produce frequencies.

We want to retreieve the number of samples per frame to
the exact byte in order to avoid quality distortion due
to mismatched byte-to-byte comparisons

1. Encrypt Data File Using AES-128
2. Lock the file using RSA Keys (Private Key)
3. Embed the file into audio file
'''
def encode():

    # load the config variables
    config()

    #  Initialize audio file by calling the AudioDiag class
    file = audio_framework.AudioDiagnostics(audioC)

    #  Once we intialize the audio file, grab the parameters
    data = file.get_frame_segments

    
'''
1. Retrieve the segments
2. Unlock the file using Public Key
3. Decrypt the file via AES-128
'''
def decode():
    return

encode()
    





