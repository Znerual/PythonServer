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
    print("Key empfangen")
    client_public_key = keyData
    print(keyData)

    #Sende Nachricht und warte auf Antwort
    session_key, message = encrypt_session("Hey du", client_public_key)
    send_data(pickle.dumps(message), client_serving_socket)
    print("Nachricht gesendet")

    #Warte auf bestätigung
    text = recv_text(client_serving_socket)
    print(text)

    #beende die Verbindung
    client_serving_socket.close()
    del client_serving_socket
    break
server_socket.close()
del server_socket
