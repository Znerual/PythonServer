import socket
from encryption import encrypt_data, decrypt_data, encrypt_text, decrypt_text
#Defines the protocoll for transferring data
#defines the chunk size and handels the chunking of receiving data
#Max lengh of data to be sent is covered by an unsigned int (4 byte)
def send_data(data, usocket):
    preData = len(data).to_bytes(4, byteorder="big")
    usocket.send(preData + data)

def send_text(text, usocket):
    data = text.encode("utf8")
    send_data(data, usocket)

def send_validation_encrypted(usocket, session_key, validate=True):
    if validate:
        send_text_encrypted("valid", usocket, session_key)
    else:
        send_text_encrypted("error", usocket, session_key)
def send_text_encrypted(text, usocket, session_key):
    enc_data = encrypt_text(text, session_key)
    send_data(enc_data, usocket)

def send_data_encrypted(data, usocket, session_key):
    enc_data =encrypt_data(data, session_key)
    send_data(enc_data, usocket)

def recv_data(usocket):
    length = int.from_bytes(usocket.recv(4), byteorder="big")
    chunk_size = length
    data = bytearray()
    if length > 1024:
        chunk_size = 1024
    while (length > 0):
        data.extend(usocket.recv(chunk_size))
        length -= chunk_size
    return bytes(data)
def recv_text(usocket):
    data = recv_data(usocket)
    return str(data,"utf8")
def recv_data_encrypted(usocket, session_key):
    enc_data = recv_data(usocket)
    data = decrypt_data(enc_data, session_key)
    return data
def recv_text_encrypted(usocket, session_key):
    enc_text = recv_data(usocket)
    text = decrypt_text(enc_text, session_key)
    return text
def recv_validation_encrypted(usocket, session_key):
    validation = recv_text_encrypted(usocket, session_key)
    if validation == "valid":
        return True
    else:
        return False
