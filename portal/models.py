import logging
from django.db import models

from openwisp_users.models import User
#from django.contrib.auth.models import User
from radius.models import Radcheck
from tests import constants

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # radius_user = models.ForeignKey(Radcheck, on_delete=models.CASCADE)

class DeviceManager(models.Manager):
    def register_device(self, user_agent, mac=None):
        if constants.user_agent_mandatory_string not in user_agent:
            return

        if mac:
            mac = mac.replace('-', ':') #if there is a mac, replace the - used by coovachilli
            device = self.filter(mac=mac, user_agent=user_agent)
            if not device.exists():
                self.create(mac=mac,
                        user_agent=user_agent)
            return

        else:
            self.create(mac=mac,
                        user_agent=user_agent)

class Device(models.Model):
    mac = models.CharField(max_length=100, unique=True, blank=True, null=True)
    #user = models.ForeignKey(ControllerUser, on_delete=models.CASCADE, blank=True, null=True)
    user_agent = models.CharField(max_length=1000, blank=True)

    objects = DeviceManager()

    def __str__(self):
        if self.mac is not None:
            return self.mac
        else:
            return 'No MAC available for this device'

class Controller(models.Model):
    name = models.CharField(max_length=100)
    controller_model = models.IntegerField(choices=constants.ControllersTypes.choices)
    description = models.CharField(max_length=200, default='')
    uuid = models.UUIDField()
    redirect_url = models.CharField(max_length=500, default='')
    client = models.ForeignKey('Client', on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#class UserAccess(models.Model):
#
class AccessPoint(models.Model):
    ssid = models.CharField(max_length=100)
    external_ip = models.CharField(max_length=15,default='192.168.254.1')
    external_port = models.CharField(max_length=5, default='5678')
    local_ip = models.CharField(max_length=15)
    mac = models.CharField(max_length=17)
    my_controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    is_controller = models.BooleanField(default=False)
    #ssh_key = models.TextField()

    def __str__(self):
        return self.local_ip + ' @ ' + self.external_ip + ' is_controller: ' + str(self.is_controller)

# class ControllerAdmin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
import pprint
from django.contrib.postgres.fields import JSONField
class CoovaChilliOptionConfig(models.Model):
    options_json = JSONField(help_text=constants.coova_options_json_model)
    #
    def pretty_print(self):
        print(pprint.pprint(self.formatted_file))
        return pprint.pprint(self.formatted_file)

#class NetworkPolicy(models.Model):
