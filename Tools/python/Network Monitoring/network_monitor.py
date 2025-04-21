# This is a network monitoring tool that uses Scapy which allows networks to be scanned for connected hosts. This is a work in progress.
# This tool is inspired by stuffy24 on YT and aims to provide real-time insights into network performance.
# Scapy official documentation: https://scapy.readthedocs.io/en/latest/installation.html
# ARP Request will ask host for IP address, reply contains MAC address as well as the IP

# Imports for packet handling
from scapy.all import ARP, Ether, srp
from argparse import ArgumentParser
import socket

# Argument Parser to accept command line arguments such as target
# - Help Menu and CLA Preparation
# - Craft ARP Request
parser = Argumentparser(
    title='NetMon',
    desc='Network Scanner.',
    ep='Hi.'
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
    