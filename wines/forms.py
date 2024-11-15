from django import forms
from .models import WineBatch, Analysis, Vessel
from django.core.exceptions import ValidationError


# Form for WineBatch
class WineBatchForm(forms.ModelForm):
    class Meta:
        model = WineBatch
        fields = [
            'lot_name', 'category', 'grape_variety', 'volume', 'vintage',
            'vessel', 'status', 'source', 'notes', 'vineyard', 'ava'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user if needed
        super().__init__(*args, **kwargs)
        if user:
            # Customize the vessel queryset for the user
            self.fields['vessel'].queryset = Vessel.objects.filter(user=user)

# Form for Analysis
class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['date', 'ph', 'ta', 'va', 'so2', 'brix', 'alcohol', 'frequency', 'notes']

# Form for Vessel
class VesselForm(forms.ModelForm):
    class Meta:
        model = Vessel
        fields = ['name', 'capacity', 'type', 'material', 'manufacturer', 'fermentor_type', 'current_wine_batch']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pass the user to filter wine batches
        super().__init__(*args, **kwargs)
        
        # Filter current wine batch dropdown to show only the user's batches
        if self.user:
            self.fields['current_wine_batch'].queryset = WineBatch.objects.filter(user=self.user)

        # Add placeholders or default values for form fields, if needed
        self.fields['current_wine_batch'].required = False


# Form for WineBatch Vessel Transfer
class WineBatchVesselTransferForm(forms.ModelForm):
    vessel = forms.ModelChoiceField(
        queryset=Vessel.objects.none(),  # Default to an empty queryset
        label="Select Vessel",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = WineBatch
        fields = ['vessel']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user
        super().__init__(*args, **kwargs)
        if user:
            # Populate the queryset with only vessels belonging to the user
            self.fields['vessel'].queryset = Vessel.objects.filter(user=user)


# General Form for Vessel Transfer
class TransferForm(forms.Form):
    vessel = forms.ModelChoiceField(
        queryset=Vessel.objects.none(),
        label="Select Vessel",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    blend_confirmation = forms.BooleanField(
        required=False,
        label="I intend to blend the wine in the selected vessel",
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vessel'].queryset = Vessel.objects.filter(user=user)



