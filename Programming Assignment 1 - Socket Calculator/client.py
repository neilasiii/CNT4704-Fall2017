'''
Created on Oct 9, 2017

@author: Neil Stagner III
'''
import socket, select, sys

if __name__ == "__main__":
    
    if(len(sys.argv) < 3):
        print ("Usage : python client.py hostname port")
        sys.exit()
        
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    #connect to remote host
    try:
        s.connect((host,port))
    except:
        print "Unable to connect" 
        sys.exit()
        
    print "Connected to server on: ", host, port
    
    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        
        for sock in read_sockets:
            #incoming message from server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print "User input ends; end the client program" 
                    sys.exit()
                else:
                    print "Answer from server:", data
            
            else:
                exitVariable = '0/0'
                msg = sys.stdin.readline()
                if str(msg) is exitVariable:
                    print "User input ends; end the client program"
                    sys.exit()
                else:
                    s.send(msg)