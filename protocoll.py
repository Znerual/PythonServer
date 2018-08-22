import socket
#Defines the protocoll for transferring data
#defines the chunk size and handels the chunking of receiving data
#Max lengh of data to be sent is covered by an unsigned int (4 byte)
def send_data(data, usocket):
    preData = len(data).to_bytes(4, byteorder="big")
    usocket.send(preData + data)
def send_text(text, usocket):
    data = text.encode("utf8")
    send_data(data, usocket)
def recv_data(usocket):
    length = int.from_bytes(usocket.recv(4), byteorder="big")
    chunk_size = length
    data = bytearray()
    if length > 1024:
        chunk_size = 1024
    while (length > 0):
        data.extend(usocket.recv(chunk_size))
        length -= chunk_size
    return bytes(data)
def recv_text(usocket):
    data = recv_data(usocket)
    return str(data,"utf8")
