'''
Created on Oct 9, 2017

@author: Neil Stagner III
'''
import socket, sys
from socket import *
from concurrent.futures import TimeoutError

serverName = 'localhost'
serverPort = 50019
buffer = 2048
clientSocket = socket(AF_INET, SOCK_STREAM)

data = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def main():
    socket_server = socket(AF_INET, SOCK_STREAM)
    socket_server.bind((serverName, serverPort))
    socket_server.listen(10)
    print('Lets Start!')
    
    clientSocket, addr = socket_server.accept() #Accept Connections
    print('Connected by', addr)
    receiverIsReceiving = True
    seqNum = '0'
    ACK = '0'
    
    
    while receiverIsReceiving:
        sndpkt = make_pkt(ACK, data, seqNum)
        udt_send(clientSocket, sndpkt)
         
        for r in range(4):
            try:
                clientSocket.settimeout(0.2)
                rcvpkt = clientSocket.recv(buffer)
                
                if corrupt(rcvpkt):
                    print ('Sender received a corrupted ACK, keep waiting')
                    raise TimeoutError
                
                elif not isACK(rcvpkt, ACK):
                    print ('Sender received an ACK with wrong sequence number, keep waiting')
                    raise TimeoutError
                    
            except timeout:
                print('Continue waiting')
                continue
                    
            except TimeoutError:
                print ('Continue waiting')
                continue
            
            else:
                print ('Sender received a valid ACK for ' + str(ACK) + ', send next message')
                seqNum = int(seqNum) + 1
                if str(ACK) == '0':
                    ACK = '1'
                elif str(ACK) == '1':
                    ACK = '0'
                break
            
        else:
            print ('Timeout. Send the message again')                       
     
        if int(seqNum) > 6:
            clientSocket.send('close')
            close_sockets(socket_server)
            
        
def corrupt(rcvpkt):
    if rcvpkt == 'corrupt':
        return True  
    
def close_sockets(socket_server):
    print ('**** Sent all data! closing the connection ****')
    socket_server.close()
    sys.exit()   
    
def make_pkt(ACK, data, seqNum):
    sndpkt = data[int(seqNum)] + ' ' + str(ACK)
    return sndpkt

def udt_send(clientSocket, sndpkt):
    clientSocket.send(sndpkt)
    print ('Sender sent a message: ' + sndpkt)
    
def isACK(rcvpkt, ACK):
    if rcvpkt == ACK:
        return True
            
if __name__ == "__main__":
    main()   