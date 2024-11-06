from django.contrib import admin
from .models import WineBatch, Vessel, Analysis

@admin.register(WineBatch)
class WineBatchAdmin(admin.ModelAdmin):
    list_display = ('lot_name', 'vintage', 'category', 'grape_variety', 'volume', 'status', 'vessel')

@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    # Removed 'location' since it's not a field in the Vessel model
    list_display = ('name', 'capacity')

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('wine_batch', 'date', 'ph', 'ta', 'so2', 'brix', 'alcohol')
