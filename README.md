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

## Tailscale VPN in a Proxmox LXC Container
[Tailscale](https://tailscale.com/) is a mesh VPN built on WireGuard that lets you securely reach your home lab from anywhere, **without any port forwarding**. Every device makes outbound connections only, and Tailscale handles NAT traversal to connect them directly (or through an encrypted relay as a fallback).

Running Tailscale in a lightweight LXC container on Proxmox lets it act as a *subnet router*, which gives remote devices access to your whole home network rather than just machines with Tailscale installed.

*Note: the Tailscale clients are open source, but the coordination server is proprietary. [Headscale](https://github.com/juanfont/headscale) is a self-hosted open-source alternative that works with the same clients.*

## Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|Proxmox VE host (already installed)|-|Yes
|[Tailscale account](https://login.tailscale.com/) (free Personal plan)|Free|Yes
|Phone or laptop to connect remotely|-|Yes

## Create the LXC Container
1. In the Proxmox web interface, click *Create CT* and choose a Debian 12 template. Give it a hostname (e.g. `tailscale`), 2 cores, 8192MB RAM, a 4GB disk, and a static IP address (e.g. `192.168.1.50`).

2. **Do not start the container yet.**

## Enable TUN Device Access
Tailscale needs access to the TUN device, which unprivileged LXC containers do not have by default.

1. Open the Proxmox host shell and edit the container config, replacing `<ID>` with your container ID.
```bash
nano /etc/pve/lxc/<ID>.conf
```

2. Add these lines to the bottom of the file and save.
```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```

3. Start the container and open its console.

## Install Tailscale
1. Update the container and install curl.
```bash
apt update && apt upgrade -y
apt install curl -y
```

2. Run the official [install script](https://tailscale.com/install.sh).
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

## Configure as a Subnet Router
1. Enable IP forwarding so the container can route traffic for other devices.
```bash
echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding=1' >> /etc/sysctl.d/99-tailscale.conf
sysctl -p /etc/sysctl.d/99-tailscale.conf
```

2. Check your home network range.
```bash
ip a
```

3. Start Tailscale and advertise your subnet (replace with your own range).
```bash
tailscale up --advertise-routes=192.168.1.0/24
```

4. Open the login URL it prints in your browser and sign in.

5. In the [admin console](https://login.tailscale.com/admin/machines), find the container under *Machines*, click the three dots and select *Edit route settings*, then tick the advertised subnet.

6. Click the three dots again and select *Disable key expiry*, so the container does not drop off the network after 180 days.

## Connect Your Devices
1. Install Tailscale on your phone ([iOS](https://apps.apple.com/app/tailscale/id1470499037) / [Android](https://play.google.com/store/apps/details?id=com.tailscale.ipn)) and your PC, and sign in with the **same account**.

2. Toggle Tailscale on. Each device will be assigned a private `100.x.y.z` address and a MagicDNS name.

3. To test, turn off Wi-Fi on your phone so it uses mobile data, then connect to a device on your home network using its local IP or Tailscale name.

4. In the Tailscale app, tap a device to see whether the connection is *direct* or *relayed*. Both work, but direct is faster.

## Troubleshooting
- **Tailscale will not start in the container:** the TUN lines are missing or incorrect. Fix the config and restart the container.
- **Cannot reach devices on the home network:** the subnet route has not been approved in the admin console.
- **PC unreachable:** check that the PC is not asleep and that its firewall allows the remote access service you are using.

## YouTube Tutorial
[![Tailscale in Proxmox](https://img.youtube.com/vi/JC63OGSzTQI/0.jpg)](https://www.youtube.com/watch?v=JC63OGSzTQI)

## Tailscale on Your Phone, Hardening and ACLs
Once the [Tailscale subnet router](#tailscale-vpn-in-a-proxmox-lxc-container) is running in its Proxmox container, the next step is to connect your phone, lock down the account, and restrict what the phone can reach if it is ever lost or stolen.

*Placeholders used below. Replace them with your own values:*
- `<HOME_SUBNET>`: your home network range, e.g. `192.168.x.0/24`
- `<PROXMOX_IP>`: the IP of your Proxmox host
- `<TAILSCALE_CT_IP>`: the IP of the Tailscale container
- `<ROUTER_IP>`: your router's IP
- `<PC_IP>`: the IP of your PC

## Fixing the Subnet Route Command
If the container was originally set up with `--ssh`, running `tailscale up --advertise-routes=...` fails with an error saying you must mention all non-default flags. Use `tailscale set` to change only the route setting.
```bash
tailscale set --advertise-routes=<HOME_SUBNET>
```

Check that it applied.
```bash
tailscale status
```

*The UDP GRO warning Tailscale prints is only a performance tip and can be ignored for a home setup.*

## Approve the Route
1. Open the [admin console](https://login.tailscale.com/admin/machines) and find the container under *Machines*.

2. Click the three dots, select *Edit route settings*, and tick your advertised subnet.

3. Click the three dots again and select *Disable key expiry*.

4. The container should now show a **Subnets** badge.

## Connect Your Phone
1. Open the Tailscale app and sign in with the **same account** used on the container.

2. Toggle Tailscale on and accept the VPN permission prompt. The container should appear in the device list.

3. **Test on mobile data.** Turn off Wi-Fi first, since testing on home Wi-Fi proves nothing.

4. With Tailscale on, open `https://<PROXMOX_IP>:8006` in the phone browser. The Proxmox login page should load (accept the certificate warning).

5. In the Tailscale app, tap the container to see whether the connection is *direct* or *relayed*. Both work, but direct is faster.

## Hardening
### Secure the Tailscale Account
Tailscale has no password of its own, so the identity provider you sign in with (Google, Microsoft, GitHub, Apple) is the weak point.

1. Enable 2-step verification on that account. An authenticator app or passkey is better than SMS.

2. In the admin console, open *Machines* and remove any device you do not recognise.

3. Open *Settings -> Keys* and delete any unused auth keys.

4. Confirm key expiry is disabled on the container, so it does not drop off the network after 180 days.

### Secure Proxmox
1. Go to *Datacenter -> Permissions -> Two Factor -> Add*.

2. Choose your user and **TOTP**, scan the QR code with an authenticator app, enter the code and confirm.

3. **Save the recovery keys** in a password manager. Without them, losing your phone could lock you out.

### MagicDNS
1. In the admin console, open the *DNS* tab and confirm **MagicDNS** is enabled.

2. Devices running Tailscale can now be reached by name instead of IP.

*MagicDNS only names devices running Tailscale. The Proxmox host will not get a name unless Tailscale is installed on it too.*

### Snapshot the Container
1. Select the container in Proxmox, open *Snapshots* and click *Take Snapshot*.

2. Name it `tailscale-working` (no spaces) and add a description, e.g. "Subnet router approved, key expiry off".

*A snapshot lives on the same storage as the container, so it protects against bad changes, not disk failure. Use *Backup -> Backup now* for a real backup.*

## Restricting the Phone with ACLs
By default, every device on a tailnet can reach every other device, and everything behind the subnet router. A phone is the device most likely to be lost, so it is given a narrow rule that only allows what it needs.

**What tagging does:** a tagged device belongs to the tag (e.g. `tag:phone`) instead of to your user. Only rules naming that tag apply to it, and its key does not expire. If a tagged phone is lost, delete it from the admin console. Never tag your main admin device.

1. In the admin console, open *Access controls* and **copy the existing policy into a text file as a backup**.

2. Replace the policy with the following (swapping in your real addresses) and save. Add more ports as you add services.
```json
{
  "tagOwners": {
    "tag:phone": ["autogroup:admin"]
  },
  "acls": [
    // Phone: only the Proxmox UI and SSH to the Tailscale container
    {
      "action": "accept",
      "src": ["tag:phone"],
      "dst": ["<PROXMOX_IP>:8006", "<TAILSCALE_CT_IP>:22"]
    },
    // All other (untagged) devices: full access
    {
      "action": "accept",
      "src": ["autogroup:member"],
      "dst": ["*:*"]
    }
  ],
  "ssh": [
    {
      "action": "check",
      "src": ["autogroup:member"],
      "dst": ["autogroup:self"],
      "users": ["autogroup:nonroot", "root"]
    }
  ],
  "tests": [
    {
      "src": "tag:phone",
      "accept": ["<PROXMOX_IP>:8006", "<TAILSCALE_CT_IP>:22"],
      "deny": ["<ROUTER_IP>:80", "<TAILSCALE_CT_IP>:8080"]
    }
  ]
}
```

3. Under *Machines*, click the three dots next to the phone, select *Edit ACL tags*, and add `tag:phone`.

## Testing the ACLs
1. **Built-in tests:** the `tests` block above is checked every time the policy is saved. If a test fails, the console refuses to save, so a mistake cannot take effect.

2. **Preview rules:** on the *Access controls* page, use *Preview rules*, pick the phone, and check what it can reach.

3. **Real-world test:** on mobile data with Tailscale on, `https://<PROXMOX_IP>:8006` should load, while something not in the rules (e.g. `http://<ROUTER_IP>`) should time out.

4. **Safety net:** leave your PC or laptop untagged so it keeps full access. If a policy change locks the phone out, fix it from there. The console also keeps a policy history.

*When adding a new service, add its IP and port to the phone's rule and a matching `accept` line to the `tests` block (e.g. `<PC_IP>:3389` for Remote Desktop, `:445` for SMB).*

## Troubleshooting
- **Page will not load from the phone:** the subnet route has not been approved, or IP forwarding is not enabled in the container.
- **`tailscale up` refuses to run:** use `tailscale set` instead (see above).
- **Phone lost access after tagging:** the ACL does not include the address or port you are trying to reach. Add it to the `tag:phone` rule.
- **Locked out of the policy:** restore the backup copy of the original policy from your text file.

## YouTube Tutorial
[![Tailscale in Proxmox](https://img.youtube.com/vi/JC63OGSzTQI/0.jpg)](https://www.youtube.com/watch?v=JC63OGSzTQI)

## OpenMediaVault Raspberry Pi 4B Fileserver
Installing a lightweight and feature-rich home NAS solution, OpenMediaVault, based on Linux and running on a RasPi 4B allows us to configure a private, at-home local network storage solution.

This can be done reliably on any Raspberry Pi full board, given enough ram and processing capabilities. ***This writeup follows the Model 4B specifically.***

Out of the box, the OMV software has support for (S)FTP, SMB/CIFS, DAAP media server, RSync, and even features built-in support for Docker containers.
## Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|[Raspberry Pi 4 Model B 4GB RAM](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/?variant=raspberry-pi-4-model-b-4gb)|€47.27 - €61.95|Yes
|[MicroSD Card](https://www.aliexpress.com/w/wholesale-micro-sd-card.html?spm=a2g0o.productlist.search.0)|€2.27 - €13.01|Yes
|Wi-Fi or (ideally) Ethernet|-  |Yes
|[MicroSD Card Reader/Adapter](https://www.aliexpress.com/w/wholesale-micro-sd-card-reader.html?spm=a2g0o.productlist.search.0) |€0.87 - €7.08|No (If purchased in bundle with Pi)
|[Monitor and HDMI -> MicroHMDI Cable](https://www.aliexpress.com/w/wholesale-raspberry-pi-micro-hdmi-cable.html?spm=a2g0o.productlist.search.0)|€2.50 - €6.23|Yes
|*(Optional)* [Raspberry Pi PCI Display](https://www.aliexpress.com/w/wholesale-raspberry-pi-pci-display.html?spm=a2g0o.productlist.search.0)|€10.00 - €20.10|No 


## *(Optional)* Flashing Pi OS on the SD Card
**If you purchased your RasPi and SD Card separately, it will not be pre-flashed with Pi OS**

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for you system.
   <img width="1185" height="475" alt="image" src="https://github.com/user-attachments/assets/cc1145b6-cf20-4800-be7f-6c642c34bf0f" />

2. Plug your MicroSD Card into the adapter and the adapter into your device. Open the Pi Imager and select [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/). Review settings and click Next. Do not apply OS customisations.

3. Wait until installation finishes, then power on the Raspberry Pi.  

## Download and Install OMV
[OMV](https://www.openmediavault.org/) is the next generation network attached storage (NAS) solution based on Debian Linux.

1. Connect Pi to peripherals or PCI Display if required.

2. Before installation, update and upgrade existing packages.
```bash
sudo apt update && sudo apt upgrade -y
```

3. Install wget.
```bash
sudo apt install wget -y
```

5. Run the [preinstall script](https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/preinstall) which will allow the ethernet connection to be persistent.
```bash
wget -O - https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/preinstall | sudo bash
```

5. Restart the Pi.
```bash
sudo reboot now
```

6. After reboot, download and install the [OMV install script](https://github.com/OpenMediaVault-Plugin-Developers/installScript).
```bash
wget -O - https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/install | sudo bash
```

8. The Pi will automaticallt reboot. If not, restart the Pi.
```bash
sudo reboot now
```

## OMV Configuration
Once the device is rebooted and on, the IP address of the Pi is used to access the OMV web interface and allows for configuring settings, such as setting up RAID configurations and selecting, wiping and formatting storage devices that are connected via the Pi USB interfaces. 

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
1. In *Storage -> Disks* you can select the disks that are connected to the Pi and format them if need be. Either way, there will be another step after this.

2. Go to *Storage -> File Systems* and select *Mount an Existing Filesystem* to add a Filesystem. Select the appropriate Disk and click Save. *Make sure to apply changes in the top right after each step!*

3. After this is done, the Disks should be visible.
   <img width="1555" height="428" alt="image" src="https://github.com/user-attachments/assets/bea81247-18ac-4676-9bf5-49e0e5db024b" />

## Setting up SMB/CIFS for File Sharing
1. Go to *Services -> SMB/CIFS -> Shares* and click "Create a new Share", which will be accessible by machines on the network.

2. Give your Share a name and Select the File System, and Assign appropriate Permissions. Save Changes.

3. In *Services -> SMB/CIFS -> Settings*, enable SMB3. Ensure it is browsable and "Enabled" is checked.

4. Your Share should now be accessible from the Network! Test this by opening the File Explorer and entering *\\'IP_of_Pi'\\'Share_Name'*.

## YouTube Tutorial
[![Building a NAS with a Raspberry Pi and OpenMediaVault](https://img.youtube.com/vi/LxsowTcNmY4/0.jpg)](https://www.youtube.com/watch?v=LxsowTcNmY4&t=745s)

# Additional Reading
