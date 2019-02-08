import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


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

def encrypt( raw , key, key_size=128) :
    raw, padding_size = pad(raw)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new(key, AES.MODE_CBC, iv )
    enc_bytes = base64.b64encode(iv + cipher.encrypt(raw) + bytes([padding_size]))
    return enc_bytes

def decrypt( enc , key ):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    plain = cipher.decrypt(enc[AES.block_size:-1])
    padding_size = enc[-1] * (-1)
    return plain[:padding_size]

'''
Function Name: file_encryption
Purpose: Encrypts the given file via AES CBC mode with the given password
'''
def file_encryption(password, input_file, output_file):
    
    # File Encryption
    with open(input_file,'rb') as inFile:
        plaintext = inFile.read()
    encrypted = encrypt(plaintext, password)

    # Now we want to write to file
    with open(output_file,'wb') as outFile:
        outFile.write(encrypted)

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



#  Opening Parameters
iFile = "C:/Users/Khang/Documents/KhangTran_Resume.docx"
oFile = "C:/Users/Khang/Documents/KhangTran_Resume.enc"
pwd = "bitchassFuck!"

# This hashes the key string literal via SHA-256 (Secure Hash Algorithm) which generates
# a 32 byte (256 bit) hash that cannot be decrypted back. This is an implementation of
# secure form of public/private key process with the given password
password = hashlib.sha256(pwd.encode('utf-8')).digest()

#file_encryption(password,iFile,oFile)
file_decryption(password,oFile,iFile)
