# Generated by Django 4.1 on 2022-10-14 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hungry', '0012_good_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
