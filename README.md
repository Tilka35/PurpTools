<img width="600" height="200" alt="github-header" src="https://github.com/user-attachments/assets/475c67df-cff3-4771-b01d-bc7c1f9c806b" />

# ⚠️ Ethical Usage Disclaimer ⚠️

This repository is intended **solely for ethical cybersecurity research, educational purposes, and authorized penetration testing**. The tools and scripts provided herein **must never be used for unauthorized access, exploitation, or any form of illegal activity**. 

By utilizing this repository, you **agree** to the following legally binding terms:
- You **must** obtain explicit permission from system owners before conducting security testing.
- You **must** comply with all applicable laws, regulations, and ethical hacking guidelines in your given location.
- The author of this repository **is not responsible** for any misuse, unlawful activity, or damages caused by the use of this code.

**Misuse of this code may result in severe legal consequences.** Proceed responsibly and ethically. Have fun.

# Overview
This is a collection of tools and a sort of roadmap of my coding practice and challenging myself to develop tools that can benefit the open-source community.
Find a variation of Blue and Red Team based tools and interesting scripts in this repository.

My intent is to provide education and for this collection to pose as a showcase of my coding ability.

Use these tools at your own discretion and ensure you are always following strict security practices and have written permission before using these tools on networks or devices THAT ARE NOT YOUR OWN!

Most tools are a work-in-progress, and I am to improve on them as I continue to develop my skills and their functionality.

I am making an honest commitment not to engage in vibe coding for the purpose of my learning, rather using LLMs and AI for learning about best practices, understanding how code works and developing new methodologies of using tools and inspiration for ideas. I appreciate constructive criticism and feedback :)

# Coming Soon...

# Programming

## Web Scraping with Python

# Pentesting

# TryHackMe Writeups

# Meshtastic

# Flipper Zero

# Nethunter

# Home Labs

## OpenMediaVault Raspberry Pi 4B Fileserver
Installing a lightweight ditribution of OpenMediaVault, based on Linux on a RaPi 4B allows us to configure a private, at-home local cloud storage solution.

This can be done reliably on any Raspberry Pi full board, given enough ram and processing capabilities. ***This writeup follows the Model 4B specifically.***

Out of the box, the OMV software has support for (S)FTP, SMB/CIFS, DAAP media server, RSync, and even features built-in support for Docker containers.

## Equipment List

|Item         |Price  | Required |
|-------------|-------|:--------:|
|[Raspberry Pi 4 Model B 4GB RAM](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/?variant=raspberry-pi-4-model-b-4gb)|€47.27 - €61.95|Yes
|[MicroSD Card]([https://www.amazon.co.uk/Vanja-Adapter-Portable-Memory-Reader/dp/B00W02VHM6?adgrpid=1178677363709686&dib=eyJ2IjoiMSJ9.HopFPG_9N9LJWbvXe4m5eeYMAPtxRBx9gvfm8hZn8CR9GNccdyqoUzlZKw_iFI14KfnBGOmUUtCw0p7j04yQBrfZrSMkP81pi-odcv-_SUUmkLd_AOmDO6-24eHnKQ7vUHkTsgaxbcBGYJcA8VARM0ZQk5W0zg3IvF9-8N2g5BQqzeiau0iBvfx6ciB_IXKiMShRScCqR3ikUFZxQvvHM0Ptxm3CWjFzOgE_uIEp74Y.toYWqy_tRWTs8Wul5m48p3h1co808yj0VOcSdZ0djz4&dib_tag=se&hvadid=73667537917398&hvbmt=be&hvdev=c&hvlocphy=150385&hvnetw=s&hvqmt=e&hvtargid=kwd-73667470802167%3Aloc-92&hydadcr=3983_2133757&keywords=micro-sd%2Bcard%2Badapter&mcid=9e6b31781fa4393fa6fb817a4a0ae669&qid=1756552100&sr=8-6&th=1](https://www.amazon.co.uk/SanDisk-128GB-microSDXC-adapter-Performance/dp/B0B7NTY2S6?crid=P0PFIWU3GQE8&dib=eyJ2IjoiMSJ9.n4R-Dt4oBYQRkM6m0S8mH6nmEEe2IJreJiTPetShc9_uO8JH4wC62LLibnyecqBE0_AhZthyvV7I4b_iYBH8HDuyJwweLnqUIne8MFwoDTUtSIG1-OmRdfVDVvcREunl3NF5Bh7hFju9pj7p4tEyozdYQ80mOIDIDPmTZJb9DM3jGO1JKuRwHmD7j9g9D2bBnjnzD5wWaSMo6aosEjPq1obv3Wtt_34Vcb81SgFrrbQ.vNJsZqX7KMVoz2-IS9D13UQF85RQB6R4Es4sdzbHlYA&dib_tag=se&keywords=micro-sd+card&qid=1756558191&sprefix=micro-sd+car%2Caps%2C91&sr=8-4))|€2.27 - €13.01|Yes
|Wi-Fi or (ideally) Ethernet|-  |Yes
|[MicroSD Card Reader/Adapter](https://www.amazon.co.uk/Vanja-Adapter-Portable-Memory-Reader/dp/B00W02VHM6?adgrpid=1178677363709686&dib=eyJ2IjoiMSJ9.HopFPG_9N9LJWbvXe4m5eeYMAPtxRBx9gvfm8hZn8CR9GNccdyqoUzlZKw_iFI14KfnBGOmUUtCw0p7j04yQBrfZrSMkP81pi-odcv-_SUUmkLd_AOmDO6-24eHnKQ7vUHkTsgaxbcBGYJcA8VARM0ZQk5W0zg3IvF9-8N2g5BQqzeiau0iBvfx6ciB_IXKiMShRScCqR3ikUFZxQvvHM0Ptxm3CWjFzOgE_uIEp74Y.toYWqy_tRWTs8Wul5m48p3h1co808yj0VOcSdZ0djz4&dib_tag=se&hvadid=73667537917398&hvbmt=be&hvdev=c&hvlocphy=150385&hvnetw=s&hvqmt=e&hvtargid=kwd-73667470802167%3Aloc-92&hydadcr=3983_2133757&keywords=micro-sd%2Bcard%2Badapter&mcid=9e6b31781fa4393fa6fb817a4a0ae669&qid=1756552100&sr=8-6&th=1) |€0.87 - €7.08|No (If purchased in bundle with RaPi)
|*(Optional)* [Raspberry Pi PCI Display](https://www.amazon.co.uk/Aurevita-Raspberry-Pi-Screen-Touchscreen/dp/B0DQ869VHP/ref=sr_1_12?crid=10P68J153HLQF&dib=eyJ2IjoiMSJ9.fWRbCjqI1Q3nkOnwOAR3eHgZXlkhj-ydGGQL_0xw3vTHkGMjXfSQsOUvJuGwVD1tsY7kLhgJvVYtbCIf7z5Y_U4YPR-lo5FIyetk3CMDHyP85lXa2jhAIgynsa_Ku6n8_C_j-AFHcmbn30euYxNq2sIyLrp_rY-JioVBnGu5WM5hO81MmQmsmaGmpuF64tydNG89t5iqS70SbgQ4zLILIDVy5VrVlGVpeboQV-IvP4A.yS_dDrS8ysfjAG01WF2eIa86EtS9L9D93tXS5vAKP54&dib_tag=se&keywords=raspberry+pi+4+display&qid=1756552349&sprefix=raspberry+pi+4+display%2Caps%2C82&sr=8-12)|€10.00 - €20.10|No 
|*(Optional)* Monitor and HDMI -> MicroHMDI Cable|€2.50 - €6.23|No


## *(Optional)* Flashing RaPi OS on the SD Card
**If you purchased your RaPi and SD Card separately, it will not be pre-flashed with RaPi OS**

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for you system.
   <img width="1185" height="475" alt="image" src="https://github.com/user-attachments/assets/cc1145b6-cf20-4800-be7f-6c642c34bf0f" />

2. Plug your MicroSD Card into the adapter and the adapter into your device. Open the Pi Imager and select [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/). Review settings and click Next. Do not apply OS customisations.

3. Wait until installation finishes, then power on the Raspberry Pi.  

## Download and Install OMV
[OMV](https://www.openmediavault.org/) is the next generation network attached storage (NAS) solution based on Debian Linux.

1. Connect RaPi to peripherals or PCI Display if required.

2. Before installation, update and upgrade existing packages.
```bash
sudo apt update && sudo apt upgrade -y
```

4. Run the [preinstall script](https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/preinstall) which will allow the ethernet connection to be persistent.
```bash
wget -O - https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/preinstall | sudo bash
```

5. Restart the RaPi.
```bash
sudo reboot now
```

6. After reboot, download and install the [OMV install script](https://github.com/OpenMediaVault-Plugin-Developers/installScript).
```bash
wget -O - https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/install | sudo bash
```

8. Restart the RaPi.
```bash
sudo reboot now
```

## OMV Configuration
Once the device is rebooted and on, the IP address of the RaPi is used to access the OMV web interface and allows for configuring settings, such as setting up RAID configurations and selecting, wiping and formatting storage devices that are connected via the RaPi USB interfaces. 

1. Check the IP address of the device.
```bash
hostname -I
```

2. Enter the address in your local browser to access the web interface and login. The default username is code(admin), and the default password is code(openmediavault). *Change these as soon as you have logged in*

3. If further configuration or access is required, you can log in using SSH with [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), as this will be set up by default when you install OMV.

4. Log into the web interface, you will be taken to the dashboard.
   <img width="373" height="622" alt="image" src="https://github.com/user-attachments/assets/df9a6cbe-2be3-4f92-9b27-e8a709760e35" />

   The dashboard will be empty, but you can select what you need from the check box options, and it will load up.

## Formatting and Setting Up Disks and Filesystems   
1. In *Storage -> Disks* you can select the disks that are connected to the RaPi and format them if need be. Either way, there will be another step after this.

2. Go to *Storage -> File Systems* and select *Mount an Existiing Filesystem* to add a Filesystem. Select the appropriate Disk and click Save. *Make sure to apply changes in the top right after each step!*

3. After this is done, the Disks should be visible.
   <img width="1555" height="428" alt="image" src="https://github.com/user-attachments/assets/bea81247-18ac-4676-9bf5-49e0e5db024b" />

## Setting up SMB/CIFS for File Sharing
1. Go to *Services -> SMB/CIFS -> Shares* and click "Create a new Share", which will be accessible by machines on the network.

2. Give your Share a name and Select the File System, and Assign appropriate Permissions. Save Changes.

3. In *Services -> SMB/CIFS -> Settings*, enable SMB3. Ensure it is browsable and "Enabled" is checked.

4. Your Share should now be accessible from the Network! Test this by opening the File Explorer and entering *\\'IP_of_Pi'\'Share_Name'*.

# Additional Reading
