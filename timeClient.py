import socket
from encryption import generate_keyset, decrypt_session, encrypt_session
from protocoll import send_data, recv_data, send_text, send_text_encrypted

VERSION_NUMBER = 1

def checkVersion(versionNumber):
    if (versionNumber < VERSION_NUMBER):
        print("Bitte updaten")

server_addr = (socket.gethostbyname(socket.gethostname()), 5555)
#connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_addr)

#generate the keyset
private_key, public_key = generate_keyset()

#send the public key to the server
send_data(public_key, client_socket)

#wait for encrypted response with the server Version number
messageData = recv_data(client_socket)
version, session_key = decrypt_session(messageData, private_key)
checkVersion(version)
print(version)

send_text_encrypted("Funktioniert", client_socket, session_key)
client_socket.close()
del client_socket
