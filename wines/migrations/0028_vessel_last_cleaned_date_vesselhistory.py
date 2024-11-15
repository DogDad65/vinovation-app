# Generated by Django 5.1.3 on 2024-11-14 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0027_alter_vessel_current_wine_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='vessel',
            name='last_cleaned_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='VesselHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_transferred_in', models.DateField(auto_now_add=True)),
                ('date_transferred_out', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('vessel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='wines.vessel')),
                ('wine_batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wines.winebatch')),
            ],
        ),
    ]
