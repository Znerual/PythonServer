import socket
from encryption import generate_keyset, encrypt_session, decrypt_session
from protocoll import send_data, recv_data, recv_text, recv_encrypted_text

VERSION_NUMBER = 1
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
    session_key, enc_data = encrypt_session(VERSION_NUMBER, client_public_key)
    send_data(enc_data, client_serving_socket)
    print("Nachricht gesendet")

    #Warte auf bestätigung
    text = recv_encrypted_text(client_serving_socket, session_key)
    print(text)

    #beende die Verbindung
    client_serving_socket.close()
    del client_serving_socket
    break
server_socket.close()
del server_socket
