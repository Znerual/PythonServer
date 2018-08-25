from protocoll import *
from enum import Enum, unique

@unique
class com(Enum):
    RECV_COM
    RECV_TEXT
    RECV_DATA
    RECV_END
    RECV_START
    SEND_COM
    SEND_TEXT
    SEND_DATA
    SEND_END
    SEND_START
    DO_NOTHING
class state(Enum):
    WAIT
    SEND
    RECV
class Commands:
    def __init__(self, usocket, session_key):
        self.state = states.WAIT
        self.command = com.DO_NOTHING
        self.prev_command = com.DO_NOTHING
        self.socket = usocket
        self.session_key = session_key
    def main(self):
        #Action loop seperating different commands
        if (self.state == states.WAIT):
            pass
        elif (self.state == states.RECV):
            if (self.command == com.RECV_COM):
                self.prev_command == self.command
                self.command = recv_text_encrypted(usocket, session_key)

        elif (self.state == states.SEND):
