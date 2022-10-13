# Generated by Django 4.1 on 2022-10-11 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hungry', '0003_remove_price_good_good_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='price',
        ),
        migrations.AddField(
            model_name='price',
            name='good',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price', to='hungry.good'),
        ),
        migrations.AlterField(
            model_name='price',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='hungry.place'),
        ),
    ]
