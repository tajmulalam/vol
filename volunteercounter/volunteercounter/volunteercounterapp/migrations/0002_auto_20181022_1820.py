# Generated by Django 2.1.2 on 2018-10-22 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteercounterapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qrscandata',
            old_name='uploadedAt',
            new_name='scannedAt',
        ),
    ]