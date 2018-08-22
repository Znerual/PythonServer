from threading import Thread
from encryption import generate_keyset, encrypt_session, decrypt_session
from protocoll import send_data, recv_data, recv_text, recv_encrypted_text


class ClientThread(Thread):
    def __init__(self, socket, addr):
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.VERSION_NUMBER = 1
        print("Client connected")
    def run(self):
        print("started")
        client_serving_socket = self.socket
        #Warte auf den Public_key des Clienten
        keyData = recv_data(client_serving_socket)
        print("Key empfangen")
        client_public_key = keyData
        print(keyData)

        #Sende Nachricht und warte auf Antwort
        session_key, enc_data = encrypt_session(self.VERSION_NUMBER, client_public_key)
        send_data(enc_data, client_serving_socket)
        print("Nachricht gesendet")

        #Warte auf bestätigung
        text = recv_encrypted_text(client_serving_socket, session_key)
        print(text)

        #beende die Verbindung
        client_serving_socket.close()
        del client_serving_socket
