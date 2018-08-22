from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import ast
import pickle
#returns a tuple with (private key, public key)
def generate_keyset():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()
def encrypt_session(version, public_key):
    #return the AES key encrypted, the nonce, the tag and the encripted data
    #tag is for validating the data
    data = version.to_bytes(4, byteorder="big")
    recipent_key = RSA.import_key(public_key)
    #generate a session key to encrypt the data with AES
    session_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(recipent_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    #encrypt the text data with AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    #encryption data for transmission getting serialized
    enc_data = pickle.dumps((enc_session_key, cipher_aes.nonce, tag, ciphertext))
    return (session_key, enc_data)

def encrypt_data(data, session_key):
    #encrypts the data with the from encrypt_session generated session key in AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    enc_data = pickle.dumps((cipher_aes.nonce, tag, ciphertext))
    return enc_data

#for de and encrypting text in utf8 format
def encrypt_text(text, session_key):
    data = text.encode("utf8")
    return encrypt_data(data, session_key)

def decrypt_text(enc_data, session_key):
    (nonce, tag, ciphertext) = pickle.loads(enc_data)
    cipher_aes = AES.new(session_key,AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return str(data,"utf8")

def decrypt_data(enc_data, session_key):
    (nonce, tag, ciphertext) = pickle.loads(enc_data)
    #same as encrypt_data but decrypts it
    cipher_aes = AES.new(session_key,AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data

def decrypt_session(enc_data, p_key):
    enc_session_key, nonce, tag, ciphertext = pickle.loads(enc_data)
    private_key = RSA.import_key(p_key)
    #decrypt the AES Key with RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    #decrypt the Data with the decrypted AES Key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext,tag)
    return int.from_bytes(data, byteorder="big"), session_key
