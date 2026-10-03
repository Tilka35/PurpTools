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

*Placeholders used below. Replace them with your own values:*
- `<HOME_SUBNET>`: your home network range, e.g. `192.168.x.0/24`
- `<PROXMOX_IP>`: the IP of your Proxmox host
- `<CT_ID>`: the ID of your container

## Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|Proxmox VE host (already installed)|-|Yes
|[Tailscale account](https://login.tailscale.com/) (free Personal plan)|Free|Yes
|Phone or laptop to connect remotely|-|Yes

## Create the LXC Container
1. In the Proxmox web interface, click *Create CT* and choose a Debian 12 template. Give it a hostname (e.g. `tailscale`), 1 core, 512MB RAM, a 4GB disk, and a static IP address on your home network.

2. **Do not start the container yet.**

## Enable TUN Device Access
Tailscale needs access to the TUN device, which unprivileged LXC containers do not have by default.

1. Open the Proxmox host shell and edit the container config.
```bash
nano /etc/pve/lxc/<CT_ID>.conf
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

3. Start Tailscale and sign in using the URL it prints.
```bash
tailscale up
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

3. Advertise your subnet. Use `tailscale set` rather than `tailscale up`, because `tailscale up` refuses to change one setting unless you restate every non-default flag.
```bash
tailscale set --advertise-routes=<HOME_SUBNET>
```

4. Check that it applied.
```bash
tailscale status
```

5. In the [admin console](https://login.tailscale.com/admin/machines), find the container under *Machines*, click the three dots and select *Edit route settings*, then tick the advertised subnet.

6. Click the three dots again and select *Disable key expiry*, so the container does not drop off the network after 180 days.

*Tailscale may print a "UDP GRO forwarding is suboptimally configured" warning. It is only a performance tip for high-throughput routing and can be ignored for a home setup.*

## Test the Connection
1. On your phone, install Tailscale ([iOS](https://apps.apple.com/app/tailscale/id1470499037) / [Android](https://play.google.com/store/apps/details?id=com.tailscale.ipn)) and sign in with the **same account**.

2. Turn off Wi-Fi so the phone uses mobile data, then toggle Tailscale on.

3. Open `https://<PROXMOX_IP>:8006` in the phone browser. The Proxmox login page should load.

4. In the Tailscale app, tap a device to see whether the connection is *direct* or *relayed*. Both work, but direct is faster.

## Hardening
Once Tailscale is working, your Tailscale account is effectively the key to your home network, so lock it down.

### Secure the Tailscale Account
Tailscale has no password of its own, so the identity provider you sign in with (Google, Microsoft, GitHub, Apple) is the weak point.

1. Enable 2-step verification on that account. An authenticator app or passkey is better than SMS.

2. In the admin console, open *Machines* and remove any device you do not recognise.

3. Open *Settings -> Keys* and delete any unused auth keys.

4. Confirm key expiry is disabled on the container (*Machines -> three dots -> Disable key expiry*).

### Secure Proxmox
1. Go to *Datacenter -> Permissions -> Two Factor -> Add*.

2. Choose your user and **TOTP**, scan the QR code with an authenticator app, enter the code and confirm.

3. **Save the recovery keys** in a password manager. Without them, losing your phone could lock you out.

### Disable Unused SSH
SSH is not needed for day-to-day administration. The Proxmox web interface has a built-in *Shell* for the host and a *Console* for every container and VM, and these work over port 8006 without SSH. Every service you leave running is one more thing to secure, so turn off what you do not use.

1. **Check you have a shell without SSH first.** In the Proxmox web interface, select your node and open *Shell*.

2. **Proxmox host:** run the following in that Shell. The second command only matters on newer versions where SSH is socket-activated, and an error saying the unit does not exist is harmless.
```bash
systemctl disable --now ssh
systemctl disable --now ssh.socket
```

3. Confirm nothing is listening on port 22. No output means it is off.
```bash
ss -tlnp | grep :22
```

4. **Tailscale container:** turn off Tailscale SSH.
```bash
tailscale set --ssh=false
```

5. **OMV:** in the OMV web interface, go to *Services -> SSH*, untick **Enabled**, save, and apply the changes.

6. From another PC on the network, `ssh root@<PROXMOX_IP>` should now be refused.

*Only do this on a single-node setup. Clustered Proxmox nodes use SSH between each other. To undo it later, run `systemctl enable --now ssh`.*

### Enable MagicDNS
1. In the admin console, open the *DNS* tab and confirm **MagicDNS** is enabled.

2. Devices running Tailscale can now be reached by name instead of IP.

*MagicDNS only names devices running Tailscale. The Proxmox host will not get a name unless Tailscale is installed on it too.*

### Snapshot the Container
1. Select the container in Proxmox, open *Snapshots* and click *Take Snapshot*.

2. Name it `tailscale-working` (no spaces) and add a description, e.g. "Subnet router approved, key expiry off".

*A snapshot lives on the same storage as the container, so it protects against bad changes, not disk failure. Use *Backup -> Backup now* for a real backup.*

### Restrict Access with ACLs
By default, every device on your tailnet can reach everything, including your whole home network. To limit what a lost phone could reach, see the ACL steps in the phone setup section.

## Troubleshooting
- **Tailscale will not start in the container:** the TUN lines are missing or incorrect. Fix the config and restart the container.
- **`tailscale up` refuses to run with an error about non-default flags:** use `tailscale set` instead.
- **Cannot reach devices on the home network:** the subnet route has not been approved in the admin console, or IP forwarding is not enabled.
- **Container drops off the tailnet after a few months:** key expiry was not disabled.
- **Locked out of a shell after disabling SSH:** use the *Shell* button on the node, or the *Console* button on a container or VM, in the Proxmox web interface.

## YouTube Tutorial
[![Tailscale in Proxmox](https://img.youtube.com/vi/JC63OGSzTQI/0.jpg)](https://www.youtube.com/watch?v=JC63OGSzTQI)

## Tailscale on Your Phone and ACLs
Once the [Tailscale subnet router](#tailscale-vpn-in-a-proxmox-lxc-container) is running in its Proxmox container, the next step is to connect your phone and restrict what it can reach if it is ever lost or stolen. Account hardening (2FA, key expiry, disabling unused SSH) is covered in the container section above.

*Placeholders used below. Replace them with your own values:*
- `<HOME_SUBNET>`: your home network range, e.g. `192.168.x.0/24`
- `<PROXMOX_IP>`: the IP of your Proxmox host
- `<TAILSCALE_CT_IP>`: the IP of the Tailscale container
- `<OMV_IP>`: the IP of your OpenMediaVault VM
- `<ROUTER_IP>`: your router's IP

## Approve the Route
1. Open the [admin console](https://login.tailscale.com/admin/machines) and find the container under *Machines*.

2. Click the three dots, select *Edit route settings*, and tick your advertised subnet.

3. Click the three dots again and select *Disable key expiry*.

4. The container should now show a **Subnets** badge.

*If the route was not advertised yet, run `tailscale set --advertise-routes=<HOME_SUBNET>` in the container. Use `tailscale set` rather than `tailscale up`, which refuses to change one setting unless you restate every non-default flag.*

## Connect Your Phone
1. Open the Tailscale app and sign in with the **same account** used on the container.

2. Toggle Tailscale on and accept the VPN permission prompt. The container should appear in the device list.

3. **Test on mobile data.** Turn off Wi-Fi first, since testing on home Wi-Fi proves nothing.

4. With Tailscale on, open `https://<PROXMOX_IP>:8006` in the phone browser. The Proxmox login page should load (accept the certificate warning).

5. In the Tailscale app, tap the container to see whether the connection is *direct* or *relayed*. Both work, but direct is faster.

## Restricting the Phone with ACLs
By default, every device on a tailnet can reach every other device, and everything behind the subnet router. A phone is the device most likely to be lost, so it is given a narrow rule that only allows what it needs.

**What tagging does:** a tagged device belongs to the tag (e.g. `tag:phone`) instead of to your user. Only rules naming that tag apply to it, and its key does not expire. If a tagged phone is lost, delete it from the admin console. Never tag your main admin device.

1. In the admin console, open *Access controls* and **copy the existing policy into a text file as a backup**.

2. Replace the policy with the following (swapping in your real addresses) and save. The phone can reach the Proxmox web interface and OMV (web interface and SMB), and nothing else. Add more ports as you add services.
```json
{
  "tagOwners": {
    "tag:phone": ["autogroup:admin"]
  },
  "acls": [
    // Phone: Proxmox UI and OMV (web UI + SMB)
    {
      "action": "accept",
      "src": ["tag:phone"],
      "dst": [
        "<PROXMOX_IP>:8006",
        "<OMV_IP>:80",
        "<OMV_IP>:445"
      ]
    },
    // All other (untagged) devices: full access
    {
      "action": "accept",
      "src": ["autogroup:member"],
      "dst": ["*:*"]
    }
  ],
  "tests": [
    {
      "src": "tag:phone",
      "accept": [
        "<PROXMOX_IP>:8006",
        "<OMV_IP>:80",
        "<OMV_IP>:445"
      ],
      "deny": [
        "<ROUTER_IP>:80",
        "<TAILSCALE_CT_IP>:22",
        "<TAILSCALE_CT_IP>:8080"
      ]
    }
  ]
}
```

3. Under *Machines*, click the three dots next to the phone, select *Edit ACL tags*, and add `tag:phone`.

*Use plain IP addresses in the policy, without a `/24` suffix. A suffix is read as a whole network and would open up far more than one device.*

## Testing the ACLs
1. **Built-in tests:** the `tests` block above is checked every time the policy is saved. If a test fails, the console refuses to save, so a mistake cannot take effect.

2. **Preview rules:** on the *Access controls* page, use *Preview rules*, pick the phone, and check what it can reach.

3. **Real-world test:** on mobile data with Tailscale on, `https://<PROXMOX_IP>:8006` and `http://<OMV_IP>` should load, while something not in the rules (e.g. `http://<ROUTER_IP>`) should time out.

4. **Safety net:** leave your PC or laptop untagged so it keeps full access. If a policy change locks the phone out, fix it from there. The console also keeps a policy history.

*When adding a new service, add its IP and port to the phone's rule and a matching `accept` line to the `tests` block (e.g. `:3389` for Remote Desktop).*

## Troubleshooting
- **Page will not load from the phone:** the subnet route has not been approved, or IP forwarding is not enabled in the container.
- **`tailscale up` refuses to run:** use `tailscale set` instead.
- **Phone lost access after tagging:** the ACL does not include the address or port you are trying to reach. Add it to the `tag:phone` rule.
- **OMV web interface loads but the share will not connect:** the ACL is missing port `445`, or SMB is not enabled in OMV.
- **Locked out of the policy:** restore the backup copy of the original policy from your text file.

## YouTube Tutorial
[![Tailscale in Proxmox](https://img.youtube.com/vi/JC63OGSzTQI/0.jpg)](https://www.youtube.com/watch?v=JC63OGSzTQI)

## OpenMediaVault in a Proxmox VM
[OpenMediaVault (OMV)](https://www.openmediavault.org/) is a Debian-based NAS solution. This writeup runs it as a **virtual machine on Proxmox** instead of on a Raspberry Pi, so it can share the same host as the rest of the home lab. It is a VM rather than an LXC container because OMV is designed for a full OS with its own disks.

*Placeholders used below. Replace them with your own values:*
- `<VM_ID>`: the ID of the OMV VM (e.g. `101`)
- `<OMV_IP>`: the IP address of the OMV VM
- `<DISK_ID>`: the ID of a physical disk, from `/dev/disk/by-id/`
- `<PROXMOX_IP>`: the IP of your Proxmox host

## Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|Proxmox VE host (already installed)|-|Yes
|[OMV ISO](https://www.openmediavault.org/download.html)|Free|Yes
|Storage for your data (virtual disk or a spare physical drive)|-|Yes
|Router access to set a DHCP reservation|-|Recommended

## Download the ISO
1. Download the latest stable ISO from the [OMV website](https://www.openmediavault.org/download.html).

2. In Proxmox, go to *local storage -> ISO Images -> Upload* and upload the file.

## Create the VM
Click *Create VM* and use the following settings.

|Tab|Setting|
|---|-------|
|General|ID `<VM_ID>`, name `omv`|
|OS|Select the OMV ISO, type Linux|
|System|Machine `q35`, tick **Qemu Agent**|
|Disks|16GB, VirtIO SCSI single (this is the OS disk only, not for your data)|
|CPU|2 cores, type `host`|
|Memory|2048MB (1GB minimum)|
|Network|Bridge `vmbr0`, model VirtIO|

Finish without ticking *Start after created*.

## Install OMV
1. Start the VM, open the *Console* and follow the installer: language, hostname (`omv`), root password, and target disk.

2. When it reboots, remove the ISO under *Hardware -> CD/DVD Drive* so it does not boot the installer again.

3. Log in as `root` and find the IP address.
```bash
ip a
```

4. Set a **DHCP reservation** for the VM in your router so its address never changes.

## First Login
1. Browse to `http://<OMV_IP>`. The default username is `admin` and the default password is `openmediavault`.

2. **Change the password immediately** from the user menu (*Change Password*).

3. In the VM console, install the guest agent so Proxmox can see the VM's IP and shut it down cleanly.
```bash
apt update && apt install -y qemu-guest-agent
systemctl enable --now qemu-guest-agent
```

## Add Storage
Choose one of the following methods.

**Option 1: Virtual disk (simplest)**

1. Select the VM, go to *Hardware -> Add -> Hard Disk*.

2. Choose the storage and size, then click *Add*.

**Option 2: Physical disk passthrough**

1. In the Proxmox host shell, list your disks by ID.
```bash
ls -l /dev/disk/by-id/
```

2. Pass the chosen disk through to the VM.
```bash
qm set <VM_ID> -scsi1 /dev/disk/by-id/<DISK_ID>
```

*Passthrough this way is easy, but SMART health data will not be visible inside OMV. For full disk access, pass through the whole disk controller instead.*

## Create a File Share
Apply the changes using the banner at the top of the OMV interface after each step.

1. Go to *Storage -> Disks* and confirm the new disk appears. Wipe it if needed.

2. Go to *Storage -> File Systems -> Create*, choose `ext4`, then *Mount* it.

3. Go to *Users -> Users -> Create* and make a user for accessing the share.

4. Go to *Storage -> Shared Folders -> Create*, select the filesystem and set permissions.

5. Go to *Services -> SMB/CIFS -> Settings*, tick **Enabled** and save.

6. In *Services -> SMB/CIFS -> Shares*, click *Create* and select the shared folder.

7. Test from a PC on the network by entering `\\<OMV_IP>\<ShareName>` in File Explorer.

## Create an SMB User and Connect from a Phone
The `admin` account is only for the OMV web interface and cannot be used to log in to SMB shares. Create a separate regular user for file access.

*Extra placeholder: `<SMB_USER>` is the name of the user you create for SMB access (e.g. `phoneuser`).*

### Create the User
1. Log in to the OMV web interface at `http://<OMV_IP>` as `admin`.

2. Go to *Users -> Users* and click *Create*.

3. Enter a lowercase name with no spaces (e.g. `phoneuser`) and a **strong password**. This account is reachable over your VPN, so do not reuse the `admin` password. Leave the default groups.

4. Click *Save*, then apply the changes using the banner at the top.

### Give the User Access to the Share
1. Go to *Storage -> Shared Folders*, select your shared folder and click *Permissions*.

2. Set `<SMB_USER>` to **Read/Write**, click *Save*, and apply the changes.

3. Go to *Services -> SMB/CIFS -> Shares* and confirm the share is listed with **Public** set to *no*, so it requires a login.

4. Go to *Services -> SMB/CIFS -> Settings* and confirm **Enabled** is ticked.

### Connect from an iPhone
1. Turn off Wi-Fi so the phone uses mobile data, and make sure Tailscale is on.

2. Open the *Files* app, tap the three dots, then *Connect to Server*.

3. Enter `smb://<OMV_IP>` and tap *Next*.

4. Choose **Registered User**, enter `<SMB_USER>` and its password, and tap *Next*. No domain or workgroup is needed.

5. Open the share. To upload, open *Photos*, select a picture, tap *Share -> Save to Files*, and choose the share. To download, open the file in the share and tap *Share -> Save Image*.

### Connect from an Android Phone
The built-in Files app does not support SMB. Use an SMB-capable file manager (e.g. Solid Explorer or CX File Explorer), add a new SMB connection to `<OMV_IP>` with `<SMB_USER>`, then copy files to and from the share.

### Check It Went Over Tailscale
1. Wi-Fi must stay off during the test.

2. In the Tailscale app, tap the container to confirm a connection is active (direct or relayed both work).

3. Open a copied picture from the share to confirm the full file arrived.

## Optional: Install Tailscale on OMV
The [Tailscale subnet router](#tailscale-vpn-in-a-proxmox-lxc-container) already lets a phone reach OMV at `<OMV_IP>` (phone -> Tailscale container -> OMV). Installing Tailscale on OMV itself adds a second, direct path (phone -> OMV).

|                          |Subnet router only|Tailscale on OMV too|
|--------------------------|------------------|--------------------|
|Needs the container running|Yes              |No, OMV stays reachable on its own|
|Address                   |`<OMV_IP>`        |`<OMV_IP>` still works, plus a `100.x` address and the name `omv`|
|Connection path           |One extra hop     |Direct when possible, which can be faster for large transfers|
|Maintenance               |One install       |Another install to keep updated|

This is not required for basic SMB and web interface access. Skip it if you do not need the extra resilience.

*Placeholder: `<OMV_TAILSCALE_IP>` is OMV's `100.x.y.z` address, shown in the Tailscale admin console or by `tailscale ip -4` on the VM.*

### A Note on Names
`omv.local` is an mDNS name. It only resolves on your home LAN and will **not** work through Tailscale. Over Tailscale, use the MagicDNS name `omv` (or `omv.<your-tailnet>.ts.net`) or the `100.x` address. MagicDNS must be enabled in the admin console under *DNS*.

### Install
No SSH is needed. Use the VM *Console* in Proxmox and log in as `root`.

1. Install Tailscale and sign in with the **same account**. Do not add `--ssh` or `--advertise-routes`.
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```

2. Open the URL it prints and sign in.

3. In the admin console, find `omv` under *Machines*, click the three dots and select *Disable key expiry*.

4. Note the VM's Tailscale address.
```bash
tailscale ip -4
```

*A VM does not need the TUN device workaround that the LXC container did.*

### Make Sure Only the Container Advertises the Subnet
Only the Tailscale container should be the subnet router. OMV should join the tailnet as an ordinary device. Advertising the same range from two devices causes confusing routing and failover.

1. On OMV, confirm it is not advertising any routes. The output should show no advertised routes.
```bash
tailscale debug prefs | grep -i -A2 advertise
```

2. If it is advertising something, clear it.
```bash
tailscale set --advertise-routes=
```

3. In the admin console, `omv` should **not** show a *Subnets* badge. Only the container should.

4. Do not enable `--accept-routes` on OMV. On Linux it is off by default, and turning it on can make OMV send its own LAN traffic through Tailscale.

### Update the ACLs
Add a `hosts` alias for OMV's Tailscale address, then allow the phone to reach it. Keep the existing `<OMV_IP>` entries so both paths work.

```json
"hosts": {
  "omv": "<OMV_TAILSCALE_IP>"
},
```

Add these to the phone rule's `dst` list and to the `accept` list in `tests`.
```json
"omv:80",
"omv:445"
```

### Test
1. Wi-Fi off, Tailscale on.

2. Open `http://omv` in the phone browser. The OMV login page should load.

3. In the Files app, connect to `smb://omv` and sign in with the SMB user.

4. To prove the direct path works without the container, stop the container briefly. `http://omv` should still load, while `http://<OMV_IP>` should not.

### Troubleshooting
- **`omv.local` does not resolve from the phone:** expected over Tailscale. Use `omv` or the `100.x` address.
- **`omv` does not resolve:** MagicDNS is off, or Tailscale is not toggled on in the phone app.
- **`omv` resolves but will not connect:** the ACL is missing the `hosts` alias or the `omv:80` / `omv:445` entries.
- **OMV cannot reach other LAN devices after installing Tailscale:** check `--accept-routes` is off with `tailscale debug prefs | grep -i acceptroutes`.

## Access OMV Remotely over Tailscale
The [Tailscale subnet router](#tailscale-vpn-in-a-proxmox-lxc-container) already exposes your home network, so OMV needs no extra setup on the VM itself.

1. If you restrict your phone with [ACLs](#restricting-the-phone-with-acls), add OMV to the phone's rule: `<OMV_IP>:445` for SMB and `<OMV_IP>:80` for the web interface.

2. Add matching `accept` lines to the `tests` block so a bad edit cannot be saved.

3. On the phone, switch to mobile data with Tailscale on, then connect to `smb://<OMV_IP>` using the Files app (iOS) or an SMB-capable file manager (Android).

## Snapshot the VM
1. Select the VM, open *Snapshots* and click *Take Snapshot*.

2. Name it `omv-baseline` and add a description, e.g. "Fresh install, share working".

*A snapshot protects against bad changes, not disk failure. It does not include passed-through physical disks, and it is not a backup of your data. Back up important files separately.*

## Troubleshooting
- **VM boots back into the installer:** the ISO is still attached. Remove it under *Hardware*.
- **Cannot find the VM's IP in Proxmox:** the guest agent is not installed or *Qemu Agent* is not ticked in the VM options.
- **OMV web interface will not load:** check the VM's IP with `ip a` in the console, as the DHCP address may have changed.
- **Share not visible from Windows:** confirm SMB/CIFS is enabled, the share exists, and you are using the user created in OMV.
- **Share works at home but not over Tailscale:** the ACL does not include `<OMV_IP>:445`.
- **Changes do not take effect:** apply them with the banner at the top of the OMV interface.

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
