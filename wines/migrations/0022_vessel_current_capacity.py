# Generated by Django 5.1.3 on 2024-11-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0021_remove_vessel_current_capacity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vessel',
            name='current_capacity',
            field=models.IntegerField(default=0),
        ),
    ]