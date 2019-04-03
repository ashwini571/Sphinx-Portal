# Generated by Django 2.1.7 on 2019-04-03 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='code',
            field=models.TextField(default='', max_length=2000),
        ),
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='questions/'),
        ),
    ]
