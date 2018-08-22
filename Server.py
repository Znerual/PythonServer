import socket
import logging
from threading import Event
from encryption import generate_keyset, encrypt_session, decrypt_session
from protocoll import send_data, recv_data, recv_text, recv_encrypted_text
from ClientServingThread import ClientThread

#Logging Format erstellen, gibt Zeit und Nachricht aus
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
#gibt bei gleichem namen immer den gleichen Logger aus, hier wird der Logger mit dem Modul namen gewählt
log = logging.getLogger(__name__)

#Erstelle den Server Socket und Binde ihn an Port 13
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 5555))
log.debug("Serversocket auf Port 5555 erstellt und Verbunden")
#Generiere die RSA Keys
private_key, public_key = generate_keyset()
log.debug("RSA Keys generiert")
running = True
while running:
    #Um unterbrechen zu können wartet der Socket nur für 2 Sekunde, danach wirft er eine abgefangene Exception und die Loop lässt den Socket erneut warten
    try:
        #Versuche zu verbinden, falls kein Client da geht er über socket.timeout und dem pass erneut in die Schleife
        server_socket.settimeout(2)
        server_socket.listen(5)
        client_serving_socket, addr = server_socket.accept()
        log.debug("Versuche mit Client zu verbinden")
    except socket.timeout:
        log.debug("Verbindung Timedout")
        pass
    except:
        log.error("Fataler Fehler bei dem Versuch zu Verbinden, siehe Server.py, schließe Server Socket")
        print("Something went wrong")
        server_socket.close()
        raise
    else:
        #Verbindung wurde erfolgreich aufgebaut
        print("Verbunden")

        #Korrektes beenden und schließen der Sockets, event verknüpfen
        running_event = Event()
        #Client wurde verbunden und seperater Thread wird gestartet
        client_serving_thread = ClientThread(client_serving_socket, addr, running_event)
        client_serving_thread.start()
        threads.append(client_serving_thread)
        #Überprüft ob der Tocher-Thread das Event gesetzt hat
        log.debug("Verbungen und Thread gestartet")
        if running_event.isSet():
            running = False
            log.debug("Serververbindung beenden")


    #Muss noch recherchieren ob notwendig, sehe bis jetzt keine Funktion, ist aber gebräuchlich die threads
    #mit Join zu versehen am ende

server_socket.close()
del server_socket
log.debug("Server beendet")
