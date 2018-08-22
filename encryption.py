from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import ast

#returns a tuple with (private key, public key)
def generate_keyset():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()
def encrypt_session(text, public_key):
    #return the AES key encrypted, the nonce, the tag and the encripted data
    #tag is for validating the data
    data = text.encode("utf-8")
    recipent_key = RSA.import_key(public_key)
    #generate a session key to encrypt the data with AES
    session_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(recipent_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    #encrypt the text data with AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    return (session_key, (enc_session_key, cipher_aes.nonce, tag, ciphertext))

def encrypt_data(data, session_key):
    #encrypts the data with the from encrypt_session generated session key in AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    return (cipher_aes.nonce, tag, ciphertext)

#for de and encrypting text in utf8 format
def encrypt_text(text, session_key):
    data = text.encode("utf8")
    return encrypt_data(data, session_key)

def decrypt_text(nonce, tag, text, session_key):
    data = text.encode("utf8")
    return decrypt_data(nonce, tag, data, session_key)
def decrypt_text(message, session_key):
    data = message[2].encode("utf8")
    return decrypt_data(message[0], message[1], data, session_key)

def decrypt_data(nonce, tag, data, session_key):
    #same as encrypt_data but decrypts it
    cipher_aes = AES.new(session_key,AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data
def decrypt_data(message, session_key):
    rcipher_aes = AES.new(session_key,AES.MODE_EAX, message[0])
    data = cipher_aes.decrypt_and_verify(message[2], message[1])
    return data
def decrypt_session(enc_session_key, nonce, tag, ciphertext, p_key):
    private_key = RSA.import_key(p_key)
    #decrypt the AES Key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    #decrypt the Data with the decrypted AES Key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext,tag)
    return data.decode("utf8"), session_key

    #for easier use: message_list contains the parameter returned from decrypt in the same order in a list strcuture
def decrypt_session(message_list, p_key):
    private_key = RSA.import_key(p_key)
    #decrypt the AES Key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(message_list[0])

    #decrypt the Data with the decrypted AES Key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, message_list[1])
    data = cipher_aes.decrypt_and_verify(message_list[3],message_list[2])
    return data.decode("utf8"), session_key
