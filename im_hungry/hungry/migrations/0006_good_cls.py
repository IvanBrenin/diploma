# Generated by Django 4.1 on 2022-10-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hungry', '0005_place_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='cls',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]