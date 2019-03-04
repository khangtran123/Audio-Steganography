#! /usr/bin/python3

from Crypto.PublicKey import RSA
import hashlib

def create_keys(pwd):

    # Calls RSA library to generate a random RSA key that meets 4096 bits in length
    key = RSA.generate(2048)

    #dataF, audioC, save_to_dir, pwd = getConfigFile()

    #pwd = "TranFamily1!"

    # This hashes the key string literal via SHA-256 (Secure Hash Algorithm) which generates
    # a 32 byte (256 bit) hash that cannot be decrypted back. This is an implementation of
    # secure form of public/private key process with the given password
    password = hashlib.sha256(pwd.encode('utf-8')).digest()

    # This is for the private key that the sender uses to lock the file (PEM File)
    # PKCS #8 is a standard syntax for storing private key information
    private_key = key.export_key("PEM",password)


    #This is the public key to share to the reciever that will unlock the file
    public_key = key.publickey().export_key()


    print ("Private Key Created!")
    privatekey_file = "private_key.pem"
    file_priv = open(privatekey_file, "wb")
    file_priv.write(private_key)
    file_priv.close()

    print ("Public Key Created!")
    publickey_file = "public_key.pem"
    file_pub = open(publickey_file, "wb")
    file_pub.write(public_key)
    file_pub.close()

    return privatekey_file, publickey_file

#create_keys()

