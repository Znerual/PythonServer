import socket
import pickle
from encryption import generate_keyset, encrypt_session, decrypt_session
from protocoll import send_data, recv_data, recv_text
#Erstelle den Server Socket und Binde ihn an Port 13
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 5555))

while True:
    state = 0
    private_key, public_key = generate_keyset()
    #Verbinde mit Clienten und erhalten den Socket
    server_socket.listen(5)
    client_serving_socket, addr = server_socket.accept()
    print("Verbunden")
    #Warte auf den Public_key des Clienten
    keyData = recv_data(client_serving_socket)

    #while True:
    #    daten = client_serving_socket.recv(2048)
    #    if not daten: break
    #    keyData += daten

    print("Key empfangen")
    client_public_key = keyData
    print(keyData)

    #Sende Nachricht und warte auf Antwort
    message = encrypt_session("Hey du", client_public_key)
    send_data(pickle.dumps(message), client_serving_socket)
    #client_serving_socket.send(pickle.dumps(message))

    #client_serving_socket.send(b"00000000")
    print("Nachricht gesendet")

    #data, addrInfo = client_serving_socket.recvfrom(2048)

    text = recv_text(client_serving_socket)
    print(text)
    client_serving_socket.close()
    del client_serving_socket
    break
server_socket.close()
del server_socket
