# Generated by Django 2.1.7 on 2019-04-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_graded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answersheet',
            name='is_graded',
            field=models.BooleanField(default=False),
        ),
    ]
