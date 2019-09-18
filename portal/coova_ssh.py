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

from datetime import datetime
s = pxssh.pxssh()
if not s.login('192.168.10.30', 'root', 'vagamesh'):
    print('login failed')
else:
        dict = {}
        device_list = []
        print('ssh session connected successfully')
        s.sendline('chilli_query list')
        s.prompt()
        output = s.before.decode('utf-8')
        output = output.replace('\r', '').split('\n')
        print(output)
        file = open('chilli_query.txt', 'w+')
        iter_output = iter(output)
        next(iter_output)
        for line in iter_output:
            if line == '':
                break
            else:
                print(line)

                splitted_line = line.split(' ')
                print(splitted_line)
                dict['mac_address'] = splitted_line[0]
                dict['ip'] = splitted_line[1]
                dict['status'] = splitted_line[2]
                dict['session_id'] = splitted_line[3]
                dict['auth_status'] = splitted_line[4]
                dict['username'] = splitted_line[5]
                dict['duration'] = splitted_line[6]
                dict['idle_time'] = splitted_line[7]
                dict['input_octets'] = splitted_line[8]
                dict['max_total_octets'] = splitted_line[9]
                dict['status_option_swap_octets'] = splitted_line[10]
                dict['bandwidth_limitation'] = splitted_line[11]
                dict['original_url'] = splitted_line[14]
                device_list.append(dict)
                dict = {}
                file.write(datetime.now())
