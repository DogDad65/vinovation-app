# Generated by Django 5.1.2 on 2024-11-02 17:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0003_alter_winebatch_grape_variety'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_performed', models.DateField(auto_now_add=True)),
                ('ph', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('ta', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Total Acidity (g/L)')),
                ('va', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Volatile Acidity (g/L)')),
                ('so2', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='SO2 (ppm)')),
                ('brix', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Brix (%)')),
                ('alcohol', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Alcohol (%)')),
                ('wine_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='wines.winebatch')),
            ],
        ),
    ]