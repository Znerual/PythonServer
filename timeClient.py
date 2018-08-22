import socket
import pickle
from encryption import generate_keyset, decrypt, encrypt
server_addr = (socket.gethostbyname(socket.gethostname()), 13)
#connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.settimeout(7)
client_socket.connect(server_addr)

#generate the keyset
private_key, public_key = generate_keyset()

#send the public key to the server
client_socket.send(public_key)

#wait for encrypted response
messageData = b""
while True:
    daten, addr = client_socket.recvfrom(1024)
    messageData += daten
    if not daten:
        break
enc_message = pickle.loads(messageData)
message = decrypt(enc_message, private_key)
print(message)
client_socket.close()
del client_socket
