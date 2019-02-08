import base64
import hashlib
import os
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import zipfile

'''
This script uses a hybrid cryptosystem that fufills my two critical features
a) Data Encryption that ciphers the plain text of a file --> AES Encryption
b) Data Security that uses public/private keys--> RSA Keys
        - The Sender will use the shared public key to lock the file
        - The reciever will then use their private key to unlock the file
'''

#  Opening Parameters
#iFile = "C:/Users/Khang/Documents/Job Hunting/KhangTran_Resume.docx"
#oFile = "C:/Users/Khang/Documents/KhangTran_Resume.enc"
iFile = "KhangTran_Resume.docx"
oFile = "KhangTran_Resume.enc"
pwd = "bitchassFuck!"

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
def cleanup(keyFile,encrypted_file):
    os.remove(keyFile)
    os.remove(encrypted_file)


'''
Function: key_generator
Purpose: Creates a .key file that will be used for part (a) of the
         hybrid crypto system --> Security
'''
def key_generator(public_key, iv, input_file, password):
    
    global key_file_name

    # read in public key to encrypt AES key
    keyPair = RSA.importKey(open(public_key,"r").read())
    keyCipher = PKCS1_OAEP.new(keyPair.publickey())
    
    # Now we want to save this in a .key file that acts as a form of authenticatiom
    # system for the application
    #x = input_file.split("/")
    #fileN = x[-1]
    #file_path = input_file.rsplit('/',1)[0]
    #key_file_name = file_path + "/" + fileN.split('.')[0] + ".key"
    key_file_name = input_file.split('.')[0] + ".key"

    key_file = open(key_file_name, 'w')
    hello = keyCipher.encrypt(password)
    key_file.write(str(iv + keyCipher.encrypt(password)))
    key_file.close()
    
    print ("Key File Created: " + key_file_name)


'''
Function: encrypt
Purpose: Encrypts the data file via AES-CBC mode and calls on key generator func
'''
def encrypt( private_key, public_key, raw , key, input_file, key_size=128) :
    raw, padding_size = pad(raw)
    iv = Random.new().read( AES.block_size )
    # This will call the function key_generator that will use the public
    # key to generate the key used for the AES encryption
    ciphered_key = key_generator(public_key, iv, input_file, key)
    cipher = AES.new(key, AES.MODE_CBC, iv )
    enc_bytes = base64.b64encode(iv + cipher.encrypt(raw) + bytes([padding_size]))
    return enc_bytes


'''
Function: decrypt
Purpose: Decrypts the encrypted file
'''
def decrypt( enc , key ):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    plain = cipher.decrypt(enc[AES.block_size:-1])
    padding_size = enc[-1] * (-1)
    return plain[:padding_size]


def hybrid_crypto(keyFile, encrypted_datafile):
    #a = encrypted_datafile.split("/")
    #fileNam = a[-1]
    #filePath = encrypted_datafile.rsplit('/',1)[0]
    #final_file_name = filePath + "/" + fileNam.split('.')[0] + ".all"
    final_file_name = encrypted_datafile.split('.')[0] + ".all"
    
    f = zipfile.ZipFile(final_file_name, "w")

    f.write(keyFile)
    f.write(encrypted_datafile)

    f.close()

    cleanup(keyFile, encrypted_datafile)

    
'''
Function Name: file_encryption
Purpose: Encrypts the given file via AES CBC mode with the given password
'''
def file_encryption(private_key, public_key, password, input_file, output_file):

    # File Encryption
    with open(input_file,'rb') as inFile:
        plaintext = inFile.read()
    encrypted = encrypt(private_key, public_key, plaintext, password, input_file)

    # Now we want to write to file
    with open(output_file,'wb') as outFile:
        outFile.write(encrypted)

    # Now we want to merge the key file and encrypted cipher together into one file to send
    hybrid_crypto(key_file_name, output_file)
    
    print ("File Encrypted!")
    


'''
Function Name: file_decryption
Purpose: Decrypts the given file via AES CBC mode with the given password
'''
def file_decryption(password, input_file, output_file):

    #File Decryption
    with open(input_file,'rb') as inFile:
        ciphertext = inFile.read()
    decrypted = decrypt(ciphertext, password)
    
    # Now we want to write to file
    with open(output_file,'wb') as outFile:
        outFile.write(decrypted)

    print ("File Decrypted!")



file_encryption(priv_key, pub_key, password, iFile, oFile)
#file_decryption(password,oFile,iFile)
