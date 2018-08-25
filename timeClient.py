import socket
import logging
import ClientServingThread
from encryption import generate_keyset, decrypt_session, encrypt_session
from protocoll import *
from passwordmanagement import hash

VERSION_NUMBER = 1

def checkVersion(versionNumber):
    if (versionNumber < VERSION_NUMBER):
        print("Bitte updaten")

server_addr = (socket.gethostbyname(socket.gethostname()), 5555)
#connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(True)
client_socket.connect(server_addr)

#generate the keyset
private_key, public_key = generate_keyset()

#send the public key to the server
send_data(public_key, client_socket)
print("Send key")

#wait for encrypted response with the server Version number
messageData = recv_data(client_socket)
version, session_key = decrypt_session(messageData, private_key)
checkVersion(version)
print(version)

#validate the Version
send_validation_encrypted(client_socket, session_key)
print("Send validation")
#wait for Password Salt
salt = recv_data_encrypted(client_socket, session_key)
print("Got salt" + str(salt,"utf8"))
#input password from user, for debugging we skip over this step
password = "1234"

#Generate the passwort hash with the salt and send it to the server
pwd_hash = hash(password.encode("utf8"), salt)
print(pwd_hash)
send_data_encrypted(pwd_hash, client_socket, session_key)
print("Send hash")
#wait for validation
valid = recv_validation_encrypted(client_socket, session_key)
if not valid:
    print("Fail")
    raise SystemExit
print("Got validation")

#send_text_encrypted("Funktioniert", client_socket, session_key)
client_socket.close()
del client_socket
