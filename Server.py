import socket
from encryption import generate_keyset, encrypt_session, decrypt_session
from protocoll import send_data, recv_data, recv_text, recv_encrypted_text
from ClientServingThread import ClientThread


#Erstelle den Server Socket und Binde ihn an Port 13
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 5555))

#Generiere die RSA Keys
private_key, public_key = generate_keyset()
threads = []
while True:

    #Verbinde mit Clienten und erhalten den Socket
    server_socket.listen(5)
    client_serving_socket, addr = server_socket.accept()
    print("Verbunden")

    #Client wurde verbunden und seperater Thread wird gestartet
    client_serving_thread = ClientThread(client_serving_socket, addr)
    client_serving_thread.start()
    threads.append(client_serving_thread)

    #Muss noch recherchieren ob notwendig, sehe bis jetzt keine Funktion, ist aber gebräuchlich die threads
    #mit Join zu versehen am ende
    for i in threads:
        i.join()

server_socket.close()
del server_socket
