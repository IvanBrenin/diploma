# Generated by Django 4.1 on 2022-10-16 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hungry', '0016_alter_good_cls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='user_photo',
        ),
    ]
