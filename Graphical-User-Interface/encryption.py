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
from dictionary import getConfigFile


'''
This script uses a hybrid cryptosystem that fufills my two critical features
a) Data Encryption that ciphers the plain text of a file --> AES Encryption
b) Data Security that uses public/private keys--> RSA Keys
        - The Sender will use the shared public key to lock the file
        - The reciever will then use their private key to unlock the file
'''
#dataF, audioC, save_to_dir, pwd = getConfigFile()

#  Opening Parameters
dataF = "C:/Users/Khang/Documents/Job Hunting/KhangTran_Resume.docx"
directory = "C:/Users/Khang/Documents/BCIT Semester 8/Project"
#oFile = "C:/Users/Khang/Documents/KhangTran_Resume.enc"
#iFile = "KhangTran_Resume.docx"
#oFile = "KhangTran_Resume.docx.enc"
pwd = "Losangles12!"

#  Sender encrypts the cipher with the reciever's public key and then the reciever will
#  decrypt the file via their private key.
priv_key = "private_key.pem"    # These values will change when the gui adds the browse option
pub_key = "public_key.pem"


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
def cleanup(sigFile, keyFile,encrypted_file):

    os.remove(sigFile)
    os.remove(keyFile)
    os.remove(encrypted_file)


def signature(private_key, password, input_file):

    global sig_file_name

    with open(input_file,'rb') as inFile:
        content = inFile.read()

    # Now we want to create a hash (SHA256 - to be compatible with AES)
    hash_content = SHA256.new(content)
    # Reading in private key to sign the file with the password input
    keyPair = RSA.import_key(open(private_key,"r").read(), passphrase=password)
    keySignature = PKCS1_v1_5.new(keyPair)

    # Now we want to save this in a .sig file that acts as a form of authentication
    # system for the application
    x = input_file.split("/")
    file_name = x[-1]
    sig_file_name = file_name.split('.')[0] + ".sig"

    f = open(sig_file_name, 'w')
    f.write(str(keySignature.sign(hash_content)))
    f.close()
    
    print ("Sig File Created: " + sig_file_name)


'''
Function: key_generator
Purpose: Creates a .key file that will be used for part (a) of the
         hybrid crypto system --> Security
'''
def key_generator(public_key, iv, input_file, password):
    
    global key_file_name

    #hashed = SHA256.new(str(random.getrandbits(2048)).encode('utf-8'))
    
    # read in public key to encrypt AES key
    keyPair = RSA.importKey(open(public_key,"rb").read())
    keyCipher = PKCS1_OAEP.new(keyPair.publickey())
    
    # Now we want to save this in a .key file that acts as a form of authenticatiom
    # system for the application
    x = input_file.split("/")
    file_name = x[-1]
    key_file_name = file_name.split('.')[0] + ".key"

    key_file = open(key_file_name, 'wb')
    key_file.write(iv + keyCipher.encrypt(password))
    key_file.close()
    
    print ("Key File Created: " + key_file_name)


'''
Function: encrypt
Purpose: Encrypts the data file via AES-CBC mode and calls on key generator func
'''
def encrypt( private_key, public_key, raw , key, input_file, key_size=128) :
    raw, padding_size = pad(raw)
    signature(private_key, key, input_file)
    iv = Random.new().read( AES.block_size )
    # This will call the function key_generator that will use the public
    # key to generate the key used for the AES encryption
    ciphered_key = key_generator(public_key, iv, input_file, key)
    cipher = AES.new(key, AES.MODE_CBC, iv )
    enc_bytes = base64.b64encode(iv + cipher.encrypt(raw) + bytes([padding_size]))
    return enc_bytes


def hybrid_crypto(sigFile, keyFile, file_name, encrypted_datafile, directory):
    
    final_file_name = directory + "/" + "file.all"

    '''
    # Just get the file name and not directory of sig, key, and file
    a = sigFile.split("/")
    signature = a[-1]

    key = encrypted_datafile

    b = encrypted_datafile.split("/")
    enc_file = b[-1]'''
    
    f = zipfile.ZipFile(final_file_name, "w")
    
    f.write(sigFile)
    f.write(keyFile)
    f.write(encrypted_datafile)

    f.close()

    cleanup(sigFile, keyFile, encrypted_datafile)

    
'''
Function Name: file_encryption
Purpose: Encrypts the given file via AES CBC mode with the given password
'''
def file_encryption(private_key, public_key, password, input_file, directory):

    # File Encryption
    with open(input_file,'rb') as inFile:
        plaintext = inFile.read()
    encrypted = encrypt(private_key, public_key, plaintext, password, input_file)

    a = input_file.split("/")
    file_name = a[-1]
    output_file = file_name + ".enc"
    
    # Now we want to write to file
    with open(output_file,'wb') as outFile:
        outFile.write(encrypted)

    # Now we want to merge the signature file, key file and encrypted cipher together into one file to sends
    hybrid_crypto(sig_file_name, key_file_name, file_name, output_file, directory)
    
    print ("File Encrypted!")
    


#file_encryption(priv_key, pub_key, password, dataF, directory)
