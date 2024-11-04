# wines/forms.py
from django import forms
from .models import WineBatch
from .models import Analysis, Vessel

class WineBatchForm(forms.ModelForm):
    class Meta:
        model = WineBatch
        fields = ['lot_name', 'grape_variety', 'volume', 'status']
        
class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['ph', 'ta', 'va', 'so2', 'brix', 'alcohol']
        
class VesselForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = ['name', 'capacity', 'type', 'material']
        
class WineBatchVesselTransferForm(forms.ModelForm):
    class Meta:
        model = WineBatch
        fields = ['vessel']  # Assuming 'vessel' is the field representing the vessel to which the batch is transferred
        labels = {
            'vessel': 'Select Vessel'
        }
