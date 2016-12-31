# '''
#     Simple socket server using threads
# '''
#
# import socket
# import sys
# from thread import *
#
# HOST = ''  # Symbolic name meaning all available interfaces
# PORT = 8888  # Arbitrary non-privileged port
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print 'Socket created'
#
# # Bind socket to local host and port
# try:
#     s.bind((HOST, PORT))
# except socket.error as msg:
#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
#
# print 'Socket bind complete'
#
# # Start listening on socket
# s.listen(10)
# print 'Socket now listening'
#
#
# # Function for handling connections. This will be used to create threads
# def client_thread(conn):
#     # Sending message to connected client
#     conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string
#
#     # infinite loop so that function do not terminate and thread do not end.
#     while True:
#
#         # Receiving from client
#         data = conn.recv(1024)
#         reply = 'OK...' + data
#         if not data:
#             break
#
#         conn.sendall(reply)
#
#     # came out of loop
#     conn.close()
#
#
# # now keep talking with the client
# while 1:
#     # wait to accept a connection - blocking call
#     conn, addr = s.accept()
#     print 'Connected with ' + addr[0] + ':' + str(addr[1])
#     conn.send(
#         'HTTP/1.1 101 Switching Protocols',
#         'Upgrade: websocket',
#         'Connection: Upgrade',
#         'Origin: '
#     )
#     # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function
#     start_new_thread(client_thread, (conn,))
#
# s.close()

import socket
import re
from base64 import b64encode
from hashlib import sha1

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8080))
s.listen(20)

while True:
    client, address = s.accept()
    text = client.recv(1024)
    print text

    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
           .groups()[0]
           .strip())

    response_key = b64encode(sha1(key + GUID).digest())
    response = '\r\n'.join(websocket_answer).format(key=response_key)

    print response
    client.sendall(response)

    print client.recv(1024)
    client.sendall('hello from server')
