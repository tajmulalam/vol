# Generated by Django 2.1.2 on 2018-10-22 18:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QrScanData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qrCode', models.TextField()),
                ('uploadedAt', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('verificationCode', models.TextField()),
                ('isVerified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='qrscandata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteercounterapp.User'),
        ),
    ]
