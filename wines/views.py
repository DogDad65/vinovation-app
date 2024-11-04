from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import WineBatch, Vessel, Analysis
from .forms import WineForm
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
        # Query red and white wines without filtering by user
        context['red_wines'] = WineBatch.objects.filter(category='Red')
        context['white_wines'] = WineBatch.objects.filter(category='White')
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
            wine_batch.save()
            return redirect('dashboard')
    else:
        form = WineBatchForm()
    return render(request, 'wines/wine_form.html', {'form': form})


@login_required
def wine_list(request):
    wines = WineBatch.objects.all()
    return render(request, 'wines/wine_list.html', {'wines': wines})


@login_required
def wine_detail(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk)
    analyses = wine.analyses.all().order_by('-date')  # Fetch all related analyses
    return render(request, 'wines/wine_detail.html', {'wine': wine, 'analyses': analyses})

def edit_wine(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk)
    if request.method == 'POST':
        form = WineForm(request.POST, instance=wine)
        if form.is_valid():
            form.save()
            return redirect('wine_detail', pk=wine.pk)
    else:
        form = WineForm(instance=wine)
    return render(request, 'wines/edit_wine.html', {'form': form, 'wine': wine})

def delete_wine(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk)
    if request.method == 'POST':
        wine.delete()
        return redirect('dashboard')  # Or redirect to any page where you list the wines
    return render(request, 'wines/confirm_delete.html', {'wine': wine})



# --- Analysis Views ---

@login_required
def add_analysis(request, wine_id):
    wine_batch = get_object_or_404(WineBatch, id=wine_id)
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


from django.shortcuts import redirect

def edit_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)
    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            return redirect('wine_detail', pk=analysis.wine_batch.pk)
    else:
        form = AnalysisForm(instance=analysis)
    return render(request, 'wines/edit_analysis.html', {'form': form, 'analysis': analysis})

def delete_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)
    wine_batch_id = analysis.wine_batch.pk
    if request.method == 'POST':
        analysis.delete()
        return redirect('wine_detail', pk=wine_batch_id)
    return render(request, 'wines/delete_analysis.html', {'analysis': analysis})



# --- Vessel Transfer Views ---
@login_required
def vessel_list(request):
    vessels = Vessel.objects.all()
    return render(request, 'wines/vessel_list.html', {'vessels': vessels})

@login_required
def create_vessel(request):
    if request.method == 'POST':
        form = VesselForm(request.POST)
        if form.is_valid():
            vessel = form.save(commit=False)
            vessel.user = request.user  # Assign the logged-in user
            vessel.save()
            return redirect('vessel_list')
    else:
        form = VesselForm()
    return render(request, 'wines/vessel_form.html', {'form': form})


@login_required
def edit_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id)
    if request.method == 'POST':
        form = VesselForm(request.POST, instance=vessel)
        if form.is_valid():
            form.save()
            messages.success(request, "Vessel updated successfully.")
            return redirect('vessel_list')
    else:
        form = VesselForm(instance=vessel)
    return render(request, 'wines/vessel_form.html', {'form': form, 'vessel': vessel})

@login_required
def delete_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id)
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
    wine_batch = get_object_or_404(WineBatch, id=wine_id)
    if request.method == 'POST':
        form = WineBatchVesselTransferForm(request.POST, instance=wine_batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Transferred to vessel successfully.")
            return redirect('wine_detail', wine_id=wine_batch.id)
    else:
        form = WineBatchVesselTransferForm(instance=wine_batch)
    return render(request, 'wines/transfer_to_vessel.html', {'form': form, 'wine_batch': wine_batch})

