from background_task import background
import os
from pexpect import pxssh
from datetime import datetime
from portal.models import CoovaDeviceStatus
from openwisp_controller.config.models import Device

@background(schedule=120)
def coovadevicepool(): #criar um background manager, que pega todos os ips dos coova devices, e sai poolando uma por uma para pegar conectados.
    s = pxssh.pxssh()
    if not s.login('192.168.15.30', 'root', 'vagamesh'):
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

        coovadevice = CoovaDeviceStatus.objects.filter(coova_device__openwisp_device__last_ip='192.168.15.30')

        if coovadevice:
            iter_output = iter(output)
            next(iter_output)
            for line in iter_output:
                file.write(line)
                coovadevice[0].json = iter_output
                coovadevice[0].save()
            file.close()
                # if line == '':
                #     break
                # else:
                #     print(line)
                #
                #     splitted_line = line.split(' ')
                #     print(splitted_line)
                #     dict['mac_address'] = splitted_line[0]
                #     dict['ip'] = splitted_line[1]
                #     dict['status'] = splitted_line[2]
                #     dict['session_id'] = splitted_line[3]
                #     dict['auth_status'] = splitted_line[4]
                #     dict['username'] = splitted_line[5]
                #     dict['duration'] = splitted_line[6]
                #     dict['idle_time'] = splitted_line[7]
                #     dict['input_octets'] = splitted_line[8]
                #     dict['max_total_octets'] = splitted_line[9]
                #     dict['status_option_swap_octets'] = splitted_line[10]
                #     dict['bandwidth_limitation'] = splitted_line[11]
                #     dict['original_url'] = splitted_line[14]
                #     device_list.append(dict)
                #     dict = {}
                    #file.write(str(datetime.now()))


        # # Look for your absolute directory path
        # absolute_path = os.path.dirname(os.path.abspath(__file__))
        # file_path = absolute_path + '/chilli_query.txt'
        #
        # file1 = open(file_path, 'r')
        # file2 = open('otherfile', 'w+')
        #
        # for line in file1:
        #     file2.write(line)
        #
        # file1.close()
        # file2.close()