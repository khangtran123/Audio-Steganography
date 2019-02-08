import base64

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import zlib

'''
def lockFile(key,f):
    rsa_key = RSA.importKey(key)
    



# Now we want to retrieve the private key to lock the file
file = open('private_key.pem','rb')
pub_key = file.read()
file.close()

# The data file to lock
dfile = open('C:/Users/Khang/Documents/Job Hunting/KhangTran_Resume.docx','rb')
data_file = dfile.read()
dfile.close()

# calls the lockFile function to lock the file
lockFile(pub_key,data_file)

# now we want to write to a new file
'''
#Our Encryption Function
def encrypt_blob(blob, public_key):
    #Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    #compress the data first
    blob = zlib.compress(blob)

    #In determining the chunk size, determine the private key length used in bytes
    #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
    #in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted =  ""

    while not end_loop:
        #The chunk
        chunk = blob[offset:offset + chunk_size]

        #If the data chunk is less then the chunk size, then we need to add
        #padding with " ". This indicates the we reached the end of the file
        #so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += " " * (chunk_size - len(chunk))

        #Append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

    #Base 64 encode the encrypted file
    return base64.b64encode(encrypted)

#Use the public key for encryption
fd = open("public_key.pem", "rb")
public_key = fd.read()
fd.close()

#Our candidate file to be encrypted
fd = open("C:/Users/Khang/Pictures/ben-stiller-omaze.jpg", "rb")
unencrypted_blob = fd.read()
fd.close()

encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

#Write the encrypted contents to a file
fd = open("C:/Users/Khang/Pictures/ben-stiller-omaze_encrypted.jpg", "wb")
fd.write(encrypted_blob)
fd.close()

print ("File Locked!")







