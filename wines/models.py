from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError 

# Define choices as tuples for grape varieties, wine categories, wine status, and vessel types
GRAPE_VARIETIES = (
    ('CS', 'Cabernet Sauvignon'),
    ('ME', 'Merlot'),
    ('CH', 'Chardonnay'),
    ('PN', 'Pinot Noir'),
    ('RS', 'Riesling'),
    ('CF', 'Cabernet Franc'),
    ('PV', 'Petit Verdot'),
    ('AG', 'Aglianico'),
    ('SA', 'Sauvignon Blanc'),
    ('CA', 'Carmenère'),
    ('SC', 'Sangiovese'),
    ('SL', 'Syrah'),
    ('FR', 'Franc'),
    ('MO', 'Moscato'),
    ('GR', 'Grenache'),
    ('VB', 'Verdelho Blanc'),
    ('VBG', 'Verdelho Grenache'),
)

WINE_CATEGORIES = (
    ('Red', 'Red'),
    ('White', 'White'),
    ('Sparkling', 'Sparkling'),
    ('Dessert', 'Dessert'),
    ('Other', 'Other'),
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

FERMENTOR_CHOICES = (
    ('Red', 'Red'),
    ('White', 'White'),
    ('Sparkling', 'Sparkling'),
)

class WineBatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wine_batches")
    lot_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=WINE_CATEGORIES)
    grape_variety = models.CharField(max_length=20, choices=GRAPE_VARIETIES)
    volume = models.DecimalField(max_digits=5, decimal_places=1)
    vineyard = models.CharField(max_length=100, null=True, blank=True)
    ava = models.CharField(max_length=100, null=True, blank=True)
    vessel = models.ForeignKey('Vessel', on_delete=models.SET_NULL, null=True, blank=True)  # Use 'Vessel' as a string for forward declaration
    status = models.CharField(max_length=20, choices=WINE_STATUS, null=True, blank=True)
    vintage = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        variety = dict(GRAPE_VARIETIES).get(self.grape_variety, self.grape_variety)
        return f"{self.lot_name} ({variety})"

class Vessel(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(help_text="Capacity in liters")
    current_capacity = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=VESSEL_TYPES, default='tank')
    material = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vessels")
    date_added = models.DateField(auto_now_add=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    fermentor_type = models.CharField(max_length=10, choices=FERMENTOR_CHOICES, default='Red')
    current_wine_batch = models.ForeignKey(WineBatch, null=True, blank=True, on_delete=models.SET_NULL, related_name='current_vessels')

    def __str__(self):
        return f"{self.name} - {self.type.capitalize()} - {self.capacity}L"



class Analysis(models.Model):
    wine_batch = models.ForeignKey(WineBatch, on_delete=models.CASCADE, related_name='analyses')
    date = models.DateField(auto_now_add=True)
    ph = models.FloatField(verbose_name="pH")
    ta = models.FloatField(verbose_name="TA")
    va = models.FloatField(verbose_name="VA")
    so2 = models.FloatField(verbose_name="SO₂")
    brix = models.FloatField(verbose_name="Brix", null=True, blank=True)
    alcohol = models.FloatField(verbose_name="Alcohol (%)", null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if self.brix and self.alcohol:
            raise ValidationError("Only one of Brix or Alcohol should be provided, not both.")
        elif not self.brix and not self.alcohol:
            raise ValidationError("Either Brix or Alcohol must be provided.")

    def __str__(self):
        return f"Analysis on {self.date} for {self.wine_batch}"
