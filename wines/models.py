from django.db import models
from django.contrib.auth.models import User 

class WineBatch(models.Model):
    lot_name = models.CharField(max_length=100)
    grape_variety = models.CharField(max_length=100)
    volume = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('fermentation', 'Fermentation'),
            ('aging', 'Aging'),
            ('bottling', 'Bottling')
        ],
        default='fermentation'
    )
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wine_batches')

    class Meta:
        unique_together = ('user', 'lot_name')  # Enforces unique lot_name per user

    def __str__(self):
        return f"{self.lot_name} ({self.grape_variety})"

