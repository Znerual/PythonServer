from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import ast

#returns a tuple with (private key, public key)
def generate_keyset():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()
def encrypt(text, public_key):
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

    return (enc_session_key, cipher_aes.nonce, tag, ciphertext)
def decrypt(enc_session_key, nonce, tag, ciphertext, private_key):
    #decrypt the AES Key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    #decrypt the Data with the decrypted AES Key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext,tag)
    return data.decode("utf8")

    #for easier use: message_list contains the parameter returned from decrypt in the same order in a list strcuture
def decrypt(message_list, private_key):
    #decrypt the AES Key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(message_list[0])

    #decrypt the Data with the decrypted AES Key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, message_list[1])
    data = cipher_aes.decrypt_and_verify(message_list[3],message_list[2])
    return data.decode("utf8")
