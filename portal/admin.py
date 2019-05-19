from django.contrib import admin
from .models import *
from django import forms
# Register your models here.

class CoovaChilliOptionConfigAdmin(admin.ModelAdmin):
    search_fields = ('pretty_print',)



# from prettyjson import PrettyJSONWidget
#
# class JsonForm(forms.ModelForm):
#   class Meta:
#     model = CoovaChilliOptionConfig
#     fields = '__all__'
#     widgets = {
#       'formatted_file': PrettyJSONWidget(),
#     }
#
# class JsonAdmin(admin.ModelAdmin):
#   form = JsonForm
#



admin.site.register(Controller)
admin.site.register(Client)
admin.site.register(PortalDevice)
admin.site.register(AccessPoint)
admin.site.register(CoovaDevice)
admin.site.register(CoovaChilliOptionConfig,CoovaChilliOptionConfigAdmin)
