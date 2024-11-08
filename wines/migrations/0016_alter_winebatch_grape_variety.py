# Generated by Django 5.1.2 on 2024-11-04 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wines', '0015_remove_winebatch_varietal_alter_winebatch_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winebatch',
            name='grape_variety',
            field=models.CharField(choices=[('CS', 'Cabernet Sauvignon'), ('ME', 'Merlot'), ('CH', 'Chardonnay'), ('PN', 'Pinot Noir'), ('RS', 'Riesling'), ('CF', 'Cabernet Franc'), ('PV', 'Petit Verdot'), ('AG', 'Aglianico'), ('SA', 'Sauvignon Blanc'), ('CA', 'Carmenère'), ('SC', 'Sangiovese'), ('SL', 'Syrah'), ('FR', 'Franc'), ('MO', 'Moscato'), ('GR', 'Grenache'), ('VB', 'Verdelho Blanc'), ('VBG', 'Verdelho Grenache')], max_length=20),
        ),
    ]
