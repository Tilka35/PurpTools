# This is a network scanner tool that uses Scapy which allows networks to be scanned for connected hosts. This is a work in progress.
# This tool is inspired by stuffy24 on YT and aims to provide real-time insights into network performance.
# Scapy official documentation: https://scapy.readthedocs.io/en/latest/installation.html
# ARP Request will ask host for IP address, reply contains MAC address as well as the IP
# Improved to scan ports using threads, using 200 threads to scan the network.

# Imports
from scapy.all import ARP, Ether, srp
from argparse import ArgumentParser
from queue import Queue
from threading import Thread, Lock
import socket

# Threading
N_THREADS = 200

q = Queue()

print_lock = Lock()

# Check if port is open or closed
# - 
# - Attempt to connect to host
def open_port(port):

    try:
        s = socket.socket()
        s.connect((host, port)) # Attempt to connect
    
    except:
        with print_lock:
            return False # Cannot connect - port closed
        
    else:
        with print_lock:
            print(f"{host:15}:{port:5} is Open!") # Print host and port with formatting

    finally:
        s.close() # Close connection

# Function for threading to improve scan speed
def scan_thread():
    global q
    while True:
        # Get port number from queue
        worker = q.get()
        # Scan port number
        open_port(worker) # Scan and put in queue
        # Notify when done
        q.task_done()
        
# Main
def main(host, ports):
    global q
    for t in range(N_THREADS):
        t = Thread(target=scan_thread)
        # Daemon set to true, thread will end when main thread ends
        t.daemon = True
        t.start()
    for worker in ports:
        # Add port to queue
        q.put(worker)
        
    q.join()
        
# Argument Parser to accept command line arguments such as target
# - Help Menu and CLA Preparation
# - Craft ARP Request
parser = ArgumentParser(
    prog='NetMon',
    description='Network Scanner.',
    epilog='Hi.'
)

parser.add_argument('-t', '--target', type=str, help='Target IP address to scan. Use -t to specify Target in CIDR notation.', required=True)
args = parser.parse_args()
target_ip = args.target # IP Dest

# ARP Packet - Assign packet destination to target_ip
arp = ARP(pdst=target_ip)

# Create Ether Broadcast MAC Address packet
ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# Stack Packets
packet = ether/arp

# Next, Send the packets at layer 2, setting the timeout to 3 seconds. The result will be assigned in a list of pairs (sent_packet, received_packet)
result = srp(packet, timeout=3, verbose=0)[0]

# List of clients, iterate over saved packets
clients = []

for sent, received in result:
    # For each response, add IP and MAC address to clients list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    
# Print clients
print("Available Devices on Network")
print("IP" + " "*18+"MAC") # 18 Char

# Print two columns, IP and MAC
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))

print("Please choose an Option")
print("1. Port Scan")

usr_input = input("Enter Number")

if usr_input == "1":
    host = input("Enter Host: ")
    print("Which ports would you like to scan?")
    ports = input("Enter port range: ")
    host, port_range = host, ports
    
    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)
    
    ports = [p for p in range(start_port, end_port)]
    
    main(host, ports)
    
    print("Scan Complete!")
    
else:
    print("Exiting.")