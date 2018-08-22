import socket
import pickle
from encryption import generate_keyset, encrypt, decrypt

#Erstelle den Server Socket und Binde ihn an Port 13
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 13))

while True:
    state = 0
    private_key, public_key = generate_keyset()
    #Verbinde mit Clienten und erhalten den Socket
    server_socket.listen(5)
    client_serving_socket, addr = server_socket.accept()
    print("Verbunden")
    #Warte auf den Public_key des Clienten
    keyData = b""
    while True:
        daten = client_serving_socket.recv(2048)
        if not daten: break
        keyData += daten
    print("Key empfangen")
    client_public_key = keyData
    print(daten)
    #Sende Nachricht und warte auf Antwort
    message = encrypt("Hey du", client_public_key)
    client_serving_socket.send(pickle.dumps(message))
    #client_serving_socket.send(b"00000000")
    print("Nachricht gesendet")
    data, addrInfo = client_serving_socket.recvfrom(2048)
    print(str(data,"utf8"))
    client_serving_socket.close()
    del client_serving_socket
    break
server_socket.close()
del server_socket
