#! /usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import random
from Crypto.Signature import PKCS1_v1_5

import base64
import hashlib
import os
import zipfile


'''
This script uses a hybrid cryptosystem that fufills my two critical features
a) Data Encryption that ciphers the plain text of a file --> AES Encryption
b) Data Security that uses public/private keys--> RSA Keys
        - The Sender will use the shared public key to lock the file
        - The reciever will then use their private key to unlock the file
'''

#  Opening Parameters
locked_file = "C:/Users/Khang/Documents/BCIT Semester 8/Project/file.all"
directory = "C:/Users/Khang/Documents/GitHub"
#locked_file = "KhangTran_Resume.all"
pwd = "bitchassFuck!"

#  The reciever will decrypt the file via their private key.
private_key = "private_key.pem"    # These values will change when the gui adds the browse option
public_key = "public_key.pem"


# This hashes the key string literal via SHA-256 (Secure Hash Algorithm) which generates
# a 32 byte (256 bit) hash that cannot be decrypted back. This is an implementation of
# secure form of a signature to indicate the reciever that this is from a trusted source
password = hashlib.sha256(pwd.encode('utf-8')).digest()


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
def cleanup(sigFile, keyFile, cipher_file):
    os.remove(sigFile)
    os.remove(keyFile)
    os.remove(cipher_file)
    

def signature_verify(public_key, input_file):

    global sig_file_name
    
    # Now we want to generate decrypted file's SHA256
    decrypted_hash = SHA256.new()
    decrypted_hash.update(open(input_file + ".docx.enc","rb").read())

    # Now we want to read in public key and check with signature
    keyPair = RSA.importKey(open(public_key,"rb").read())
    # The key to use to sign or verify the message
    keyVerify = PKCS1_v1_5.new(keyPair.publickey())

    # Get signature file
    #x = input_file.split("/")
    #fileN = x[-1]
    #file_path = input_file.rsplit('/',1)[0]
    #sig_file_name = file_path + "/" + fileN.split('.')[0] + ".sig"
    #sig_file_name = input_file + fileN.split('.')[0] + ".sig"
    sig_file_name = input_file.split('.')[0] + ".sig"

    # Now we want to verify the deciphered key and authenticate signature,
    # If not authenticated, will exit program
    if (keyVerify.verify(decrypted_hash, open(sig_file_name, "rb").read())):
        print ("This sender is authenticated via their signature!")
        print ("Here is the hash signature: " + decrypted_hash.hexdigest())
    else:
        print ("This sender failed authentication and cannot be trusted!")


'''
Function: key_reader
Purpose: Creates a .key file that will be used for part (a) of the
         hybrid crypto system --> Security
'''
def key_verify(private_key, password, input_file):
    
    global key_file_name
    default_length = 256 #default chunk size of a RSA Key of 1024 Bytes  (256 - 2) - 2(32)
    offset = 0
    res = []
    status = False

    # read in public key to encrypt AES key
    #try:
    privKey = open(private_key,"rb").read()
    
    try:
        keyPair = RSA.import_key(privKey, passphrase = password)
        keyDecipher = PKCS1_OAEP.new(keyPair)
        print ("Password Accepted")
        # Now we want to save this in a .key file that acts as a form of authenticatiom
        # system for the application
        key_file_name = input_file.split('.')[0] + ".key"
        
        key_file = open(key_file_name, 'rb')
        
        # will read the first 16 characters of stored data in the file
        iv = key_file.read(16)
        
        while 1:
            chunk = key_file.read(default_length)
            if not chunk: break
            res.append(keyDecipher.decrypt(chunk))

        key_file.close()
        key = b''.join(res)
        status = True

        return key, iv, status

    except ValueError:
        status = False
        print ("Wrong Password")
        return status


'''
Function: decrypt
Purpose: Decrypts the encrypted file
'''
def decrypt(private_key, public_key, password, locked_file):

    global cipher_file
    
    #ciphertext = base64.b64decode(ciphertext)
    
    # remember as the reciever, we're using our private keys to unlock
    key, iv, status = key_verify(private_key, password, locked_file)
    
    # now we want to get just the filename without any extension
    keyDecipher = AES.new(key, AES.MODE_CBC, iv )
    '''
    x = locked_file.split("/")
    fileN = x[-1]
    file_path = input_file.rsplit('/',1)[0]
    file_name = file_path + "/" + fileN.split('.')[0]
    cipher_file = file_name + ".enc" '''
    cipher_file = locked_file + ".docx.enc"

    with open(cipher_file,'rb') as inFile:
        encrypted_text = inFile.read()

    encrypted_text = base64.b64decode(encrypted_text)
    
    plain_text = keyDecipher.decrypt(encrypted_text[AES.block_size:-1])
    padding_size = encrypted_text[-1] * (-1)
    plain_text = plain_text[:padding_size]
    
    f = open(locked_file + ".docx", "wb")
    f.write(plain_text)
    f.close()

    signature_verify(public_key, locked_file)


'''
Function Name: extraction
Purpose: Extracts the components of the all file
'''
def extraction(input_file):
    
    # open the input file
    f = zipfile.ZipFile(input_file + ".all", "r")
    
    #extract all files in this compression
    f.extractall()
        

a = locked_file.split("/")
file_name = a[-1]
locked_filename = file_name.split('.')[0]

# We first need to extract the files from the all file sent by the sender
extraction(locked_file)

# Now that all files are extracted, we want to decrypt the file
decrypt(private_key, public_key, password, locked_filename)

# Now that the file has been retrieved, we want to remove all unnecessary files
cleanup(sig_file_name, key_file_name, cipher_file)

print ("File Decrypted!")
