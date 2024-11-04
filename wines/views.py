from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import WineBatch, Vessel, Analysis
from django.views.generic import TemplateView  
from .forms import WineBatchForm, AnalysisForm, VesselForm, WineBatchVesselTransferForm


from .models import WineBatch, Analysis, Vessel
from .forms import WineBatchForm, AnalysisForm, VesselForm, WineBatchVesselTransferForm

# --- Landing and Dashboard Views ---

class LandingView(TemplateView):
    """View for the landing page"""
    template_name = 'wines/landing.html'


class DashboardView(TemplateView):
    template_name = 'wines/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adjust filter to match actual values
        context['red_wines'] = WineBatch.objects.filter(user=self.request.user, grape_variety__in=['CS', 'ME'])
        # Assuming you have other values for white wines, add them here
        context['white_wines'] = WineBatch.objects.filter(user=self.request.user, grape_variety__in=['CH', 'SB'])  # Example varieties
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
    if request.method == 'POST':
        form = WineBatchForm(request.POST)
        if form.is_valid():
            wine_batch = form.save(commit=False)
            wine_batch.user = request.user
            wine_batch.save()
            return redirect('dashboard')
    else:
        form = WineBatchForm()
    return render(request, 'wines/wine_form.html', {'form': form})

@login_required
def wine_list(request):
    wines = WineBatch.objects.filter(user=request.user)
    return render(request, 'wines/wine_list.html', {'wines': wines})

@login_required
def wine_detail(request, wine_id):
    """Detail view for a single wine batch"""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    return render(request, 'wines/wine_detail.html', {'wine_batch': wine_batch})


# --- Analysis Views ---

@login_required
def add_analysis(request, wine_id):
    """View to add analysis to a specific wine batch"""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.wine_batch = wine_batch
            analysis.save()
            messages.success(request, "Analysis added successfully.")
            return redirect('wine_detail', wine_id=wine_batch.id)
    else:
        form = AnalysisForm()
    return render(request, 'wines/analysis_form.html', {'form': form, 'wine_batch': wine_batch})


# --- Vessel Transfer Views ---
@login_required
def vessel_list(request):
    vessels = Vessel.objects.filter(user=request.user)  # Assuming vessels are associated with users
    return render(request, 'wines/vessel_list.html', {'vessels': vessels})

@login_required
def create_vessel(request):
    if request.method == 'POST':
        form = VesselForm(request.POST)
        if form.is_valid():
            vessel = form.save(commit=False)
            vessel.user = request.user
            vessel.save()
            return redirect('vessel_list')
    else:
        form = VesselForm()
    return render(request, 'wines/vessel_form.html', {'form': form})

@login_required
def edit_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)
    if request.method == 'POST':
        form = VesselForm(request.POST, instance=vessel)
        if form.is_valid():
            form.save()
            messages.success(request, "Vessel updated successfully.")
            return redirect('vessel_detail', vessel_id=vessel.id)
    else:
        form = VesselForm(instance=vessel)
    return render(request, 'wines/vessel_form.html', {'form': form, 'vessel': vessel})


@login_required
def delete_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)
    if request.method == 'POST':
        vessel.delete()
        messages.success(request, "Vessel deleted successfully.")
        return redirect('vessel_list')
    return redirect('vessel_detail', vessel_id=vessel.id)


# Vessel detail view
@login_required
def vessel_detail(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)
    return render(request, 'wines/vessel_detail.html', {'vessel': vessel})

@login_required
def edit_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id, user=request.user)
    if request.method == 'POST':
        form = VesselForm(request.POST, instance=vessel)
        if form.is_valid():
            form.save()
            messages.success(request, "Vessel updated successfully.")
            return redirect('vessel_list')
    else:
        form = VesselForm(instance=vessel)
    return render(request, 'wines/vessel_form.html', {'form': form})


@login_required
def transfer_to_vessel(request, wine_id):
    """View to transfer a wine batch to a vessel"""
    # Fetch the WineBatch instance, ensuring it belongs to the logged-in user
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    
    # If the request method is POST, process the form data
    if request.method == 'POST':
        form = WineBatchVesselTransferForm(request.POST, instance=wine_batch)
        if form.is_valid():
            form.save()  # Save the transfer form
            messages.success(request, "Transferred to vessel successfully.")
            return redirect('wine_detail', wine_id=wine_batch.id)  # Redirect to the wine detail page
    
    # If the request method is GET, display the empty form
    else:
        form = WineBatchVesselTransferForm(instance=wine_batch)

    # Render the transfer_to_vessel template
    return render(request, 'wines/transfer_to_vessel.html', {'form': form, 'wine_batch': wine_batch})
