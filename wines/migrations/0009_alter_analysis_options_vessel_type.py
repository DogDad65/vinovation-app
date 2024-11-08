# Generated by Django 5.1.2 on 2024-11-03 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0008_alter_winebatch_unique_together_winebatch_vessel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='analysis',
            options={},
        ),
        migrations.AddField(
            model_name='vessel',
            name='type',
            field=models.CharField(choices=[('tank', 'Tank'), ('barrel', 'Barrel')], default='tank', max_length=10),
            preserve_default=False,
        ),
    ]
