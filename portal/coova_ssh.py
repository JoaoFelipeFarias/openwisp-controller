import time
from pexpect import pxssh

'''
chilli_query list

To list all connected clients (subscribers) providing the 
MAC Address, 
IP Address, 
internal chilli state (dnat, pass, etc), 
the session id (used in Acct-Session-ID), 
authenticated status (1 authorized, 0 not), 
user-name used during login, 
duration / max duration, 
idle time / max idle time, 
input octets / max input octets, 
output octets / max output octets, 
max total octets,
status of option swapoctets, 
bandwidth limitation information, 
and the original URL.
'''

'''
'chilli_query list', 
'00-56-CD-32-AF-F9 
192.168.180.1 
pass 
5ce176f000000001 
1 
joao 
96/14460 
0/3600 
363519/0 
3227039/0 
0 
1 0%/0 0%/0 http://captive.apple.com/hotspot-detect.html', 'C0-3D-D9-18-D8-98 0.0.0.0 none 5ce0a33600000002 0 - 0/14460 0/3600 0/0 0/0 0 1 0/0 0/0 -', ''
'''

#B8-27-EB-05-C8-61 192.168.180.1 pass 5aa96c5500000001 1 lferreira@gmail.com 276/14440 0/3600 500373/0 15722895/0 0 1 0%/0 0%/0 http://google.com/


#chilli_query authorize ip 192.168.180.3 sessiontimeout 60 username jf123

s = pxssh.pxssh()
if not s.login('192.168.15.30', 'root', 'vagamesh'):
    print('login failed')
else:
    while(True):
        print('ssh session connected successfully')
        s.sendline('chilli_query list')
        s.prompt()
        output = s.before.decode('utf-8').replace('\r', '').split('\n')
        #for k in range(len(output))
        print(output)
        #s.logout()
        time.sleep(20)