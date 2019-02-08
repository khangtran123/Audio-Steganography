import base64

from Crypto import Random
from Crypto.PublicKey import RSA
import hashlib


# Calls RSA library to generate a random RSA key that meets 4096 bits in length
key = RSA.generate(2048, e=65537)

pwd = "bitchassFuck!"

# This hashes the key string literal via SHA-256 (Secure Hash Algorithm) which generates
# a 32 byte (256 bit) hash that cannot be decrypted back. This is an implementation of
# secure form of public/private key process with the given password
password = hashlib.sha256(pwd.encode('utf-8')).digest()

# This is for the private key that the sender uses to lock the file (PEM File)
private_key = key.export_key(passphrase=password, pkcs=8)


#This is the public key to share to the reciever that will unlock the file
public_key = key.publickey().export_key()


print ("Private Key: " + str(private_key))
file_priv = open("private_key.pem", "wb")
file_priv.write(private_key)
file_priv.close()

print ("Public Key: " + str(public_key))
file_pub = open("public_key.pem", "wb")
file_pub.write(public_key)
file_pub.close()





