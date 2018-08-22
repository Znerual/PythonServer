import socket
import pickle
from encryption import generate_keyset, decrypt_session, encrypt_session
from protocoll import send_data, recv_data, send_text

server_addr = (socket.gethostbyname(socket.gethostname()), 5555)
#connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.settimeout(7)
client_socket.connect(server_addr)

#generate the keyset
private_key, public_key = generate_keyset()

#send the public key to the server

send_data(public_key, client_socket)
#client_socket.send(public_key)

#wait for encrypted response
messageData = recv_data(client_socket)

#while True:
#    daten, addr = client_socket.recvfrom(1024)
#    messageData += daten
#    if not daten:
#        break

enc_message = pickle.loads(messageData)
message, session_key = decrypt_session(enc_message, private_key)
print(message)

send_text("Funktioniert", client_socket)
client_socket.close()
del client_socket
