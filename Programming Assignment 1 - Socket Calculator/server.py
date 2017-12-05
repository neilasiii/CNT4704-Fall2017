'''
Created on Oct 9, 2017

@author: Neil Stagner III
'''
import re
import select
import socket
import sys


def mathValidator(data):
    # found pattern to match at
    #https://stackoverflow.com/questions/34244782/check-whether-an-expression-is-valid-using-regex-in-python
    if re.match("^\s*[+-]?\s*(?:\d+(?:\.\d*)?|\.\d+)(?:\s*[-+/*]\s*\s*[+-]?\s".
                "*(?:\d+(?:\.\d*)?|\.\d+))*\s*$", data):
        return True
    else:
        return False


if __name__ == "__main__":

    CONNECTION_LIST = []
    TCP_IP = '127.0.0.1'
    TCP_PORT = 50027
    BUFFER_SIZE = 1024

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((TCP_IP, TCP_PORT))
    socket_server.listen(10)

    CONNECTION_LIST.append(socket_server)

    # Read inputs from client in loop until get 0/0
    while 1:
        read_sockets, write_sockets, error_sockets = select.select(
            CONNECTION_LIST, [], [])

        for sock in read_sockets:
            if sock == socket_server:
                # new connection
                sockfd, addr = socket_server.accept()
                CONNECTION_LIST.append(sockfd)
                print "Connected with client on: ", addr

            else:  # Incoming message from client
                try:
                    data = sock.recv(BUFFER_SIZE)
                    if data:
                        if mathValidator(data):
                            print 'Received question:',data,'Send back answer:', eval(data)
                            newdata = eval(data)
                            sock.send(str(newdata))
                        else:
                            sock.send('Invalid question! Please enter the math question again.')

                except:
                    print'\n\nServer program ends (due to the client closes the connection)'
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    sys.exit()

    socket_server.close()
