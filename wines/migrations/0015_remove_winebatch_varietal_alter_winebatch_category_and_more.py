# Generated by Django 5.1.2 on 2024-11-04 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0014_remove_winebatch_date_created_remove_winebatch_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winebatch',
            name='varietal',
        ),
        migrations.AlterField(
            model_name='winebatch',
            name='category',
            field=models.CharField(choices=[('Red', 'Red'), ('White', 'White'), ('Sparkling', 'Sparkling'), ('Dessert', 'Dessert'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='winebatch',
            name='grape_variety',
            field=models.CharField(choices=[('CS', 'Cabernet Sauvignon'), ('ME', 'Merlot'), ('CH', 'Chardonnay'), ('PN', 'Pinot Noir'), ('RS', 'Riesling'), ('CF', 'Cabernet Franc'), ('PV', 'Petit Verdot')], max_length=2),
        ),
        migrations.AlterField(
            model_name='winebatch',
            name='status',
            field=models.CharField(blank=True, choices=[('fermentation', 'Fermentation'), ('aging', 'Aging'), ('bottling', 'Bottling')], max_length=20, null=True),
        ),
    ]
