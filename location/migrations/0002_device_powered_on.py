# Generated by Django 4.2.7 on 2023-11-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='powered_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
