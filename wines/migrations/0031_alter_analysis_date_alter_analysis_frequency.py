# Generated by Django 5.1.3 on 2024-11-15 15:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0030_analysis_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='frequency',
            field=models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=50),
        ),
    ]
