from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.utils.timezone import now
from django.views.generic import TemplateView
from .models import WineBatch, Vessel, Analysis
from .forms import WineBatchForm, AnalysisForm, VesselForm, WineBatchVesselTransferForm, TransferForm


@login_required
def clean_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)
    vessel.last_cleaned_date = now()
    vessel.save()
    messages.success(request, f"Vessel '{vessel.name}' has been marked as cleaned.")
    return redirect('vessel_detail', vessel_id=vessel.id)

# --- Landing and Dashboard Views ---

class LandingView(TemplateView):
    """View for the landing page"""
    template_name = 'wines/landing.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'wines/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Get the currently logged-in user
        # Filter wine batches by the logged-in user
        context['red_wines'] = WineBatch.objects.filter(category='Red', user=user)
        context['white_wines'] = WineBatch.objects.filter(category='White', user=user)
        return context

# --- Authentication Views ---

def signup(request):
    """User signup view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'wines/signup.html', {'form': form})


# --- Wine Batch Views ---
@login_required
def create_wine(request):
    if request.method == "POST":
        form = WineBatchForm(request.POST, user=request.user)
        if form.is_valid():
            wine_batch = form.save(commit=False)
            wine_batch.user = request.user

            # Perform conversion based on the selected unit
            volume = form.cleaned_data['volume']
            unit = form.cleaned_data['volume_unit']

            if unit == 'gallons':
                wine_batch.volume = volume * 3.785  # Convert gallons to liters
            elif unit == 'tons':
                wine_batch.volume = volume * 1000  # Convert tons to liters
            else:
                wine_batch.volume = volume

            wine_batch.save()
            messages.success(request, "Wine batch created successfully.")
            return redirect('wine_list')
    else:
        form = WineBatchForm(user=request.user)

    return render(request, 'wines/shared_form.html', {
        'form': form,
        'title': 'Create Wine Batch',
        'button_text': 'Save Wine Batch',
    })


@login_required
def edit_wine(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WineBatchForm(request.POST, instance=wine, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Wine batch updated successfully.")
            return redirect('wine_detail', pk=wine.pk)
    else:
        form = WineBatchForm(instance=wine, user=request.user)

    return render(request, 'wines/shared_form.html', {
        'form': form,
        'title': f"Edit Wine Batch: {wine.lot_name}",
        'button_text': 'Save Changes',
    })


@login_required
def wine_list(request):
    search_query = request.GET.get('search', '')
    wine_batches = WineBatch.objects.filter(user=request.user, lot_name__icontains=search_query)
    paginator = Paginator(wine_batches, 10)  # Paginate the filtered results
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'wines/wine_list.html', {'page_obj': page_obj, 'search_query': search_query})

@login_required
def wine_detail(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk, user=request.user)  # Ensure wine batch belongs to the user
    analyses = wine.analyses.all().order_by('-date')  # Fetch all related analyses
    return render(request, 'wines/wine_detail.html', {'wine': wine, 'analyses': analyses})

def delete_wine(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk, user=request.user)  # Ensure the wine batch belongs to the user
    if request.method == 'POST':
        wine.delete()
        messages.success(request, "Wine batch deleted successfully.")
        return redirect('wine_list')
    return render(request, 'wines/confirm_delete.html', {'wine': wine})

# --- Analysis Views ---

@login_required
def add_analysis(request, wine_id):
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.wine_batch = wine_batch
            analysis.save()
            messages.success(request, "Analysis added successfully.")
            return redirect('wine_detail', pk=wine_batch.id)
    else:
        form = AnalysisForm()
    
    return render(request, 'wines/shared_form.html', {
        'form': form,
        'title': f"Add Analysis for {wine_batch.lot_name}",
        'button_text': 'Save Analysis'
    })


def edit_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)  # Fetch the analysis object
    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, "Analysis updated successfully.")
            return redirect('wine_detail', pk=analysis.wine_batch.pk)
    else:
        form = AnalysisForm(instance=analysis)
    return render(request, 'wines/edit_analysis.html', {'form': form, 'analysis': analysis})

def delete_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)  # Fetch the analysis object
    wine_batch_id = analysis.wine_batch.pk
    if request.method == 'POST':
        analysis.delete()
        messages.success(request, "Analysis deleted successfully.")
        return redirect('wine_detail', pk=wine_batch_id)
    return render(request, 'wines/delete_analysis.html', {'analysis': analysis})

# --- Vessel Views ---
@login_required
def vessel_list(request):
    vessels_red = Vessel.objects.filter(user=request.user, type='tank', fermentor_type='Red')
    vessels_white = Vessel.objects.filter(user=request.user, type='tank', fermentor_type='White')
    vessels_barrels = Vessel.objects.filter(user=request.user, type='barrel')
    return render(request, 'wines/vessel_list.html', {
        'vessels_red': vessels_red,
        'vessels_white': vessels_white,
        'vessels_barrels': vessels_barrels,
    })

@login_required
def create_vessel(request):
    if request.method == "POST":
        form = VesselForm(request.POST, user=request.user)  # Pass user to form
        if form.is_valid():
            vessel = form.save(commit=False)
            vessel.user = request.user
            vessel.save()
            messages.success(request, "Vessel created successfully.")
            return redirect('vessel_list')
    else:
        form = VesselForm(user=request.user)

    return render(request, 'wines/shared_form.html', {
        'form': form,
        'title': 'Create Vessel',
        'button_text': 'Save Vessel',
    })

@login_required
def delete_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)  # Ensure the vessel belongs to the user
    if request.method == 'POST':
        vessel.delete()
        messages.success(request, "Vessel deleted successfully.")
        return redirect('vessel_list')
    return render(request, 'wines/confirm_delete.html', {'vessel': vessel})

# Vessel detail view
@login_required
def vessel_detail(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)  # Ensure the vessel belongs to the user
    return render(request, 'wines/vessel_detail.html', {'vessel': vessel})

@login_required
def edit_vessel(request, vessel_id):
    # Fetch the vessel object for the logged-in user
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)
    if request.method == "POST":
        # Bind the submitted data to the VesselForm
        form = VesselForm(request.POST, instance=vessel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vessel '{vessel.name}' updated successfully.")
            return redirect('vessel_list')  # Redirect to the vessel list page
    else:
        # Initialize the form with the current vessel data
        form = VesselForm(instance=vessel)

    # Render the shared_form template for editing
    return render(request, 'wines/shared_form.html', {
        'form': form,
        'title': f"Edit Vessel: {vessel.name}",
        'button_text': "Save Changes"
    })

@login_required
def transfer_to_vessel(request, wine_id):
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    vessels = Vessel.objects.filter(user=request.user)
    current_vessel = wine_batch.vessel

    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            selected_vessel = form.cleaned_data['vessel']
            blend_confirmation = form.cleaned_data.get('blend_confirmation', False)

            # Validate transfer logic
            is_valid, error_message = validate_transfer(selected_vessel, wine_batch, blend_confirmation)
            if not is_valid:
                messages.error(request, error_message)
                return render(request, 'wines/transfer_to_vessel.html', {
                    'form': form,
                    'wine_batch': wine_batch,
                    'vessels': vessels,
                    'current_vessel': current_vessel,
                })

            # Perform transfer
            selected_vessel.current_wine_batch = wine_batch
            selected_vessel.current_capacity += wine_batch.volume
            selected_vessel.save()

            wine_batch.vessel = selected_vessel
            wine_batch.save()

            messages.success(request, f"Wine batch '{wine_batch.lot_name}' successfully transferred to vessel '{selected_vessel.name}'.")
            return redirect('wine_detail', pk=wine_batch.id)
    else:
        form = TransferForm(user=request.user)

    return render(request, 'wines/transfer_to_vessel.html', {
        'form': form,
        'wine_batch': wine_batch,
        'vessels': vessels,
        'current_vessel': current_vessel,
    })

def validate_transfer(selected_vessel, wine_batch, blend_confirmation):
    # Check if the vessel is occupied and blending is not confirmed
    if selected_vessel.current_wine_batch and not blend_confirmation:
        return False, f"Vessel '{selected_vessel.name}' is already occupied by '{selected_vessel.current_wine_batch.lot_name}'."
    # Check if the vessel has enough capacity (optional)
    if selected_vessel.current_capacity + wine_batch.volume > selected_vessel.capacity:
        return False, f"Vessel '{selected_vessel.name}' does not have enough capacity for the transfer."
    return True, ""

@login_required
def success_page(request):
    return render(request, 'wines/success.html')



