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
- `<PROXMOX_IP>`: the IP of your Proxmox node
- `<CT_ID>`: the ID of your container

### Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|Proxmox VE node (already installed)|-|Yes
|[Tailscale account](https://login.tailscale.com/) (free Personal plan)|Free|Yes
|Phone or laptop to connect remotely|-|Yes

### Create the LXC Container
1. In the Proxmox web interface, click *Create CT* and choose a Debian 12 template. Give it a hostname (e.g. `tailscale`), 1 core, 512MB RAM, a 4GB disk, and a static IP address on your home network.

2. **Do not start the container yet.**

### Enable TUN Device Access
Tailscale needs access to the TUN device, which unprivileged LXC containers do not have by default.

1. Open the Proxmox node shell and edit the container config.
```bash
nano /etc/pve/lxc/<CT_ID>.conf
```

2. Add these lines to the bottom of the file and save.
```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```

3. Start the container and open its console.

### Install Tailscale
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

### Configure as a Subnet Router
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

### Test the Connection
1. On your phone, install Tailscale ([iOS](https://apps.apple.com/app/tailscale/id1470499037) / [Android](https://play.google.com/store/apps/details?id=com.tailscale.ipn)) and sign in with the **same account**.

2. Turn off Wi-Fi so the phone uses mobile data, then toggle Tailscale on.

3. Open `https://<PROXMOX_IP>:8006` in the phone browser. The Proxmox login page should load.

4. In the Tailscale app, tap a device to see whether the connection is *direct* or *relayed*. Both work, but direct is faster.

### Hardening
Once Tailscale is working, your Tailscale account is effectively the key to your home network, so lock it down.

#### Secure the Tailscale Account
Tailscale has no password of its own, so the identity provider you sign in with (Google, Microsoft, GitHub, Apple) is the weak point.

1. Enable 2-step verification on that account. An authenticator app or passkey is better than SMS.

2. In the admin console, open *Machines* and remove any device you do not recognise.

3. Open *Settings -> Keys* and delete any unused auth keys.

4. Confirm key expiry is disabled on the container (*Machines -> three dots -> Disable key expiry*).

#### Secure Proxmox
1. Go to *Datacenter -> Permissions -> Two Factor -> Add*.

2. Choose your user and **TOTP**, scan the QR code with an authenticator app, enter the code and confirm.

3. **Save the recovery keys** in a password manager. Without them, losing your phone could lock you out.

#### Disable Unused SSH
SSH is not needed for day-to-day administration. The Proxmox web interface has a built-in *Shell* for the node and a *Console* for every container and VM, and these work over port 8006 without SSH. Every service you leave running is one more thing to secure, so turn off what you do not use.

1. **Check you have a shell without SSH first.** In the Proxmox web interface, select your node and open *Shell*.

2. **Proxmox node:** run the following in that Shell. The second command only matters on newer versions where SSH is socket-activated, and an error saying the unit does not exist is harmless.
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

#### Enable MagicDNS
1. In the admin console, open the *DNS* tab and confirm **MagicDNS** is enabled.

2. Devices running Tailscale can now be reached by name instead of IP.

*MagicDNS only names devices running Tailscale. The Proxmox node will not get a name unless Tailscale is installed on it too.*

#### Snapshot the Container
1. Select the container in Proxmox, open *Snapshots* and click *Take Snapshot*.

2. Name it `tailscale-working` (no spaces) and add a description, e.g. "Subnet router approved, key expiry off".

*A snapshot lives on the same storage as the container, so it protects against bad changes, not disk failure. Use *Backup -> Backup now* for a real backup.*

#### Restrict Access with ACLs
By default, every device on your tailnet can reach everything, including your whole home network. To limit what a lost phone could reach, see [Restricting the Phone with ACLs](#restricting-the-phone-with-acls).

### Troubleshooting
- **Tailscale will not start in the container:** the TUN lines are missing or incorrect. Fix the config and restart the container.
- **`tailscale up` refuses to run with an error about non-default flags:** use `tailscale set` instead.
- **Cannot reach devices on the home network:** the subnet route has not been approved in the admin console, or IP forwarding is not enabled.
- **Container drops off the tailnet after a few months:** key expiry was not disabled.
- **Locked out of a shell after disabling SSH:** use the *Shell* button on the node, or the *Console* button on a container or VM, in the Proxmox web interface.

### YouTube Tutorial
[![Tailscale in Proxmox](https://img.youtube.com/vi/JC63OGSzTQI/0.jpg)](https://www.youtube.com/watch?v=JC63OGSzTQI)

## Tailscale on Your Phone and ACLs
Once the [Tailscale subnet router](#tailscale-vpn-in-a-proxmox-lxc-container) is running in its Proxmox container, the next step is to connect your phone and restrict what it can reach if it is ever lost or stolen. Account hardening (2FA, key expiry, disabling unused SSH) is covered in the container section above.

*Placeholders used below. Replace them with your own values:*
- `<HOME_SUBNET>`: your home network range, e.g. `192.168.x.0/24`
- `<PROXMOX_IP>`: the IP of your Proxmox node
- `<TAILSCALE_CT_IP>`: the IP of the Tailscale container
- `<OMV_IP>`: the LAN IP of your OpenMediaVault VM
- `<OMV_TAILSCALE_IP>`: OMV's `100.x.y.z` Tailscale address (only if Tailscale is installed on OMV)
- `<ROUTER_IP>`: your router's IP

### Approve the Route
1. Open the [admin console](https://login.tailscale.com/admin/machines) and find the container under *Machines*.

2. Click the three dots, select *Edit route settings*, and tick your advertised subnet.

3. Click the three dots again and select *Disable key expiry*.

4. The container should now show a **Subnets** badge.

*If the route was not advertised yet, run `tailscale set --advertise-routes=<HOME_SUBNET>` in the container. Use `tailscale set` rather than `tailscale up`, which refuses to change one setting unless you restate every non-default flag.*

### Connect Your Phone
1. Open the Tailscale app and sign in with the **same account** used on the container.

2. Toggle Tailscale on and accept the VPN permission prompt. The container should appear in the device list.

3. **Test on mobile data.** Turn off Wi-Fi first, since testing on home Wi-Fi proves nothing.

4. With Tailscale on, open `https://<PROXMOX_IP>:8006` in the phone browser. The Proxmox login page should load (accept the certificate warning).

5. In the Tailscale app, tap the container to see whether the connection is *direct* or *relayed*. Both work, but direct is faster.

### Restricting the Phone with ACLs
By default, every device on a tailnet can reach every other device, and everything behind the subnet router. A phone is the device most likely to be lost, so it is given a narrow rule that only allows what it needs.

**What tagging does:** a tagged device belongs to the tag (e.g. `tag:phone`) instead of to your user. Only rules naming that tag apply to it, and its key does not expire. If a tagged phone is lost, delete it from the admin console. Never tag your main admin device.

1. In the admin console, open *Access controls* and **copy the existing policy into a text file as a backup**.

2. Replace the policy with the following (swapping in your real addresses) and save. The phone can reach the Proxmox web interface and OMV (web interface and SMB), and nothing else. Add more ports as you add services.
```jsonc
{
  "tagOwners": {
    "tag:phone": ["autogroup:admin"]
  },
  "hosts": {
    "omv": "<OMV_TAILSCALE_IP>"
  },
  "acls": [
    // Phone: Proxmox UI and OMV (web UI + SMB), over the LAN route and directly
    {
      "action": "accept",
      "src": ["tag:phone"],
      "dst": [
        "<PROXMOX_IP>:8006",
        "<OMV_IP>:80",
        "<OMV_IP>:445",
        "omv:80",
        "omv:445"
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
        "<OMV_IP>:445",
        "omv:80",
        "omv:445"
      ],
      "deny": [
        "<ROUTER_IP>:80",
        "<TAILSCALE_CT_IP>:22",
        "<TAILSCALE_CT_IP>:8080",
        "omv:22"
      ]
    }
  ]
}
```

3. Under *Machines*, click the three dots next to the phone, select *Edit ACL tags*, and add `tag:phone`.

*Notes:*
- *The `hosts` alias and the `omv:` entries are only needed if Tailscale is installed on OMV. If it is not, delete them and keep the `<OMV_IP>` entries.*
- *Use plain IP addresses in the policy, without a `/24` suffix. A suffix is read as a whole network and would open up far more than one device.*
- *Anything not listed in the phone rule is blocked, so a new service needs a new entry.*
- *The second rule gives every untagged device signed in to your account full access. This is a deliberate convenience for a small home setup. If you want tighter control, replace `autogroup:member` with your own account email and list only the ports you use.*

### Testing the ACLs
1. **Built-in tests:** the `tests` block above is checked every time the policy is saved. If a test fails, the console refuses to save, so a mistake cannot take effect. The tests do not verify that the `hosts` alias holds the correct IP, so compare it against `tailscale ip -4` on OMV.

2. **Preview rules:** on the *Access controls* page, use *Preview rules*, pick the phone, and check what it can reach.

3. **Real-world test:** on mobile data with Tailscale on, `https://<PROXMOX_IP>:8006` and `http://<OMV_IP>` (or `http://omv`) should load, while something not in the rules (e.g. `http://<ROUTER_IP>`) should time out.

4. **Recovery:** the admin console is a browser page and does not depend on tailnet access, and it keeps a policy history. If a change locks the phone out, restore the previous policy from there or from your backup copy.

*When adding a new service, add its IP and port to the phone's rule and a matching `accept` line to the `tests` block (e.g. `:3389` for Remote Desktop, `:53` for Pi-hole DNS).*

### Troubleshooting
- **Page will not load from the phone:** the subnet route has not been approved, or IP forwarding is not enabled in the container.
- **`tailscale up` refuses to run:** use `tailscale set` instead.
- **Phone lost access after tagging:** the ACL does not include the address or port you are trying to reach. Add it to the `tag:phone` rule.
- **OMV web interface loads but the share will not connect:** the ACL is missing port `445`, or SMB is not enabled in OMV.
- **Locked out of the policy:** restore the backup copy of the original policy from your text file.

## OpenMediaVault in a Proxmox VM
[OpenMediaVault (OMV)](https://www.openmediavault.org/) is a Debian-based NAS solution. This writeup runs it as a **virtual machine on Proxmox** instead of on a Raspberry Pi, so it can share the same node as the rest of the home lab. It is a VM rather than an LXC container because OMV is designed for a full OS with its own disks.

*Placeholders used below. Replace them with your own values:*
- `<VM_ID>`: the ID of the OMV VM (e.g. `110`)
- `<OMV_IP>`: the IP address of the OMV VM
- `<DISK_ID>`: the ID of a physical disk, from `/dev/disk/by-id/`
- `<SMB_USER>`: the name of the user you create for SMB access (e.g. `phoneuser`)

### Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|Proxmox VE node (already installed)|-|Yes
|[OMV ISO](https://www.openmediavault.org/download.html)|Free|Yes
|Storage for your data (virtual disk or a spare physical drive)|-|Yes
|Router access to set a DHCP reservation|-|Recommended

### Download the ISO
1. Download the latest stable ISO from the [OMV website](https://www.openmediavault.org/download.html).

2. In Proxmox, go to *local storage -> ISO Images -> Upload* and upload the file.

### Create the VM
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

### Install OMV
1. Start the VM, open the *Console* and follow the installer: language, hostname (`omv`), root password, and target disk.

2. When it reboots, remove the ISO under *Hardware -> CD/DVD Drive* so it does not boot the installer again.

3. Log in as `root` and find the IP address.
```bash
ip a
```

4. Set a **DHCP reservation** for the VM in your router so its address never changes.

### First Login
1. Browse to `http://<OMV_IP>`. The default username is `admin` and the default password is `openmediavault`.

2. **Change the password immediately** from the user menu (*Change Password*).

3. In the VM console, install the guest agent so Proxmox can see the VM's IP and shut it down cleanly.
```bash
apt update && apt install -y qemu-guest-agent
systemctl enable --now qemu-guest-agent
```

### Add Storage
Choose one of the following methods.

**Option 1: Virtual disk (simplest)**

1. Select the VM, go to *Hardware -> Add -> Hard Disk*.

2. Choose the storage and size, then click *Add*.

**Option 2: Physical disk passthrough**

1. In the Proxmox node shell, list your disks by ID.
```bash
ls -l /dev/disk/by-id/
```

2. Pass the chosen disk through to the VM.
```bash
qm set <VM_ID> -scsi1 /dev/disk/by-id/<DISK_ID>
```

*Passthrough this way is easy, but SMART health data will not be visible inside OMV. For full disk access, pass through the whole disk controller instead.*

### Create a File Share
Apply the changes using the banner at the top of the OMV interface after each step.

1. Go to *Storage -> Disks* and confirm the new disk appears. Wipe it if needed.

2. Go to *Storage -> File Systems -> Create*, choose `ext4`, then *Mount* it.

3. Create a user for accessing the share, as described in [Create an SMB User](#create-an-smb-user-and-connect-from-a-phone) below.

4. Go to *Storage -> Shared Folders -> Create*, select the filesystem and set permissions.

5. Go to *Services -> SMB/CIFS -> Settings*, tick **Enabled** and save.

6. In *Services -> SMB/CIFS -> Shares*, click *Create* and select the shared folder.

7. Test from a PC on the network by entering `\\<OMV_IP>\<ShareName>` in File Explorer.

### Create an SMB User and Connect from a Phone
The `admin` account is only for the OMV web interface and cannot be used to log in to SMB shares. Create a separate regular user for file access.

#### Create the User
1. Log in to the OMV web interface at `http://<OMV_IP>` as `admin`.

2. Go to *Users -> Users* and click *Create*.

3. Enter a lowercase name with no spaces (e.g. `phoneuser`) and a **strong password**. This account is reachable over your VPN, so do not reuse the `admin` password. Leave the default groups.

4. Click *Save*, then apply the changes using the banner at the top.

#### Give the User Access to the Share
1. Go to *Storage -> Shared Folders*, select your shared folder and click *Permissions*.

2. Set `<SMB_USER>` to **Read/Write**, click *Save*, and apply the changes.

3. Go to *Services -> SMB/CIFS -> Shares* and confirm the share is listed with **Public** set to *no*, so it requires a login.

4. Go to *Services -> SMB/CIFS -> Settings* and confirm **Enabled** is ticked.

#### Connect from an iPhone
1. Turn off Wi-Fi so the phone uses mobile data, and make sure Tailscale is on.

2. Open the *Files* app, tap the three dots, then *Connect to Server*.

3. Enter `smb://<OMV_IP>` and tap *Next*.

4. Choose **Registered User**, enter `<SMB_USER>` and its password, and tap *Next*. No domain or workgroup is needed.

5. Open the share. To upload, open *Photos*, select a picture, tap *Share -> Save to Files*, and choose the share. To download, open the file in the share and tap *Share -> Save Image*.

#### Connect from an Android Phone
The built-in Files app does not support SMB. Use an SMB-capable file manager (e.g. Solid Explorer or CX File Explorer), add a new SMB connection to `<OMV_IP>` with `<SMB_USER>`, then copy files to and from the share.

#### Check It Went Over Tailscale
1. Wi-Fi must stay off during the test.

2. In the Tailscale app, tap the container to confirm a connection is active (direct or relayed both work).

3. Open a copied picture from the share to confirm the full file arrived.

### Access OMV Remotely over Tailscale
The [Tailscale subnet router](#tailscale-vpn-in-a-proxmox-lxc-container) already exposes your home network, so OMV needs no extra setup on the VM itself.

1. If you restrict your phone with [ACLs](#restricting-the-phone-with-acls), add OMV to the phone's rule: `<OMV_IP>:445` for SMB and `<OMV_IP>:80` for the web interface.

2. Add matching `accept` lines to the `tests` block so a bad edit cannot be saved.

3. On the phone, switch to mobile data with Tailscale on, then connect to `smb://<OMV_IP>` using the Files app (iOS) or an SMB-capable file manager (Android).

### Snapshot the VM
1. Select the VM, open *Snapshots* and click *Take Snapshot*.

2. Name it `omv-baseline` and add a description, e.g. "Fresh install, share working".

*A snapshot protects against bad changes, not disk failure. It does not include passed-through physical disks, and it is not a backup of your data. Back up important files separately.*

### Optional: Install Tailscale on OMV
The subnet router already lets a phone reach OMV at `<OMV_IP>` (phone -> Tailscale container -> OMV). Installing Tailscale on OMV itself adds a second, direct path (phone -> OMV).

|                          |Subnet router only|Tailscale on OMV too|
|--------------------------|------------------|--------------------|
|Needs the container running|Yes              |No, OMV stays reachable on its own|
|Address                   |`<OMV_IP>`        |`<OMV_IP>` still works, plus a `100.x` address and the name `omv`|
|Connection path           |One extra hop     |Direct when possible, which can be faster for large transfers|
|Maintenance               |One install       |Another install to keep updated|

This is not required for basic SMB and web interface access. Skip it if you do not need the extra resilience.

*Placeholder: `<OMV_TAILSCALE_IP>` is OMV's `100.x.y.z` address, shown in the Tailscale admin console or by `tailscale ip -4` on the VM.*

#### A Note on Names
`omv.local` is an mDNS name. It only resolves on your home LAN and will **not** work through Tailscale. Over Tailscale, use the MagicDNS name `omv` (or `omv.<your-tailnet>.ts.net`) or the `100.x` address. MagicDNS must be enabled in the admin console under *DNS*.

#### Install
No SSH is needed. Use the VM *Console* in Proxmox and log in as `root`.

1. Install curl, then Tailscale, and sign in with the **same account**. Do not add `--ssh` or `--advertise-routes`.
```bash
apt update && apt install -y curl
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

#### Make Sure Only the Container Advertises the Subnet
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

#### Update the ACLs
Add a `hosts` alias for OMV's Tailscale address, then allow the phone to reach it. Keep the existing `<OMV_IP>` entries so both paths work.

```jsonc
"hosts": {
  "omv": "<OMV_TAILSCALE_IP>"
},
```

Add these to the phone rule's `dst` list and to the `accept` list in `tests`.
```jsonc
"omv:80",
"omv:445"
```

#### Test
1. Wi-Fi off, Tailscale on.

2. Open `http://omv` in the phone browser. The OMV login page should load.

3. In the Files app, connect to `smb://omv` and sign in with the SMB user.

4. To prove the direct path works without the container, stop the container briefly. `http://omv` should still load, while `http://<OMV_IP>` should not.

#### Troubleshooting
- **`omv.local` does not resolve from the phone:** expected over Tailscale. Use `omv` or the `100.x` address.
- **`omv` does not resolve:** MagicDNS is off, or Tailscale is not toggled on in the phone app.
- **`omv` resolves but will not connect:** the ACL is missing the `hosts` alias or the `omv:80` / `omv:445` entries.
- **OMV cannot reach other LAN devices after installing Tailscale:** check `--accept-routes` is off. `tailscale debug prefs | grep -i routeall` should show `false`.

### Troubleshooting
- **VM boots back into the installer:** the ISO is still attached. Remove it under *Hardware*.
- **Cannot find the VM's IP in Proxmox:** the guest agent is not installed or *Qemu Agent* is not ticked in the VM options.
- **OMV web interface will not load:** check the VM's IP with `ip a` in the console, as the DHCP address may have changed.
- **Share not visible from Windows:** confirm SMB/CIFS is enabled, the share exists, and you are using the user created in OMV.
- **Share works at home but not over Tailscale:** the ACL does not include `<OMV_IP>:445`.
- **Changes do not take effect:** apply them with the banner at the top of the OMV interface.

## Scheduled Weekly Reboot with Notifications
This section reboots the Proxmox node once a week and sends a push notification to your phone when it is back up. Rebooting the node is enough: Proxmox shuts every guest down gracefully and starts them again, so the other containers and VMs do not need their own reboot jobs.

*Placeholders used below. Replace them with your own values:*
- `<NTFY_TOPIC>`: a long, random topic name for [ntfy](https://ntfy.sh) (e.g. several random words plus digits)
- `<HC_UUID>`: the UUID of your [healthchecks.io](https://healthchecks.io) check
- `<REGION/CITY>`: your timezone, e.g. `Europe/Dublin`
- `<OMV_IP>`: the IP address of the OMV VM

*On the public ntfy server, anyone who knows the topic name can read it and post to it, so treat it like a password. Do not reuse an example name from a guide, and do not publish your real topic name or check UUID.*

All commands in this section run on the **Proxmox node** (select the node in the web interface, then *Shell*), not inside a container or VM.

### Make Guests Start Automatically
A node reboot only helps if the guests come back on their own.

1. Select the Tailscale container, go to *Options -> Start at boot* and set it to **Yes**.

2. Do the same for the OMV VM and the Pi-hole container.

3. On each guest, go to *Options -> Start/Shutdown order*:
   - Tailscale container: order `1`
   - Pi-hole container: order `1`
   - OMV VM: order `2`, up delay `30` seconds

### Check the Timezone
Cron uses the node's local time. Check it.
```bash
timedatectl
```

If it is wrong, set it.
```bash
timedatectl set-timezone <REGION/CITY>
```

### Notify When the Node Is Back Up
A script runs once the node has booted and sends a notification listing every container and VM, so you can see at a glance whether everything started.

1. Install the [ntfy app](https://ntfy.sh) on your phone and subscribe to `<NTFY_TOPIC>`.

2. Create the script. Replace `<NTFY_TOPIC>` first, with only letters, digits, `-` and `_`. Angle brackets are not valid in a topic name and cause a 404 error.
```bash
cat > /usr/local/bin/boot-notify.sh << 'EOF'
#!/bin/bash
TOPIC="<NTFY_TOPIC>"
sleep 30
BODY="$(hostname) is back up ($(date '+%a %H:%M'))

Containers:
$(/usr/sbin/pct list | awk 'NR>1 {print "- " $1 " " $NF ": " $2}')

VMs:
$(/usr/sbin/qm list | awk 'NR>1 {print "- " $1 " " $2 ": " $3}')"
curl -fsS -H "Title: Proxmox rebooted" -d "$BODY" "https://ntfy.sh/$TOPIC"
EOF
chmod +x /usr/local/bin/boot-notify.sh
```

3. Check that the first line is exactly `#!/bin/bash`. Pasting into an editor can add leading spaces, which makes systemd fail with `Exec format error`.
```bash
head -n 1 /usr/local/bin/boot-notify.sh | cat -A
```
The output should be `#!/bin/bash$`.

4. Create a systemd unit so it runs after the network and the guests have started.
```bash
cat > /etc/systemd/system/boot-notify.service << 'EOF'
[Unit]
Description=Notify after boot
After=network-online.target pve-guests.service
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/boot-notify.sh

[Install]
WantedBy=multi-user.target
EOF
```

5. Enable it.
```bash
systemctl daemon-reload
systemctl enable boot-notify.service
```

6. Test it through systemd (not just by running the script by hand). Wait about 30 seconds, then check the status and your phone. The status should show `status=0/SUCCESS`.
```bash
systemctl start boot-notify.service
systemctl status boot-notify.service
```

The notification looks like this:
```
pve is back up (Sat 22:30)

Containers:
- 100 tailscale: running
- 120 pihole: running

VMs:
- 110 omv: running
```

### Get Alerted if the Node Does Not Come Back
A node that fails to boot cannot send a notification, so the failure alert has to come from something outside it. A dead-man's switch does this: the node pings an external service every few minutes, and you are alerted when the pings stop. Set this up **before** scheduling the weekly reboot.

1. Create a free check at [healthchecks.io](https://healthchecks.io). Name it after the node, set the **Period** to 5 minutes and the **Grace Time** to about 20 minutes, and save. The grace time must be longer than your reboot window, or you will get an alert every Sunday.

2. In the check's *Integrations*, keep email, or add ntfy with a **different topic** from the boot notification, and subscribe to it in the app.

3. Copy the ping URL (`https://hc-ping.com/<HC_UUID>`). Treat it as private, since anyone with it can send fake pings.

4. Test the ping by hand. It should print `OK`, and the check should turn green.
```bash
curl -fsS -m 10 --retry 3 https://hc-ping.com/<HC_UUID>
```

5. Check what is already in the crontab, so you do not add a duplicate.
```bash
crontab -l
```

6. Add the ping to the node's crontab. Run this once.
```bash
(crontab -l 2>/dev/null; echo '*/5 * * * * curl -fsS -m 10 --retry 3 https://hc-ping.com/<HC_UUID> > /dev/null') | crontab -
```

7. Confirm the line is present, and that cron is running.
```bash
crontab -l
systemctl is-active cron
```

8. After about 10 minutes, the check should still show as **up** on the healthchecks.io dashboard.

9. *(Optional)* To test the alert, put a `#` in front of the ping line (`crontab -e`), wait 25 minutes (5 minute period plus 20 minute grace), confirm you are alerted, then remove the `#`.

If the node stops pinging for longer than the grace time, you are alerted. This covers a failed reboot, a power cut and a crash. You can create a second check and ping it from inside the Tailscale container to also catch the case where the node is up but the container is not.

### Test a Reboot
1. Confirm *Start at boot* is set on every guest.

2. Reboot the node manually at a time when you are happy to lose access for a few minutes.
```bash
reboot
```

3. After a few minutes, check that the notification arrives, `http://omv` or `http://<OMV_IP>` loads from your phone, and the Tailscale container shows as connected in the admin console.

### Schedule the Reboot
Only do this once the manual reboot and the healthchecks.io ping both work. Add a cron job that reboots the node every Sunday at 04:00 (`0` in the fifth field means Sunday). This appends to your existing crontab without overwriting it.
```bash
(crontab -l 2>/dev/null; echo '0 4 * * 0 /usr/sbin/reboot') | crontab -
```

Confirm both lines are present.
```bash
crontab -l
```

*Run the append command only once, or the line will be duplicated.*

After the first scheduled reboot, check that you received the notifications, the guests are running, and the healthchecks.io check did not alert. If it did, the node took longer than the grace time to come back, so raise it.

### Things to Know
- **Remote access drops for a few minutes** around the reboot, since the Tailscale container goes down with the node.

- **The failure alert can fire without a real fault.** The dead-man's switch also triggers if your home internet is down while the node is fine.

- **A node that fails to boot cannot be fixed remotely**, because Tailscale is down with it. Keep backups before relying on unattended reboots.

- **Weekly reboots are optional.** Proxmox shows when a kernel update is pending, so you could reboot manually after updates instead.

- **Once real disks are attached to OMV,** check that OMV and its disks come back cleanly after a reboot, and avoid scheduling the reboot during large transfers.

- **Proxmox's built-in notifications** (*Datacenter -> Notifications*) can send email, Gotify or webhooks for backup jobs and updates. There is no built-in "node rebooted" event, which is why the script above is needed.

### Troubleshooting
- **Service fails with `Exec format error` (status 203/EXEC):** the first line of the script is not exactly `#!/bin/bash`. Recreate the file with the command above and check it with `cat -A`.

- **`curl` returns a 404 error:** the topic still contains a placeholder or an invalid character. Check it with `grep TOPIC= /usr/local/bin/boot-notify.sh`.

- **Service succeeds but no alert on the phone:** open the topic in the ntfy app and check the message is listed. If it is, check notification permissions and battery optimization for the app. If it is not, check the app is subscribed to the same topic on `ntfy.sh`.

- **Other errors:** check `systemctl status boot-notify.service` and `journalctl -u boot-notify.service -b`.

- **Notification arrives but a guest is missing from the list:** *Start at boot* is not set on that guest.

- **Guests start in the wrong order:** check the order and up delay under *Options -> Start/Shutdown order*.

- **Reboot happens at the wrong time:** the node's timezone is wrong. Check it with `timedatectl`.

- **Weekly alert from healthchecks.io:** the grace time is shorter than the time the node takes to reboot. Increase it.

- **Check never turns green:** test the ping URL by hand, check `crontab -l`, and confirm `systemctl is-active cron` says `active`.

- **Cron job does not run:** check `crontab -l` and use full paths, as in the examples above.

## Notify When the Node Shuts Down
This sends a push notification when the Proxmox node shuts down or reboots, and (optionally) when an individual container or VM stops. It complements the [boot notification](#notify-when-the-node-is-back-up), so with the weekly reboot you get "rebooting" followed by "back up". All commands run on the **Proxmox node** (*node -> Shell*), not inside a container or VM.

*Placeholders used below. Replace them with your own values:*
- `<NTFY_TOPIC>`: your private [ntfy](https://ntfy.sh) topic. It can only contain letters, digits, `-` and `_`. Angle brackets cause a 404 error. Do not publish your real topic.
- `<CT_ID>`: the ID of the Tailscale container
- `<PIHOLE_ID>`: the ID of the Pi-hole container
- `<VM_ID>`: the ID of the OMV VM

*Nothing can notify you about a power cut, crash or hard reset, because nothing runs when the machine dies instantly. Use a dead-man's switch such as [healthchecks.io](https://healthchecks.io) for those.*

### How It Works
- A systemd service "starts" instantly and stays active, and does nothing while the node is running.
- At shutdown, systemd stops the service, which runs the notification script.
- The service is ordered after the network and the guests, so it is stopped *before* them and the network is still up when it sends.
- The script checks whether a reboot is queued, so the message says "rebooting" or "shutting down".

### Create the Script
1. Create the script. Replace `<NTFY_TOPIC>` first.
```bash
cat > /usr/local/bin/shutdown-notify.sh << 'EOF'
#!/bin/bash
TOPIC="<NTFY_TOPIC>"
if systemctl list-jobs | grep -q 'reboot.target'; then ACTION="rebooting"; else ACTION="shutting down"; fi
curl -fsS -m 10 -H "Title: Proxmox $ACTION" -d "$(hostname) is $ACTION ($(date '+%a %H:%M'))" "https://ntfy.sh/$TOPIC"
exit 0
EOF
chmod +x /usr/local/bin/shutdown-notify.sh
```

2. Check that the first line is exactly `#!/bin/bash` and the topic has no angle brackets. Pasting into an editor can add leading spaces, which makes systemd fail with `Exec format error`.
```bash
head -n 2 /usr/local/bin/shutdown-notify.sh | cat -A
```

3. Test the script by hand. Your phone should receive "is shutting down". It says that because no reboot is in progress, and the node does not actually shut down.
```bash
/usr/local/bin/shutdown-notify.sh
```

### Create the Service
1. Create the unit.
```bash
cat > /etc/systemd/system/shutdown-notify.service << 'EOF'
[Unit]
Description=Notify on shutdown
After=network-online.target pve-guests.service
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/true
ExecStop=/usr/local/bin/shutdown-notify.sh
TimeoutStopSec=20

[Install]
WantedBy=multi-user.target
EOF
```

2. Enable and start it.
```bash
systemctl daemon-reload
systemctl enable --now shutdown-notify.service
systemctl status shutdown-notify.service
```
The status should read `active (exited)`.

### Test It
1. Stopping the service runs the script, just as shutdown does. Then re-arm it.
```bash
systemctl stop shutdown-notify.service
systemctl start shutdown-notify.service
```

2. Reboot the node at a time when you are happy to lose access for a few minutes.
```bash
reboot
```

3. You should receive two notifications in order: "rebooting", then the boot notification once the node is back up.

### Optional: Notify When a Single Guest Stops
A Proxmox hookscript runs on the node whenever a guest changes state, so nothing needs installing inside the guests.

1. Go to *Datacenter -> Storage -> local -> Edit -> Content* and tick **Snippets**.

2. Create the hookscript. It stays quiet when the whole node is shutting down, so you do not get several alerts at once.
```bash
cat > /var/lib/vz/snippets/guest-notify.sh << 'EOF'
#!/bin/bash
VMID="$1"
PHASE="$2"
TOPIC="<NTFY_TOPIC>"
[ "$PHASE" = "post-stop" ] || exit 0
systemctl list-jobs 2>/dev/null | grep -qE 'reboot.target|poweroff.target|halt.target' && exit 0
NAME=$(/usr/sbin/pct config "$VMID" 2>/dev/null | awk '/^hostname:/{print $2}')
[ -z "$NAME" ] && NAME=$(/usr/sbin/qm config "$VMID" 2>/dev/null | awk '/^name:/{print $2}')
curl -fsS -m 10 -H "Title: Guest stopped" -d "$VMID ${NAME:-unknown} stopped ($(date '+%a %H:%M'))" "https://ntfy.sh/$TOPIC" > /dev/null
exit 0
EOF
chmod +x /var/lib/vz/snippets/guest-notify.sh
```

3. Attach it to each guest.
```bash
pct set <CT_ID> --hookscript local:snippets/guest-notify.sh
pct set <PIHOLE_ID> --hookscript local:snippets/guest-notify.sh
qm set <VM_ID> --hookscript local:snippets/guest-notify.sh
```

4. Test with a guest you do not rely on remotely, such as OMV or Pi-hole. Shut it down from the web interface, then start it again. If the first stop does not notify, start the guest and stop it again, since the hook may only apply from the next start.

*Do not test on the Tailscale container while you are away from home, since stopping it cuts your remote access.*

### Things to Know
- **Shutdown cannot be held up.** The `-m 10` limit on `curl`, `exit 0` and `TimeoutStopSec=20` mean a failed send adds a few seconds at most.
- **The node script only reports the node.** Use the hookscript to be told when an individual container or VM stops.
- **Remote access drops for a few minutes** around a reboot if the Tailscale container runs on this node.

### Troubleshooting
- **No notification on shutdown:** run `systemctl status shutdown-notify.service` and `journalctl -u shutdown-notify.service -n 20 --no-pager`.

- **`Exec format error` (status 203/EXEC):** the first line of the script is not exactly `#!/bin/bash`. Recreate the file with the command above.

- **`curl` returns a 404 error:** the topic still contains a placeholder or an invalid character. Check it with `grep TOPIC= /usr/local/bin/shutdown-notify.sh`.

- **Service shows `inactive` after a test:** run `systemctl start shutdown-notify.service` to re-arm it.

- **Message always says "shutting down" during a reboot:** the reboot job was not visible when the script ran. The notification still arrives, so this is cosmetic.

- **No guest message:** check *Snippets* is enabled on the `local` storage and the hookscript is attached (`pct config <ID>` or `qm config <ID>`).

## Pi-hole in a Proxmox LXC Container
[Pi-hole](https://pi-hole.net/) is a network-wide ad and tracker blocker that works as a DNS server for your home network. Devices ask it for the address of a domain, and Pi-hole answers with a dead address (`0.0.0.0`) if the domain is on a blocklist. Otherwise it forwards the question to a real upstream DNS server and caches the answer. Your actual web traffic never passes through Pi-hole, so it needs very few resources.

*Placeholders used below. Replace them with your own values:*
- `<PIHOLE_ID>`: the ID of the Pi-hole container (e.g. `120`)
- `<PIHOLE_IP>`: a free, static IP outside your router's DHCP pool
- `<ROUTER_IP>`: your router's IP

### How It Works
```
Device                 Pi-hole                      Upstream DNS
  |  "IP for example.com?"  |                              |
  |------------------------>|  not blocked, not cached     |
  |                         |----------------------------->|
  |<------------------------|<-----------------------------|
  |  real answer (cached)                                  |
  |===== website traffic goes straight to the site =======>|

  |  "IP for ads.tracker.com?" |
  |--------------------------->|  on a blocklist
  |<---------------------------|  0.0.0.0, the connection fails instantly
```
- Pi-hole sees the domain names each device looks up, never the page contents.
- It blocks whole domains, so ads served from the same domain as the content (e.g. YouTube) cannot be blocked this way.
- Devices set to their own DNS server, or using built-in encrypted DNS, bypass it.
- **If Pi-hole is down, every device that uses it loses DNS.** The steps below keep your infrastructure off Pi-hole so remote access survives an outage.

### Create the LXC Container
1. Ping `<PIHOLE_IP>` from a PC. It should time out, which confirms the address is free. Also make sure it is outside your router's DHCP pool, or reserve it there.

2. In Proxmox, go to *local -> CT Templates -> Templates* and download `debian-12-standard` if you do not have it.

3. Click *Create CT* and use the following settings.

|Tab|Setting|
|---|-------|
|General|ID `<PIHOLE_ID>`, hostname `pihole`, set a root password, leave *Unprivileged* ticked|
|Template|`debian-12-standard`|
|Disks|4GB|
|CPU|1 core|
|Memory|512MB, swap 512MB|
|Network|Bridge `vmbr0`, IPv4 *Static* `<PIHOLE_IP>/24`, gateway `<ROUTER_IP>`|
|DNS|DNS server `1.1.1.1` (or your router), domain blank|

4. Untick *Start after created* and finish.

5. Select the container, go to *Options -> Start at boot* and set it to **Yes**.

6. Go to *Options -> Start/Shutdown order* and set the order to `1`, so DNS is among the first things up after a node reboot.

7. Start the container and open its *Console*.

### Install Pi-hole
1. Update the container and install curl.
```bash
apt update && apt upgrade -y
apt install -y curl
```

2. Run the official installer.
```bash
curl -sSL https://install.pi-hole.net | bash
```

3. In the installer, keep the static IP prompt (the container is already static), choose an upstream DNS provider (e.g. Cloudflare or Quad9), and keep the default blocklist and query logging.

4. Set the admin password. On Pi-hole v6 the command is:
```bash
pihole setpassword
```
On v5, use `pihole -a -p` instead.

### Privacy Settings
- **Privacy mode:** start with *Show everything*, since the query log is how you find out why a site is broken. Raise it later (hide domains, or domains and clients) if other people use the network.
- **Query logging:** keep it on. Shorten the retention period instead of turning it off.
- **Upstream provider:** whichever one you pick sees every domain you look up, even if Pi-hole hides it in its own log.
- **DNSSEC:** safe to enable. It checks that answers have not been tampered with.
- **Listening:** only answer local requests. **Never expose port 53 to the internet.**

### Blocklists
The installer enables one list by default (StevenBlack's Unified Hosts). To check or add lists:

1. Open `http://<PIHOLE_IP>/admin` and go to *Lists*.

2. To add one, paste its URL, add a comment and click *Add*. Curated lists are on [firebog.net](https://firebog.net). Start with the ones marked as safe, and avoid adding many, since aggressive lists break more sites.

3. Reload the lists in the container console after any change.
```bash
pihole -g
```

### Test It
1. Open `http://<PIHOLE_IP>/admin` and log in.

2. From a PC, check that an ad domain is blocked. A result of `0.0.0.0` means it works.
```
nslookup doubleclick.net <PIHOLE_IP>
```

3. Check that a normal site still resolves to a real address.
```
nslookup google.com <PIHOLE_IP>
```

4. Both lookups should appear in the *Query Log*, one blocked and one allowed.

5. Take a snapshot of the container named `pihole-working` before changing anything else on the network.

### Try It on One Device First
Do not change the router yet.

1. On a PC, set the DNS server manually to `<PIHOLE_IP>` (*Settings -> Network -> your adapter -> DNS*).

2. Browse normally for a few minutes, including some ad-heavy sites.

3. If a site breaks, find the blocked domain in the *Query Log* and click *Allow*. The change applies immediately.

### Roll It Out to the Whole Network
1. Set the router's DHCP DNS server to `<PIHOLE_IP>`. Devices pick it up when they renew their lease or reconnect.

2. If you can enter a second DNS server on the router, you can add `1.1.1.1` as a fallback. Many devices do not strictly prefer the first server, so some will skip ad blocking even when Pi-hole is up. Leave it out if you want strict blocking.

3. **Rollback:** if devices lose internet after the change, put the router's DNS back to its previous setting. Write this step down somewhere you can read without internet.

### Keep Infrastructure Off Pi-hole
Pi-hole runs on the same node as everything else, so the services that provide your remote access and monitoring must not depend on it.

|Service|Use Pi-hole?|Why|
|-------|:----------:|---|
|Proxmox node|No|It needs DNS before Pi-hole has started (the boot notification sends to `ntfy.sh`, and updates need it too), and it hosts Pi-hole|
|Tailscale container|No|It is the way back in, and must find Tailscale's servers at boot without another guest being up|
|OMV VM|No|It gains almost nothing from ad blocking, and needs reliable DNS for updates and Tailscale|
|Phones, PCs, TVs, other household devices|Yes|This is what Pi-hole is for|

Set a non-Pi-hole DNS server (your router, or `1.1.1.1`) on each:

1. **Proxmox node:** *node -> System -> DNS*. Verify with `cat /etc/resolv.conf` in the node *Shell*.

2. **Tailscale container:** *container -> DNS* tab. Verify with `cat /etc/resolv.conf` in its console.

3. **OMV:** *Network -> Interfaces*, edit the interface and enter a DNS server. OMV may have taken its address by DHCP, so it would otherwise inherit Pi-hole from the router.

4. **Static settings are not changed by the router.** The node and the Tailscale container have their own DNS settings and keep them. OMV is the one at risk, so check it first.

5. **Do not set Pi-hole as a global nameserver in the Tailscale admin console.** It would apply to every device on the tailnet, including the ones above.

### Notifications
**Boot notification:** no script is needed inside the Pi-hole container. The [boot notification](#notify-when-the-node-is-back-up) runs on the node and lists every container and VM, so Pi-hole appears automatically once *Start at boot* is set.

**Shutdown notification:** the [shutdown notification](#notify-when-the-node-shuts-down) covers the node and every guest. To get an alert when Pi-hole itself stops, attach the guest hookscript described there.
```bash
pct set <PIHOLE_ID> --hookscript local:snippets/guest-notify.sh
```

### Weekly Reboot and DNS
The weekly node reboot takes Pi-hole down with it, so DNS filtering is unavailable for a few minutes around 04:00. Pi-hole starts first (order `1`), so the gap should be short. Devices that are awake at that hour may see failed lookups until it returns.

### Maintenance
- **Update Pi-hole** from the container console, at a time when a short DNS restart does not matter.
```bash
pihole -up
apt update && apt upgrade -y
```

- **Reload blocklists:** `pihole -g`.

### Troubleshooting
- **Sites will not load on a device:** check its DNS setting, and try the rollback above. Test with `nslookup google.com <PIHOLE_IP>`.

- **A site or app is broken:** open the *Query Log*, find the blocked domain from that time, and click *Allow*.

- **Ads still appear:** the device may use its own DNS or built-in encrypted DNS, or the ad is served from the same domain as the content.

- **Whole network loses DNS:** the container is down. Start it from the Proxmox web interface, or use the router rollback.

- **Dashboard shows 0 domains on blocklists:** the lists have not loaded. Run `pihole -g`.

- **Container will not start after a reboot:** check *Start at boot* is set and the static IP is not used by another device.

## NOTIFICATIONS AND MONITORING

- Boot notification (ntfy): /usr/local/bin/boot-notify.sh + boot-notify.service
  - Runs after the network and pve-guests.service, waits 30s
  - Sends ONE message listing every container and VM with its status
  - Example: "pve is back up" with "- 100 tailscale: running", "- 110 omv: running"
  - Does NOT send a separate alert for a failed guest. A guest that didn't start shows as "stopped" in the list, so read the list.
  - "running" only means the guest process is up, not that its services are healthy. Check http://omv and Pi-hole after a reboot.
- Shutdown notification (ntfy): /usr/local/bin/shutdown-notify.sh + shutdown-notify.service
  - Sends "rebooting" or "shutting down" when the node goes down
  - Service must stay armed: systemctl is-active shutdown-notify.service = active
  - After a manual stop/start test, always start it again
- Guest hookscript (optional): /var/lib/vz/snippets/guest-notify.sh
  - Alerts when a single guest stops, stays quiet during a whole-node reboot
  - Only reports stops, not starts [TODO: confirm attached, or skip]
- Dead-man's switch: healthchecks.io
  - Check: period 5 min, grace 20 min (alerts after 25 min of silence)
  - Ping: cron on the node every 5 minutes (confirmed working)
  - Alert: its own ntfy integration, separate topic from the boot/shutdown one, plus email
  - Normal reboot inside the window sends NO alert (it never goes "down")
  - Covers power cuts, crashes, hard resets and a node that won't boot
  - Can false-alarm if home internet is down while the node is fine
- Weekly reboot: 0 4 * * 0 /usr/sbin/reboot [TODO: add after the reboot test passes]
- Two ntfy topics are in use: one for node boot/shutdown, one for healthchecks.io. Keep both private.
  - [TODO: confirm the node scripts no longer use the old topic ending in x7k2q9m4]
    check with: grep TOPIC= /usr/local/bin/boot-notify.sh /usr/local/bin/shutdown-notify.sh

### After every reboot, check
- Boot notification arrived and lists tailscale, pihole and omv as running
- http://omv loads from the phone (mobile data, Tailscale on)
- Pi-hole answers: nslookup google.com 192.168.0.120
- crontab -l shows the ping (and the reboot line once added)
- systemctl is-active cron shutdown-notify.service = active
- healthchecks.io check is green, with no alert

### Not covered
- Power cuts, crashes and hard resets send nothing from the node (healthchecks.io is the alert)
- A node that fails to boot can't be fixed remotely, because Tailscale goes down with it

## OpenMediaVault Raspberry Pi 4B Fileserver
Installing a lightweight and feature-rich home NAS solution, OpenMediaVault, based on Linux and running on a RasPi 4B allows us to configure a private, at-home local network storage solution.

This can be done reliably on any Raspberry Pi full board, given enough ram and processing capabilities. ***This writeup follows the Model 4B specifically.***

Out of the box, the OMV software has support for (S)FTP, SMB/CIFS, DAAP media server, RSync, and even features built-in support for Docker containers.

### Equipment List
|Item         |Price  | Required |
|-------------|-------|:--------:|
|[Raspberry Pi 4 Model B 4GB RAM](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/?variant=raspberry-pi-4-model-b-4gb)|€47.27 - €61.95|Yes
|[MicroSD Card](https://www.aliexpress.com/w/wholesale-micro-sd-card.html?spm=a2g0o.productlist.search.0)|€2.27 - €13.01|Yes
|Wi-Fi or (ideally) Ethernet|-  |Yes
|[MicroSD Card Reader/Adapter](https://www.aliexpress.com/w/wholesale-micro-sd-card-reader.html?spm=a2g0o.productlist.search.0) |€0.87 - €7.08|No (If purchased in bundle with Pi)
|[Monitor and HDMI -> Micro HDMI Cable](https://www.aliexpress.com/w/wholesale-raspberry-pi-micro-hdmi-cable.html?spm=a2g0o.productlist.search.0)|€2.50 - €6.23|Yes
|*(Optional)* [Raspberry Pi DSI Display](https://www.aliexpress.com/w/wholesale-raspberry-pi-pci-display.html?spm=a2g0o.productlist.search.0)|€10.00 - €20.10|No 


### *(Optional)* Flashing Pi OS on the SD Card
**If you purchased your RasPi and SD Card separately, it will not be pre-flashed with Pi OS**

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for your system.
   <img width="1185" height="475" alt="image" src="https://github.com/user-attachments/assets/cc1145b6-cf20-4800-be7f-6c642c34bf0f" />

2. Plug your MicroSD Card into the adapter and the adapter into your device. Open the Pi Imager and select [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/). Review settings and click Next. Do not apply OS customisations.

3. Wait until installation finishes, then power on the Raspberry Pi.  

### Download and Install OMV
[OMV](https://www.openmediavault.org/) is the next generation network attached storage (NAS) solution based on Debian Linux.

1. Connect Pi to peripherals or DSI Display if required.

2. Before installation, update and upgrade existing packages.
```bash
sudo apt update && sudo apt upgrade -y
```

3. Install wget.
```bash
sudo apt install wget -y
```

4. Run the [preinstall script](https://raw.githubusercontent.com/OpenMediaVault-Plugin-Developers/installScript/master/preinstall) which will allow the ethernet connection to be persistent.
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

7. The Pi will automatically reboot. If not, restart the Pi.
```bash
sudo reboot now
```

### OMV Configuration
Once the device is rebooted and on, the IP address of the Pi is used to access the OMV web interface and allows for configuring settings, such as setting up RAID configurations and selecting, wiping and formatting storage devices that are connected via the Pi USB interfaces. 

1. Check the IP address of the device.
```bash
hostname -I
```

2. Enter the address in your local browser to access the web interface and login. The default username is `admin`, and the default password is `openmediavault`. *Change these as soon as you have logged in*

3. If further configuration or access is required, you can log in using SSH with [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), as this will be set up by default when you install OMV.

4. Log into the web interface, you will be taken to the dashboard.

   <img width="373" height="622" alt="image" src="https://github.com/user-attachments/assets/df9a6cbe-2be3-4f92-9b27-e8a709760e35" />

   The dashboard will be empty, but you can select what you need from the check box options, and it will load up.

### Formatting and Setting Up Disks and Filesystems   
1. In *Storage -> Disks* you can select the disks that are connected to the Pi and format them if need be. Either way, there will be another step after this.

2. Go to *Storage -> File Systems* and select *Mount an Existing Filesystem* to add a Filesystem. Select the appropriate Disk and click Save. *Make sure to apply changes in the top right after each step!*

3. After this is done, the Disks should be visible.
   <img width="1555" height="428" alt="image" src="https://github.com/user-attachments/assets/bea81247-18ac-4676-9bf5-49e0e5db024b" />

### Setting up SMB/CIFS for File Sharing
1. Go to *Services -> SMB/CIFS -> Shares* and click "Create a new Share", which will be accessible by machines on the network.

2. Give your Share a name and Select the File System, and Assign appropriate Permissions. Save Changes.

3. In *Services -> SMB/CIFS -> Settings*, enable SMB3. Ensure it is browsable and "Enabled" is checked.

4. Your Share should now be accessible from the Network! Test this by opening the File Explorer and entering `\\<IP_of_Pi>\<Share_Name>`.

### YouTube Tutorial
[![Building a NAS with a Raspberry Pi and OpenMediaVault](https://img.youtube.com/vi/LxsowTcNmY4/0.jpg)](https://www.youtube.com/watch?v=LxsowTcNmY4&t=745s)
