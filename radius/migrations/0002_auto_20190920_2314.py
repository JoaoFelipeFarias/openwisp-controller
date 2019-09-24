# Generated by Django 2.0.13 on 2019-09-20 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radius', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radacct',
            name='acctstartdelay',
        ),
        migrations.RemoveField(
            model_name='radacct',
            name='acctstopdelay',
        ),
        migrations.RemoveField(
            model_name='radacct',
            name='xascendsessionsvrkey',
        ),
        migrations.AddField(
            model_name='radacct',
            name='acctupdatetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='radacct',
            name='delegatedipv6prefix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='radacct',
            name='framedinterfaceid',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='radacct',
            name='framedipv6address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='radacct',
            name='framedipv6prefix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
