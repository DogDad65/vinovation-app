from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 

# Define choices as tuples for grape varieties and wine status
GRAPE_VARIETIES = (
    ('CS', 'Cabernet Sauvignon'),
    ('ME', 'Merlot'),
    ('CH', 'Chardonnay'),
    ('PN', 'Pinot Noir'),
    ('RS', 'Riesling'),
    ('CF', 'Cabernet Franc'),
    ('PV', 'Petit Verdot'),
)

WINE_STATUS = (
    ('fermentation', 'Fermentation'),
    ('aging', 'Aging'),
    ('bottling', 'Bottling'),
)

VESSEL_TYPES = (
    ('tank', 'Tank'),
    ('barrel', 'Barrel'),
)

class Vessel(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(help_text="Capacity in liters")
    type = models.CharField(max_length=10, choices=VESSEL_TYPES, default='tank')  # Default set to 'tank'
    material = models.CharField(max_length=50, blank=True, null=True)  # e.g., stainless steel, oak
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vessels")

    def __str__(self):
        return f"{self.name} - {self.type.capitalize()} - {self.capacity}L"


class WineBatch(models.Model):
    lot_name = models.CharField(max_length=100)
    grape_variety = models.CharField(max_length=2, choices=GRAPE_VARIETIES)
    volume = models.FloatField()
    status = models.CharField(max_length=20, choices=WINE_STATUS, default='fermentation')
    date_created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wine_batches')
    vessel = models.ForeignKey(Vessel, on_delete=models.SET_NULL, null=True, blank=True, related_name='wine_batches')

    def __str__(self):
        return f"{self.lot_name} ({self.get_grape_variety_display()})"


class Analysis(models.Model):
    wine_batch = models.ForeignKey(WineBatch, on_delete=models.CASCADE, related_name='analyses')
    date = models.DateField(auto_now_add=True)
    ph = models.FloatField(verbose_name="pH")
    ta = models.FloatField(verbose_name="TA")
    va = models.FloatField(verbose_name="VA")
    so2 = models.FloatField(verbose_name="SO₂")
    brix = models.FloatField(verbose_name="Brix", null=True, blank=True)
    alcohol = models.FloatField(verbose_name="Alcohol (%)", null=True, blank=True)

    def clean(self):
        if self.brix and self.alcohol:
            raise ValidationError("Only one of Brix or Alcohol should be provided, not both.")
        elif not self.brix and not self.alcohol:
            raise ValidationError("Either Brix or Alcohol must be provided.")

    def __str__(self):
        return f"Analysis on {self.date} for {self.wine_batch}"
