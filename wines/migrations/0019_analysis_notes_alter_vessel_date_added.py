# Generated by Django 5.1.2 on 2024-11-06 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0018_vessel_date_added_vessel_fermentor_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]