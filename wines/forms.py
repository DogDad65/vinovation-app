from django import forms
from .models import WineBatch, Analysis, Vessel

class WineBatchForm(forms.ModelForm):
    class Meta:
        model = WineBatch
        fields = [
            'lot_name', 'category', 'grape_variety', 'volume', 'vineyard',
            'ava', 'vessel', 'status', 'vintage', 'source', 'notes'
        ]
        # No need to redefine widgets for fields with choices, Django will handle it
        widgets = {
            'vessel': forms.Select(),  # Dynamically populated by Vessel instances
        }

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['ph', 'ta', 'va', 'so2', 'brix', 'alcohol', 'notes']

class VesselForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = ['name', 'capacity', 'type', 'material', 'user','manufacturer', 'fermentor_type']

class WineBatchVesselTransferForm(forms.ModelForm):
    vessel = forms.ModelChoiceField(queryset=Vessel.objects.all(), label="Select Vessel")

    class Meta:
        model = WineBatch
        fields = ['vessel']