# This is a WiFi scanner tool that uses Scapy which allows a user to scan for nearby wireless networks. It is not a network scanner. This is a work in progress.
# This tool shows the signal strength and other information about wireless networks.
# https://thepythoncode.com/
# Will most likely be merged with Tools/python/Network Scanner/network_scanner.py
# Happily inspired by airodump-ng (https://www.aircrack-ng.org/doku.php?id=airodump-ng) using Scapy (https://scapy.readthedocs.io/en/latest/installation.html)
# the code won't work if you do not enable monitor mode in your network interface
# Ideally to be run in a Linux environment, hence the commands command key command z command y ce0t;ldf omg
# Check if environment is Linux or Windows and run according commands

''' airmon-ng start wlan0 
    iwconfig
    sudo ifconfig wlan0 down
    sudo iwconfig wlan0 mode monitor'''

# Import
from scapy.all import *
from threading import Thread
import pandas
import time
import os

# Functions
def ap_list():
    # Initialise an empty data frame that will hold all of the scanned access points
    networks = pandas.DataFrame(columns=["BSSID","SSID","dBm_Signal","Channel","Crypto"])
    # Set BSSID (MAC Address) of AP, which is unique to each row
    networks.set_index("BSSID", inplace=True)
    
    return networks

# Makes sure that the sniffed packet has a beacon layer on it. Then extracts stats.
def callback(packet, networks):
    # execute whenever a packet is sniffed
    if packet.haslayer(Dot11Beacon):
        # Get MAC Address of AP
        ap_bssid = packet[Dot11].addr2
        # Get name of AP
        ap_ssid = packet[Dot11].info.decode()
        try:
            # Get Signal Strength of AP
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
            
        # Get network stats
        ap_stats = packet[Dot11Beacon].network_stats()
        # Get AP channel
        ap_channel = ap_stats.get("channel")
        # Get Crypto
        ap_enc_type = ap_stats.get("crypto")
        networks.loc[ap_bssid] = (ap_ssid, dbm_signal, ap_channel, ap_enc_type)
    
# Visualize the dataframes    
def print_networks(networks):
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)
        
# Change Channels to monitor
# if you want to change to channel 2, iwconfig wlan0mon channel 2 
def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {dev_interface} channel {ch}")
        # Switch Channel from 1 to 14 every 0.5 seconds
        ch = ch % 14 + 1
        time.sleep(0.5)

def main():
    # Check interface name using iwconfig
    dev_interface = "wlan0mon"
    # Start the thread that prints all of the networks
    network_printer = Thread(target=print_networks)
    network_printer.daemon = True
    network_printer.start()
    # Start the Channel Changer
    channel_changer = Thread(target=change_channel)
    channgel_changer.daemon = True
    channel_changer.start()
    # Start Sniffing
    sniff(prn=callback, iface=dev_interface)

if __name__ == "__main__":
    main()