#Defines the protocoll for transferring data
#defines the chunk size and handels the chunking of receiving data
#Max lengh of data to be sent is covered by an unsigned int (4 byte)
def send_data(data, socket):
    preData = len(data).to_bytes(4, byteorder="big")
    socket.send(preData + data)
def send_text(text, socket):
    data = text.encode("utf8")
    send_data(data, socket)
def recv_data(socket):
    length = int.from_bytes(socket.recv(4), byteorder="big")
    chunk_size = length
    data = bytearray()
    if length > 1024:
        chunk_size = 1024
    while (length > 0):
        data.append(socket.recv(chunk_size))
        length -= chunk_size
    return bytes(data)
def recv_text(socket):
    data = recv_data(socket)
    return str(data,"utf8")
