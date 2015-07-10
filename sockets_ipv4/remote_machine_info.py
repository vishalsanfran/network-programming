import socket
import sys
import argparse

from binascii import hexlify

def get_remote_machine_info():
    remote_host = 'www.google.com'
    try:
        print "IP address: %s" %socket.gethostbyname(remote_host)
    except socket.error, err_msg:
        print "%s: %s" %(remote_host, err_msg)
        
def convert_ip4_address():
    for ip_addr in ['127.0.0.1', '192.168.0.1']:
        packed_ip_addr = socket.inet_aton(ip_addr)
        unpacked_ip_addr = socket.inet_ntoa(packed_ip_addr)
        print "IP Address: %s => Packed: %s, Unpacked: %s"\
	 %(ip_addr, hexlify(packed_ip_addr), unpacked_ip_addr)

def find_service_name():
    protocolname = 'tcp'
    for port in [80, 25]:
        print "Port: %s => service name: %s" %(port, socket.getservbyport(port, protocolname))
    print "Port: %s => service name: %s" %(53, socket.getservbyport(53, 'udp'))

def convert_integer():
    data = 1234
    #32-bit
    print "Original: %s => Long  host byte order: %s, Network byte order: %s"\
    %(data, socket.ntohl(data), socket.ntohl(data))
    
    #16-bit
    print "Original: %s => Long  host byte order: %s, Network byte order: %s"\
    %(data, socket.ntohs(data), socket.ntohs(data))

def test_socket_timeout():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Default socket timeout: %s" %s.gettimeout()
    s.settimeout(100)
    print "Current socket timeout: %s" %s.gettimeout()

def simple_socket_send():
    # setup argument parsing
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host", required=False)
    parser.add_argument('--port', action="store", dest="port", type=int, required=False)
    parser.add_argument('--file', action="store", dest="file", required=False)
    given_args = parser.parse_args()
    
    host = given_args.host
    port = given_args.port
    filename = given_args.file
    
    #create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
        print "Error creating socket: %s" % e
        sys.exit(1)
        
    #create a socket
    try:
        s.connect((host, port))
    except socket.gaierror, e:
        print "Address-related error connecting to server: %s" % e
        sys.exit(1)
    except socket.error, e:
        print "Connection error: %s" % e
        sys.exit(1)
    
    #sending data
    try:
        s.sendall("GET %s HTTP/1.0\r\n\r\n" % filename)
    except socket.error, e:
        print "Error sending data: %s" % e
        sys.exit(1)
        
    while 1:
        # waiting to receive data from remote host
        try:
            buf = s.recv(2048)
        except socket.error, e:
            print "Error receiving data: %s" % e
            sys.exit(1)
        if not len(buf):
            break
        # write the received data
        sys.stdout.write(buf)

if __name__ == '__main__':
    convert_ip4_address()
    get_remote_machine_info()
    find_service_name()
    convert_integer()
    test_socket_timeout()
    simple_socket_send()