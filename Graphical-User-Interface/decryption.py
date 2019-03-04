#! /usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import random
from Crypto.Signature import PKCS1_v1_5
from dictionary import getConfigFile

import base64
import hashlib
import os
import zipfile
import sys


'''
This script uses a hybrid cryptosystem that fufills my two critical features
a) Data Encryption that ciphers the plain text of a file --> AES Encryption
b) Data Security that uses public/private keys--> RSA Keys
        - The Sender will use the shared public key to lock the file
        - The reciever will then use their private key to unlock the file
'''
#locked_file, directory, private_key, public_key, pwd = getConfigFile()

#  Opening Parameters
#unlocked_file = "C:/Users/Khang/Documents/demo/file.all"
#directory = "C:/Users/Khang/Documents/demo"
#pwd = "TranFamily1!"

#  The reciever will decrypt the file via their private key.
#private_key = "private_key.pem"    # These values will change when the gui adds the browse option
#public_key = "public_key.pem"


# This hashes the key string literal via SHA-256 (Secure Hash Algorithm) which generates
# a 32 byte (256 bit) hash that cannot be decrypted back. This is an implementation of
# secure form of a signature to indicate the reciever that this is from a trusted source
#password = hashlib.sha256(pwd.encode('utf-8')).digest()


'''
Function name: pad
Purpose: Since CBC mode allows you to encrypt bigger bits of data in a
         given block, padding allows us to scale the data to fit in the
         default block size.

         So, if you have 4ℓ bits of data to encrypt,
         for ℓ the block size of your cipher, then you're fine. But what
         if you have 4ℓ+5 bits of data? (I am assuming the blocksize
         does not divide 5.) Then you need to pad the data with ℓ−5 bits
         of padding in order to end up with a multiple of the blocksize
         of data ready for encryption with your mode of operation.
'''
def pad(s):
    padding_size = AES.block_size - len(s) % AES.block_size
    return s + b"\0" * padding_size, padding_size


'''
Function: cleanup
Purpose: Remove the Key File generated and the Encrypted Data File
'''
def cleanup(locked_file, sigFile, keyFile, cipher_file):
    os.remove(locked_file)
    os.remove(sigFile)
    os.remove(keyFile)
    os.remove(cipher_file)
    

def signature_verify(public_key, output_file):

    global sig_file_name


    # Now we want to generate decrypted file's SHA256
    with open(output_file,'rb') as hashed_file:
        hash_content = hashed_file.read()
    
    decrypted_hash = SHA256.new()
    decrypted_hash.update(hash_content)

    # Now we want to read in public key and check with signature
    with open(public_key,"rb") as inKey:
        key_content = inKey.read()
    
    key = RSA.importKey(key_content)
    # The key to use to sign or verify the message
    keyVerify = PKCS1_v1_5.new(key.publickey())

    # Get signature file
    file_path = output_file.rsplit('/',1)[0]
    
    f = os.listdir(file_path)
    if len(f) > 0:
        for file in os.listdir(file_path):
            if file.endswith('.sig'):
                print (".sig File found")
                sig_file_name = file_path + "/" + file
                # Now we want to verify the deciphered key and authenticate signature,
                # If not authenticated, will exit program
                with open(sig_file_name,"rb") as sigFile:
                    sig_content = sigFile.read()
                print ("HELLOW")
                if (keyVerify.verify(decrypted_hash, sig_content)):
                    print ("This sender is authenticated via their signature!")
                    print ("Here is the hash signature: " + decrypted_hash.hexdigest())
                    signature_status = True
                    return signature_status
                else:
                    raise ValueError("This sender failed authentication and cannot be trusted!")
                    signature_status = False
                    return signature_status


'''
Function: key_verify
Purpose: Creates a .key file that will be used for part (a) of the
         hybrid crypto system --> Security
'''
def key_verify(private_key, password, input_file):
    
    global key_file_name
    default_length = 256 #default chunk size of a RSA Key of 1024 Bytes  (256 - 2) - 2(32)
    offset = 0
    res = []

    privKey = open(private_key,"rb").read()

    # read in public key to decrypt AES key
    keyPair = RSA.import_key(privKey, passphrase = password)
    keyDecipher = PKCS1_OAEP.new(keyPair)

    
    # Now we want to save this in a .key file that acts as a form of authenticatiom
    # system for the application
    #key_file_name = input_file.split('.')[0] + ".key"
    file_path = input_file.rsplit('/',1)[0]

    f = os.listdir(file_path)
    if len(f) > 0:
        for file in os.listdir(file_path):
            if file.endswith('.key'):
                key_file_name = file_path + "/" + file
                key_file = open(key_file_name, 'rb')
    
                # will read the first 16 characters of stored data in the file
                iv = key_file.read(16)
                while 1:
                    chunk = key_file.read(default_length)
                    if not chunk: break
                    res.append(keyDecipher.decrypt(chunk))

                key_file.close()
                key = b''.join(res)

                return key, iv


'''
Function: decrypt
Purpose: Decrypts the encrypted file
'''
def decrypt(private_key, public_key, password, unlocked_file, directory):

    global cipher_file
    global sig_verification
    
    #ciphertext = base64.b64decode(ciphertext)
    file_path = unlocked_file.rsplit('/',1)[0]
    f = os.listdir(file_path)
    if len(f) > 0:
        for file in os.listdir(file_path):
            if file.endswith('.enc'):
                cipher_file = file_path + "/" + file
                # This should be a section that checks for passphrase
                # If yes then proceed to key_verify
                # If no, return status so the gui can have a popup dialog saying incorrect password
                # remember as the reciever, we're using our private keys to unlock
                key, iv = key_verify(private_key, password, cipher_file)
                # now we want to get just the filename without any extension
                keyDecipher = AES.new(key, AES.MODE_CBC, iv )
                
                with open(cipher_file,'rb') as inFile:
                    encrypted_text = inFile.read()

                encrypted_text = base64.b64decode(encrypted_text)
                
                plain_text = keyDecipher.decrypt(encrypted_text[AES.block_size:-1])
                padding_size = encrypted_text[-1] * (-1)
                plain_text = plain_text[:padding_size]
                
                output_file = directory + "/" + file.split('.')[0] + "." + file.split('.')[1]
                
                f = open(output_file, "wb")
                f.write(plain_text)
                f.close()

                sig_verification = signature_verify(public_key, output_file)
                # Now that the file has been retrieved, we want to remove all unnecessary files
                #cleanup(locked_file, sig_file_name, key_file_name, cipher_file)
                return sig_verification
            else:
                continue


'''
Function Name: extraction
Purpose: Extracts the components of the all file
'''
def extraction(unlocked_file):

    path = unlocked_file.rsplit('/',1)[0]
    file_path = path + "/"
    
    # open the input file
    f = zipfile.ZipFile(unlocked_file, "r")
    
    #extract all files in this compression
    f.extractall(file_path)
        
    

'''
Function: verification()
Parameters: private_key, public_key, password, locked_file, directory
Purpose: Verify the password provided by the user to even begin file
         extraction and retrieval

'''
def verification(private_key, public_key, password, unlocked_file, directory):
    
    global sig_verification

    privKey = open(private_key,"rb").read()
    
    try:

        # Load RSA Key and decrypt it with given password
        # if wrong password, RSA lib will throw ValueError
        # exception
        keyPair = RSA.import_key(privKey, passphrase = password)
        keyDecipher = PKCS1_OAEP.new(keyPair)

        print ("Password Accepted")
        print ("Commencing File Extraction")

        # We first need to extract the files from the all file sent by the sender
        extraction(unlocked_file)

        print ("File Extraction Completed")
        print ("Commencing File Decryption")

        # Now that all files are extracted, we want to decrypt the file
        decrypt(private_key, public_key, password, unlocked_file, directory)
        
        print ("File Decrypted")
        status = True
        return status, sig_verification
        
    except ValueError:
        print ("Wrong Password")
        status = False
        sig_verification = False
        return status, sig_verification 


# We want to call on this function to verify if the provided password works
#status, sig_verification = verification(private_key, public_key, password, unlocked_file, directory)

