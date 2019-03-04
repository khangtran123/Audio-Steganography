#!/usr/bin/python3
global config_list
import ast
import wave as w
import audio_framework
import math
import struct
import sys
import threading
import time
import taglib


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
3. Embed the file into audio file via LSB Insertion

    In conventional LSB technique,
    which requires eight bytes of pixels to store 1byte of secret
    data but in proposed LSB technique, just four bytes of pixels
    are sufficient to hold one message byte.
'''


# Now we want to retrieve the config variables from config file
#dataF, audioC, save_to_dir, pwd = getConfigFile()
#audioC = "C:/Users/Khang/Documents/GitHub/UpbeatFunk_NEW.wav"
#dataF = "C:/Users/Khang/Documents/Job Hunting/KhangTran_Resume.docx"
#audioC = "C:/Users/Khang/Documents/BCIT Semester 8/Audio-Steganography/UpbeatFunk.wav"
#dataF = "C:/Users/Khang/Documents/BCIT Semester 8/Project/file.all"
#directory = "C:/Users/Khang/Documents/SSC"


def embed(audio_carrier, dataF, directory):

    startTime = time.ctime(time.time())
    start = time.time()
    
    # indexes --> bit representation of how much of the file is processed
    index_file_data = 0
    index_audio_data = 0

    new_audio_buffer = []
    current_buffer = 0
    buffer_len = 0
    status = False


    #  Initialize audio file by calling the AudioDiagnostics Class
    file = audio_framework.AudioDiagnostics(audio_carrier)

    print (audio_carrier + " file has been opened")

    #  Once we intialize the audio file, grab the parameters --> getparams()
    data = file.get_frame_segments()

    # Get the total number of channels in audio file --> return 2 for stereo
    channels = file.get_num_channels()
    print("Total Number of Channels: " + str(channels))

    # Gets the sample width/bit width (the number of bytes per sample)
    # A frame consists of samples. There is one sample per channel, per frame. Every wav file has a sample width
    sample_width = file.get_num_samplew()
    print ("Sample Width: " + str(sample_width))

    # Get the total number of frames
    total_frames = file.get_audio_frames()
    print ("Total Number of Frames in Audio File: " + str(total_frames))

    # Calculates the total number of samples in the audio file
    total_samples = total_frames * channels
    print ("Total number of samples: " + str(total_samples))

    data_file = open(dataF,"rb").read()
    
    file_size = len(data_file)
    
    # get total storage space of bytes that can store the file --> each frame can 
    lsb_space = math.ceil(file_size * 8 / total_samples)
    print ("Total space for storage " + str(lsb_space))

    if (lsb_space > 4):
        raise ValueError("Input file too large to hide, "
                         "max byte to hide is {}"
                         .format((total_samples * lsb_space) // 8))
    #else:
        #print("data file is perfect size to embed into audio")

    # The width of a sample defines the number of bits required to represent the value on a storage medium
    # Typical Wav File --> Stores audio using stereo 16-bit samples (Highest Quality) or 8-bits (Lowest Quality for file size)
    # If sample width is 1 byte == 8 bits --> that means they are unsigned 8 bit
    # If sample width is 2 bytes == 16 bits --> means signed 16 bit 
    if(sample_width == 1):
        sample_quality = "{}B".format(total_samples) # represented through byte form
        # (1 << 8) == shift 1 binary (0001) to the left by 8 bits
        # masking is used to set the least significant bit of each sample
        masking = (1 << 8) - (1 << lsb_space)
        min_masking_sample = -(1 << 8)
    elif(sample_width == 2):
        sample_quality = "{}h".format(total_samples) # Represented through hexadecimal width
        # (1 << 15) == shift 1 binary (0000 0001) to the left 15 bits --> 1000 0000 0000 0000 = 32768 decimal
        # (1 << lsb_space) == shift 1 binary (0000 0001) to the left 1 bit left (0000 0010) == 2
        # masking is used to set the least significant bit of each sample
        masking = (1 << 15) - (1 << lsb_space)
        # remember to also retrieve the lowest possible value of a sample
        min_masking_sample = -(1 << 15)
        #print (sample_quality)
    else:
        raise ValueError("File has unsupport bit-depth that can store a single bit of the datafile")

    sample_details = list(struct.unpack(sample_quality, file.read_audio_frames(total_frames)))
    file.close_audio_file()

    # now create a loop that will perform LSB until status == True (new audio content buffer is empty)
    while(not status):

        # Loop that makes sure the buffer is filled with new buffer data and index_file_data bits are filled up with data file
        while((buffer_len < lsb_space) and (index_file_data // 8 < len(data_file))):
            # // in python == divide with integral result (discard remainder) --> i.e. 80/3 = 26 rather than 26.66666
            # we take the current buffer and increment --> value of the bytes retrieved from data file in binary and shifting
            # the value by (value of file index mod 8) bits to the right followed. Now we take that new binary value and perform
            # another shift (buffer_len) to the left
            current_buffer += (data_file[index_file_data // 8] >> (index_file_data % 8)) << buffer_len
            bits_added = 8 - (index_file_data % 8)
            buffer_len += bits_added    # now we want to being adding the bits into buffer len
            index_file_data += bits_added

        # now we want to retrieve the next set of lsb_space bits from the buffer
        current_data = current_buffer % (1 << lsb_space)
        current_buffer >>= lsb_space
        buffer_len -= lsb_space
        #print (buffer_len)
        #print ("Length of new altered sound buffer: " + str(len(sample_details)))

        # doesn't go to loop len(sample_details) == 3135364
        # Loop that makes sure the data from the audio file fully iterates through actual audio file (sample_details = iterate through all frames)
        # and the index of the sample_details is the at the lowest bit that can be read
        while(index_audio_data < len(sample_details) and sample_details[index_audio_data] == min_masking_sample):
            # This will iterate throught the samples from the audio file and will skip the lowest possible
            # sample value (min_sample). If we decide to alter the LSB of this value can lead to buffer
            # overflows or distort output quality
            new_audio_buffer.append(struct.pack(sample_quality[-1],sample_details[index_audio_data]))
            index_audio_data += 1
            
        if (index_audio_data < len(sample_details)):
            current_sample_position = sample_details[index_audio_data]
            index_audio_data += 1
            #print (len(index_audio_data))

            absolute_value = 1
            if (current_sample_position < 0):
                current_sample_position =- current_sample_position
                absolute_value = -1

            # & in Python represents Bitwise AND
            # | in Python represents Bitwise OR
            # The bitwise AND with the masking bits defined above turns the LSB of current
            # sample position to zero. Bitwise OR will replace these LSB bits with the
            # the next set of bits from data file
            new_sample = absolute_value * ((current_sample_position & masking) | current_data)

            new_audio_buffer.append(struct.pack(sample_quality[-1], new_sample))
        
        # This is where it errors out meaning condition is not met and status is still false + never ending loop
        if ((index_file_data // 8 >= len(data_file)) and (buffer_len <= 0)):
            status = True
            print (status)
                

    # This loop refers to the rest of the untouched samples (when data file has been embedded via LSB and there are still untouched samples)
    # This loop will then just append the rest of the samples back into the new audio buffer which will be written to the new audio file
    while(index_audio_data < len(sample_details)):
        new_audio_buffer.append(struct.pack(sample_quality[-1], sample_details[index_audio_data]))
        index_audio_data += 1

    #print (len(new_audio_buffer))
    x = audio_carrier.split("/")
    fname = x[-1]
    file_name = fname.split('.')[0] + "_NEW.wav"
    output_file = directory + "/" + file_name

    # Hidden File name
    y = dataF.split("/")
    hidden_file_name = y[-1]
    
    new_audio = w.open(output_file, "w")
    new_audio.setparams(data)
    new_audio.writeframes(b"".join(new_audio_buffer))
    new_audio.close()
    print ("File Encoded")

    # Now we want to add audio tags to the file for the sender to verify that this file does contain a data file
    new_audio_file = taglib.File(output_file)
    # FILE_TYPE == 1 --> This is an audio file that contains the hidden data / if not 1 --> then reg audio file
    new_audio_file.tags["FILE_TYPE"] = "1"
    new_audio_file.tags["FILE_SIZE"] = str(file_size)
    new_audio_file.tags["HIDDEN_FILENAME"] = hidden_file_name
    new_audio_file.tags["STORAGE_FILE_SPACE"] = str(lsb_space)
    new_audio_file.save()
    
    
    endTime = time.ctime(time.time())
    finish = time.time()
    print ("Start Time: " + str(startTime) + " - End Time: " + str(endTime))
    secondsToFinish = finish - start
    print ("Without using threads, it took: " + str(secondsToFinish) + " seconds to embed the datafile.")



def decode(audio_file, directory):

    # indexes --> bit representation of how much of the file is processed
    index_file_data = bytearray()
    index_audio_data = 0

    current_buffer = 0
    buffer_len = 0

    # I want to retrieve the tags of the audio file and verify it is in fact
    recieved_audio = taglib.File(audio_file)

    if (not int(recieved_audio.tags["FILE_TYPE"][0])):
        raise ValueError("This is a regular audio file")

    data_file = str(recieved_audio.tags["HIDDEN_FILENAME"][0])  # C:/Users/Khang/Documents/BCIT Semester 8/Project/file.all
    datafile_size = int(recieved_audio.tags["FILE_SIZE"][0])
    lsb_space = int(recieved_audio.tags["STORAGE_FILE_SPACE"][0])

    recieved_audio.save()
    
    #  Initialize audio file by calling the AudioDiagnostics Class
    file = audio_framework.AudioDiagnostics(audio_file)

    print (audio_file + " file has been opened")

    #  Once we intialize the audio file, grab the parameters --> getparams()
    data = file.get_frame_segments()

    # Get the total number of channels in audio file --> return 2 for stereo
    channels = file.get_num_channels()
    print("Total Number of Channels: " + str(channels))

    # Gets the sample width/bit width (the number of bytes per sample)
    # A frame consists of samples. There is one sample per channel, per frame. Every wav file has a sample width
    sample_width = file.get_num_samplew()
    print ("Sample Width: " + str(sample_width))

    # Get the total number of frames
    total_frames = file.get_audio_frames()
    print ("Total Number of Frames in Audio File: " + str(total_frames))

    # Calculates the total number of samples in the audio file
    total_samples = total_frames * channels
    print ("Total number of samples: " + str(total_samples))
    

    # The width of a sample defines the number of bits required to represent the value on a storage medium
    # Typical Wav File --> Stores audio using stereo 16-bit samples (Highest Quality) or 8-bits (Lowest Quality for file size)
    # If sample width is 1 byte == 8 bits --> that means they are unsigned 8 bit
    # If sample width is 2 bytes == 16 bits --> means signed 16 bit 
    if(sample_width == 1):
        sample_quality = "{}B".format(total_samples) # represented through byte form
        # (1 << 8) == shift 1 binary (0001) to the left by 8 bits
        min_masking_sample = -(1 << 8)
    elif(sample_width == 2):
        sample_quality = "{}h".format(total_samples) # Represented through hexadecimal width
        # (1 << 15) == shift 1 binary (0000 0001) to the left 15 bits --> 1000 0000 0000 0000 = 32768 decimal
        min_masking_sample = -(1 << 15)
        #print (sample_quality)
    else:
        raise ValueError("File has unsupport bit-depth that can store a single bit of the datafile")

    # Now we want to put all the samples loaded from the audio file into a list according
    # to the format string sample_quality
    sample_details = list(struct.unpack(sample_quality, file.read_audio_frames(total_frames)))
    # We want to extract the LSB 
    mask = (1 << lsb_space) - 1
    hidden_filename = directory + "/" + data_file
    hidden_file = open(hidden_filename, "wb+")

    while (datafile_size > 0):
        sample_data = sample_details[index_audio_data]
        if (sample_data != min_masking_sample):
            # we take the current buffer and increment --> value of the bytes retrieved from data file in binary performing a bitwise AND
            # Now we take that new binary value and perform a bit shift (buffer_len) to the left
            current_buffer += (abs(sample_data) & mask) << buffer_len
            buffer_len += lsb_space
            
        index_audio_data += 1

        while (buffer_len >= 8 and datafile_size > 0):
            # now we will iterate through the audio frames and check for hidden data file bytes
            # then add it to the bytearray  and decrement the file size to inspect
            data_position = current_buffer % (1 << 8)
            # Shift current buffer right by 8
            current_buffer >>= 8
            buffer_len -= 8
            index_file_data += struct.pack('1B', data_position)
            datafile_size -= 1
    
    hidden_file.write(index_file_data)
    hidden_file.close()
    print ("File decoded")
    return hidden_filename
    


'''
Function:embed_thread
Purpose: Uses multi-threading to start embedding the data file into the audio file

def embed_thread(audioC, dataF, directory):
    try:
        thread = threading.Thread(target=embed, args=(audioC, dataF, directory))
        #  now since this is a server that should always stay online, if a thread was to be killed
        #  the daemon should still be active for other clients
        thread.setDaemon(True)
        thread.start()
        
    except KeyboardInterrupt:
        print ("You have exited the program")
        sys.exit()'''


# Function:embed_thread
# Purpose: Uses multi-threading to start embedding the data file into the audio file
'''
def decode_thread(audio_file, directory):
    try:
        thread = threading.Thread(target=decode, args=(audio_file, directory))
        #  now since this is a server that should always stay online, if a thread was to be killed
        #  the daemon should still be active for other clients
        thread.setDaemon(True)
        thread.start()
        
    except KeyboardInterrupt:
        print ("You have exited the program")
        sys.exit()'''

#embed(audioC, dataF, directory)
#FILENAME = decode(audioC, directory)
#print(FILENAME)
