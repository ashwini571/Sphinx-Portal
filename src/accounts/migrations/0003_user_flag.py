# Generated by Django 2.1.3 on 2019-04-11 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190409_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
