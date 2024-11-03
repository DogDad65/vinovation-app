# wines/forms.py
from django import forms
from .models import WineBatch
from .models import Analysis

class WineBatchForm(forms.ModelForm):
    class Meta:
        model = WineBatch
        fields = ['lot_name', 'grape_variety', 'volume', 'status']
        
class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['ph', 'ta', 'va', 'so2', 'brix', 'alcohol']
