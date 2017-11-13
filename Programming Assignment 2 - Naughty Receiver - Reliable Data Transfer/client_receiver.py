"""client_receiver."""
import socket
import sys
from random import randint


def main():
    """Run main Function."""
    if(len(sys.argv) < 3):
        print('Usage : python client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    rcvpktLast = ''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to remote host
    try:
        s.connect((host, port))
    except socket.error:
        print('Unable to connect')
        sys.exit()

    print('Connected to server on: ' + host + ' ' + str(port))
    ACK = '0'

    while True:
        rcvpkt = s.recv(2048)

        if rcvpkt == 'close':
            s.close()
            print('**** Disconnected due to server shutdown! ****')
            sys.exit()

        if not corrupt(rcvpkt) and has_ACK(ACK, rcvpkt):

            isDuplicate(rcvpkt, rcvpktLast)
            naughty_reciever(s, ACK)

        rcvpktLast = rcvpkt
        if str(ACK) == '0':
            ACK = '1'
        elif str(ACK) == '1':
            ACK = '0'


def corrupt(rcvpkt):
    """Return true if corrupt, false if not."""
    if rcvpkt == 'corrupt':
        return True
    else:
        return False


def has_ACK(ACK, rcvpkt):
    """Return true if rcvpkt has ACK, else false."""
    if str(ACK) in rcvpkt:
        return True
    else:
        return False


def isDuplicate(rcvpkt, rcvpktLast):
    """Print different message if duplicate packet or not."""
    if rcvpkt == rcvpktLast:
        print('Receiver just correctly received a duplicated message:'
              + rcvpkt)
    else:
        print('Receiver just correctly received a message: ' + rcvpkt)


def naughty_reciever(s, ACK):
    """Naughty receiver functionality from the assignment."""
    print('How do you respond?')
    print('(1) send a correct ACK; (2) send a corrupted ACK;'
          + ' (3) do not send ACK; (4) send a wrong ACK')
    choice = randint(1, 4)

    if choice == 1:
        s.send(str(ACK))
        print('Receiver correctly responds with ACK ' + str(ACK))
    elif choice == 2:
        s.send('corrupt')
        print('A corrupted ACK is sent')
    elif choice == 3:
        print('Receiver will not send ACK')
    elif choice == 4:
        if str(ACK) == '0':
            ACK = '1'
        elif str(ACK) == '1':
            ACK = '0'
        s.send(str(ACK))
        print('Receiver incorrectly responds with ACK ' + str(ACK))


if __name__ == "__main__":
    main()
