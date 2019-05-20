from rest_framework import routers, serializers, viewsets
from ..models import *
from openwisp_controller.config.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name','mac_address', 'last_ip',)


class ControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controller
        fields = ('name','client',)

class CoovaDeviceSerializer(serializers.ModelSerializer):
    openwisp_device = DeviceSerializer()
    my_controller = ControllerSerializer()

    class Meta:
        model = CoovaDevice
        fields = ('is_coova','openwisp_device', 'my_controller')


'''

    openwisp_device = models.ForeignKey(OpenWispDevice, blank=True, null=True, on_delete=models.DO_NOTHING)
    is_coova = models.BooleanField(default=False)
    my_controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
'''

'''
name = models.CharField(max_length=100)
    controller_model = models.IntegerField(choices=constants.ControllersTypes.choices)
    description = models.CharField(max_length=200, default='')
    uuid = models.UUIDField()
    redirect_url = models.CharField(max_length=500, default='')
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

'''