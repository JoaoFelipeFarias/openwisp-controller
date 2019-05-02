# Generated by Django 2.0.2 on 2018-04-22 01:22

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(max_length=100)),
                ('external_ip', models.CharField(default='192.168.254.1', max_length=15)),
                ('external_port', models.CharField(default='5678', max_length=5)),
                ('local_ip', models.CharField(max_length=15)),
                ('mac', models.CharField(max_length=17)),
                ('is_controller', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('controller_model', models.IntegerField(choices=[(1, 'swarm'), (2, 'aerohive'), (3, 'coovachilli')])),
                ('description', models.CharField(default='', max_length=200)),
                ('uuid', models.UUIDField()),
                ('redirect_url', models.CharField(default='', max_length=500)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Client')),
            ],
        ),
        migrations.CreateModel(
            name='CoovaChilliOptionConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options_json', django.contrib.postgres.fields.jsonb.JSONField(help_text="utilize o formato {key: value, key:value} onde key sao options do coova chilli, ex:{\n'radiusserver1' : 10.1.1.1,\n 'radiusserver2' : 192.168.1.1, \ndhcpif : 'br-lan'}")),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('user_agent', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accesspoint',
            name='my_controller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Controller'),
        ),
    ]
