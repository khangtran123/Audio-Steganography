#! /usr/bin/python3

'''
File: audio-class.py
Date: January 31, 2019
Name: Huu Khang Tran
Description: This class contains the framework and schematics of the carrier WAV file. This class will act
             as the main architecture to loading, reading, and retrieving all necessary details about the
             audio file like frames, sizes, etc...

             In this case, we only need to extract the frames and nothing more like getting audio samples
             or channels. 
'''

import wave as w


class AudioDiagnostics:


    #  This will initialize the audio WAV file by opening the file source and
    #  reading in the bytes
    def __init__(self, file):
        self.file = w.open(file,'rb')   # rb = Read Only Mode

    
    '''
    Function: get_audio_frames
    Purpose: Once we open the audio file, we want to know the total number
             of frames per file.
    Output: int represents total number of audio
            frames in the file object
    '''
    def get_audio_frames(self):
        return self.file.getnframes()   #getnframes() = Returns number of audio frames


    '''
    Function: read_audio_frame
    Purpose: Once we retrieved the number of audio frames, we want to
             extract information from each frame
    Output: Reads and returns at most n frames of audio, as a string of bytes.
    '''
    def read_audio_frames(self):
        return self.file.readframes(self.get_audio_frames())  # readframes(n) --> iterate through each frame based on the total count of frames

    
    '''
    Function: get_frame_segments
    Purpose: Once we read through the audio frames, we want to
             extract each segment of the frame like headers and all that
    Output: gets tuple of parameters that makes up each audio frame. (Tuple =  finite ordered list (sequence) of elements that makes up per audio frame)
    Returns (nchannels, sampwidth, framerate, nframes, comptype, compname)
    '''
    def get_frame_segments(self):
        return self.file.getparams()
    

    '''
    Function: close_audio_file
    Purpose: Once we are done with the opened audio file, it's time to close it
    '''
    def close_audio_file(self):
        return self.file.close()

  
    
    
