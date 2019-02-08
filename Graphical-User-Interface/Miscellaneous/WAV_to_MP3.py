#!/usr/bin/python3

'''
File: WAV-to-MP3.py
Date: January 30, 2019
Designers: Huu Khang Tran
Description: This scripts covers the general conversion of the chosen audio WAV file into a MP3 file
             using the Python Library ffmpeg. Script will be called upon as the final file output.
'''

import os
import subprocess
import sys

'''
wav_file = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/The Black Eyed Peas - Where Is The Love.wav"
mp3_file = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/The Black Eyed Peas - Where Is The Love.mp3"
'''

wav_file = str(sys.argv[0])
mp3_file = str(sys.argv[1])

def file_transform(wav_file, mp3_file):
    subprocess.call(['ffmpeg', '-i',wav_file,mp3_file], shell = False)
    #print (wav_file + " " + mp3_file)

file_transform(wav_file, mp3_file)

    




