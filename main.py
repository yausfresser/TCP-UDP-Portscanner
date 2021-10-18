"""
1. program allows user to enter in ipaddress to scan
2. program scans both TCP and UDP protocol
3. because takes very long time to run, adding threading that allows the program to run very quickly
4.

"""
import socket, threading

def TCP_connect(ip, port_number, delay, output, socktypes, banner):
    # socket.AF_INET- IPV4: soctypes=either UDP or TCP
    TCPsock = socket.socket(socket.AF_INET, socktypes)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # set delay how long to pause
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))

        strMessage='whoAreYou\r\n'
        TCPsock.send(strMessage.encode())
        output[port_number] = 'Listening'
        banner[port_number] = str(TCPsock.recv(1024).decode("utf-8"))

    except:
        output[port_number] = ''
def printServiceOnPort(portNumber, protocol):
    return socket.getservbyport(portNumber, protocol)


def scan_ports(host_ip, delay,sock):

    threads = []        # To run TCP_connect concurrently
    output = {}         # For printing purposes
    banner = {}           # for printing details

    # Spawning threads to scan ports
    for i in range(10000):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output,sock,banner))
        threads.append(t)

    # Starting threads
    for i in range(10000):
        threads[i].start()

    # Locking the main thread until all threads complete
    for i in range(10000):
        threads[i].join()

    # Printing listening ports from small to large
    for i in range(10000):

        if output[i] == 'Listening' or output[i] == 'ESTABLISHED':
            # if protocol is UDP

            if str(sock)=='SocketKind.SOCK_DGRAM':
                print('UDP: ' + str(i) + ': ' + output[i] + ' version:' + banner[i])
            else:
                print('TCP: ' + str(i) + ': ' + output[i] + ' version:' + banner[i]) #19 + printServiceOnPort(i,str(sock)))
                #print('TCP: ' + str(i) + ': ' + output[i] + ' version:' + banner[i] + 'ServiceName= ' + servicename[i])


def main():
    host_ip = input("Enter host IP: ")
    delay = int(input("How many seconds the socket is going to wait until timeout: "))

    scan_ports(host_ip, delay,socket.SOCK_STREAM)
    scan_ports(host_ip, delay,socket.SOCK_DGRAM)

if __name__ == "__main__":
    main()
