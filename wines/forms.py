from django import forms
from .models import WineBatch, Analysis, Vessel
from django.core.exceptions import ValidationError


class WineBatchForm(forms.ModelForm):
    class Meta:
        model = WineBatch
        fields = [
            'lot_name', 'category', 'grape_variety', 'volume', 'vineyard',
            'ava', 'vessel', 'status', 'vintage', 'source', 'notes'
        ]

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
        fields = ['name', 'capacity', 'type', 'material', 'manufacturer', 'fermentor_type', 'current_capacity']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Accept user as a parameter
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Use the user passed in the form initialization or raise an error if unavailable
        if not self.user:
            raise ValidationError("User is required to validate vessel uniqueness.")

        # Check if a vessel with the same name already exists for this user
        if Vessel.objects.filter(name=name, user=self.user).exists():
            raise ValidationError(f"A vessel named '{name}' already exists for you.")
        return name



class WineBatchVesselTransferForm(forms.ModelForm):
    vessel = forms.ModelChoiceField(queryset=Vessel.objects.all(), label="Select Vessel")

    class Meta:
        model = WineBatch
        fields = ['vessel']
        
class TransferForm(forms.ModelForm):
    vessel = forms.ModelChoiceField(queryset=Vessel.objects.all(), label="Select Vessel")

    class Meta:
        model = Vessel  # This can be adjusted based on what you want to transfer
        fields = ['vessel']  # You can adjust this according to your needs