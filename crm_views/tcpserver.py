import sys
import socket
import time
import threading

# socket.AF_INET, socket.SOCK_STREAM


def handle(s):
    print >> sys.stdout, s.recv(4096)
    s.send('''
            HTTP/1.1 101 Web Socket Protocol Handshake\r
            Upgrade: WebSocket\r
            Connection: Upgrade\r
            WebSocket-Origin: http://localhost:8000\r
            WebSocket-Location: ws://localhost:11000/\r
            WebSocket-Protocol: sample
    '''.strip() + '\r\n\r\n')
    time.sleep(1)
    s.send('Hello')
    s.close()


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 11000)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(5)

while True:
    # Wait for a connection
    print >> sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    message = ('1', client_address)
    print >> sys.stderr, '%s connections! Client address: %s' % message
    threading.Thread(target=handle, args=(connection,)).start()
