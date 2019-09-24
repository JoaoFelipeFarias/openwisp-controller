from __future__ import unicode_literals
from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Radacct(models.Model):
    radacctid = models.BigAutoField(primary_key=True)
    acctsessionid = models.CharField(max_length=64)
    acctuniqueid = models.CharField(max_length=32)
    username = models.CharField(max_length=253, blank=True, null=True)
    groupname = models.CharField(max_length=253, blank=True, null=True)
    realm = models.CharField(max_length=64, blank=True, null=True)
    nasipaddress = models.GenericIPAddressField()
    nasportid = models.CharField(max_length=15, blank=True, null=True)
    nasporttype = models.CharField(max_length=32, blank=True, null=True)
    acctstarttime = models.DateTimeField(blank=True, null=True)
    acctstoptime = models.DateTimeField(blank=True, null=True)
    acctinterval = models.BigIntegerField(blank=True, null=True)
    acctupdatetime = models.DateTimeField(blank=True, null=True)
    acctsessiontime = models.BigIntegerField(blank=True, null=True)
    acctauthentic = models.CharField(max_length=32, blank=True, null=True)
    connectinfo_start = models.CharField(max_length=50, blank=True, null=True)
    connectinfo_stop = models.CharField(max_length=50, blank=True, null=True)
    acctinputoctets = models.BigIntegerField(blank=True, null=True)
    acctoutputoctets = models.BigIntegerField(blank=True, null=True)
    calledstationid = models.CharField(max_length=50, blank=True, null=True)
    callingstationid = models.CharField(max_length=50, blank=True, null=True)
    acctterminatecause = models.CharField(max_length=32, blank=True, null=True)
    servicetype = models.CharField(max_length=32, blank=True, null=True)
    framedprotocol = models.CharField(max_length=32, blank=True, null=True)
    framedipaddress = models.GenericIPAddressField(blank=True, null=True)
    framedipv6address = models.GenericIPAddressField(blank=True, null=True)
    framedipv6prefix = models.CharField(max_length=50, blank=True, null=True)
    framedinterfaceid = models.CharField(max_length=50, blank=True, null=True)
    delegatedipv6prefix = models.CharField(max_length=50, blank=True, null=True)
    #acctstartdelay = models.IntegerField(blank=True, null=True)
    #acctstopdelay = models.IntegerField(blank=True, null=True)
    #xascendsessionsvrkey = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'radacct'


class Radcheck(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radcheck'

    def __str__(self):
        return 'Radcheck ' + self.username


class Radgroupcheck(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radgroupcheck'


class Radgroupreply(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radgroupreply'


class Radpostauth(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=253)
    pass_field = models.CharField(db_column='pass', max_length=128, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    reply = models.CharField(max_length=32, blank=True, null=True)
    calledstationid = models.CharField(max_length=50, blank=True, null=True)
    callingstationid = models.CharField(max_length=50, blank=True, null=True)
    authdate = models.DateTimeField()

    class Meta:
        db_table = 'radpostauth'


class Radreply(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        db_table = 'radreply'


class Radusergroup(models.Model):
    username = models.CharField(max_length=64)
    groupname = models.CharField(max_length=64)
    priority = models.IntegerField()

    class Meta:
        db_table = 'radusergroup'

class Nas(models.Model):
   nasname = models.CharField(max_length=128)
   shortname = models.CharField(max_length=32)
   type = models.CharField(max_length=30)
   ports = models.IntegerField(blank=True, null=True)
   secret = models.CharField(max_length=60)
   server = models.CharField(max_length=64, blank=True, null=True)
   community = models.CharField(max_length=50, blank=True, null=True)
   description = models.CharField(max_length=200, blank=True, null=True)

   class Meta:
       db_table = 'nas'

   def __str__(self):
       return 'IP:' + self.nasname + ' device:' + self.shortname