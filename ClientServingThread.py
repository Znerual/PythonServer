from threading import Thread
from encryption import generate_keyset, encrypt_session, decrypt_session
from protocoll import *
from passwordmanagement import load_hash, save_hash
import logging

class ClientThread(Thread):
    #übergebe den vom Server zugewiesenen Socket + der Client adresse (als Tuple), sowie das Event zum Beenden des Servers
    def __init__(self, socket, addr, running_event):
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.running_event = running_event


        self.VERSION_NUMBER = 1
        self.SALT = "tHisIsMySEc!retSalt271WhatdoyoUKnow".encode("utf8")

        FORMAT = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=FORMAT, filename='serverThread.log',level=logging.DEBUG)
        self.log = logging.getLogger(__name__)
        print("Client connected")

    def end_session(usocket):
        self.log.debug("Beende den Thread und schließe den Socket")
        usocket.close()
        del usocket
        raise SystemExit

    def run(self):
        print("started")
        client_serving_socket = self.socket
        self.log.debug("Thread gestartet")
        #Warte auf den Public_key des Clienten
        keyData = recv_data(client_serving_socket)
        print("Key empfangen")
        client_public_key = keyData
        print(keyData)
        self.log.debug("Public Key empfangen")

        #Sende Nachricht mit Versionsnummer und warte auf Antwort
        session_key, enc_data = encrypt_session(self.VERSION_NUMBER, client_public_key)
        send_data(enc_data, client_serving_socket)
        print("Nachricht gesendet")
        self.log.debug("Versionsnummer gesendet")

        #warte auf Bestätigung
        if not recv_validation_encrypted(client_serving_socket, session_key):
            end_session(client_serving_socket)
            self.log.info("Versionsnummer abgelehnt")
        self.log.debug("Versionsnummer bestätigt")
        #Sende das Passwort Salt
        send_data_encrypted(self.SALT, client_serving_socket, session_key)
        self.log.debug("Salt gesendet")

        #Empfange den Passwort hash und überprüfe ihn
        pwd_hash = recv_data_encrypted(client_serving_socket, session_key)

        saved_pwd_hash = load_hash()
        if not bytes(saved_pwd_hash) == bytes(pwd_hash):
            self.log.info("Falsches Passwort eingegeben " + str(pwd_hash))
            send_validation_encrypted(client_serving_socket, session_key, False)
            print("Falsches Passwort")
            self.end_session(client_serving_socket)
        self.log.debug("Passwort stimmt")

        #Sende bestätigung
        send_validation_encrypted(client_serving_socket, session_key)
        self.log.debug("Bestätigung gesendet")

        #beende die Verbindung
        client_serving_socket.close()
        del client_serving_socket
        self.log.info("Thread schließt den Socket")
        #beende den Server als ganzes, kann später durch Befehl ausgetauscht werden
        self.running_event.set()
        self.log.info("Thread setzt Event und beendet Server")
