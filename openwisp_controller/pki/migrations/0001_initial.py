# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 17:49
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
from django.db import migrations, models

import django_x509.base.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('openwisp_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('notes', models.TextField(blank=True)),
                ('key_length', models.CharField(blank=True, choices=[('', ''), ('512', '512'), ('1024', '1024'), ('2048', '2048'), ('4096', '4096')], default=django_x509.base.models.default_key_length, help_text='bits', max_length=6, verbose_name='key length')),
                ('digest', models.CharField(blank=True, choices=[('', ''), ('sha1', 'SHA1'), ('sha224', 'SHA224'), ('sha256', 'SHA256'), ('sha384', 'SHA384'), ('sha512', 'SHA512')], default=django_x509.base.models.default_digest_algorithm, help_text='bits', max_length=8, verbose_name='digest algorithm')),
                ('validity_start', models.DateTimeField(blank=True, default=django_x509.base.models.default_validity_start, null=True)),
                ('validity_end', models.DateTimeField(blank=True, default=django_x509.base.models.default_ca_validity_end, null=True)),
                ('country_code', models.CharField(blank=True, max_length=2)),
                ('state', models.CharField(blank=True, max_length=64, verbose_name='state or province')),
                ('city', models.CharField(blank=True, max_length=64, verbose_name='city')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('common_name', models.CharField(blank=True, max_length=63, verbose_name='common name')),
                ('extensions', jsonfield.fields.JSONField(blank=True, default=list, help_text='additional x509 certificate extensions', verbose_name='extensions')),
                ('serial_number', models.PositiveIntegerField(blank=True, help_text='leave blank to determine automatically', null=True, verbose_name='serial number')),
                ('certificate', models.TextField(blank=True, help_text='certificate in X.509 PEM format')),
                ('private_key', models.TextField(blank=True, help_text='private key in X.509 PEM format')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='openwisp_users.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name_plural': 'CAs',
                'abstract': False,
                'verbose_name': 'CA',
            },
        ),
        migrations.CreateModel(
            name='Cert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('notes', models.TextField(blank=True)),
                ('key_length', models.CharField(blank=True, choices=[('', ''), ('512', '512'), ('1024', '1024'), ('2048', '2048'), ('4096', '4096')], default=django_x509.base.models.default_key_length, help_text='bits', max_length=6, verbose_name='key length')),
                ('digest', models.CharField(blank=True, choices=[('', ''), ('sha1', 'SHA1'), ('sha224', 'SHA224'), ('sha256', 'SHA256'), ('sha384', 'SHA384'), ('sha512', 'SHA512')], default=django_x509.base.models.default_digest_algorithm, help_text='bits', max_length=8, verbose_name='digest algorithm')),
                ('validity_start', models.DateTimeField(blank=True, default=django_x509.base.models.default_validity_start, null=True)),
                ('validity_end', models.DateTimeField(blank=True, default=django_x509.base.models.default_cert_validity_end, null=True)),
                ('country_code', models.CharField(blank=True, max_length=2)),
                ('state', models.CharField(blank=True, max_length=64, verbose_name='state or province')),
                ('city', models.CharField(blank=True, max_length=64, verbose_name='city')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('common_name', models.CharField(blank=True, max_length=63, verbose_name='common name')),
                ('extensions', jsonfield.fields.JSONField(blank=True, default=list, help_text='additional x509 certificate extensions', verbose_name='extensions')),
                ('serial_number', models.PositiveIntegerField(blank=True, help_text='leave blank to determine automatically', null=True, verbose_name='serial number')),
                ('certificate', models.TextField(blank=True, help_text='certificate in X.509 PEM format')),
                ('private_key', models.TextField(blank=True, help_text='private key in X.509 PEM format')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('revoked', models.BooleanField(default=False, verbose_name='revoked')),
                ('revoked_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='revoked at')),
                ('ca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pki.Ca', verbose_name='CA')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='openwisp_users.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name_plural': 'certificates',
                'abstract': False,
                'verbose_name': 'certificate',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cert',
            unique_together=set([('ca', 'serial_number')]),
        ),
    ]
