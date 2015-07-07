import socket

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
    
if __name__ == '__main__':
    convert_ip4_address()
    get_remote_machine_info()