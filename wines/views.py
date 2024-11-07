from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from .models import WineBatch, Vessel, Analysis
from .forms import WineBatchForm, AnalysisForm, VesselForm, WineBatchVesselTransferForm, TransferForm

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
    if request.method == 'POST':
        form = WineBatchForm(request.POST)
        if form.is_valid():
            wine_batch = form.save(commit=False)
            wine_batch.user = request.user  # Assign the logged-in user to the wine batch
            wine_batch.save()
            messages.success(request, "Wine batch created successfully.")
            return redirect('wine_list')
        else:
            # Log form errors to help identify the issue
            print("Form errors:", form.errors)
            messages.error(request, "There was an error saving the wine batch. Please check your input.")
    else:
        form = WineBatchForm()

    # Fetch vessels belonging to the logged-in user to populate the dropdown
    vessels = Vessel.objects.filter(user=request.user)  # Only vessels for the logged-in user
    return render(request, 'wines/wine_form.html', {'form': form, 'vessels': vessels})



@login_required
def wine_list(request):
    # Fetch only the wine batches belonging to the logged-in user
    wines = WineBatch.objects.filter(user=request.user)  # Filter by user
    return render(request, 'wines/wine_list.html', {'wines': wines})

@login_required
def wine_detail(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk, user=request.user)  # Ensure wine batch belongs to the user
    analyses = wine.analyses.all().order_by('-date')  # Fetch all related analyses
    return render(request, 'wines/wine_detail.html', {'wine': wine, 'analyses': analyses})

@login_required
def edit_wine(request, pk):
    wine = get_object_or_404(WineBatch, pk=pk, user=request.user)  # Ensure the wine belongs to the logged-in user
    if request.method == 'POST':
        form = WineBatchForm(request.POST, instance=wine)
        if form.is_valid():
            form.save()
            messages.success(request, "Wine batch updated successfully.")
            return redirect('wine_detail', pk=wine.pk)  # Redirect to the wine detail page
    else:
        form = WineBatchForm(instance=wine) 

    return render(request, 'wines/edit_wine.html', {'form': form, 'wine': wine})




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
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)  # Ensure the wine batch belongs to the user
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.wine_batch = wine_batch
            analysis.save()
            messages.success(request, "Analysis added successfully.")
            return redirect('wine_detail', pk=wine_batch.id)  # Use pk instead of wine_id here
    else:
        form = AnalysisForm()
    return render(request, 'wines/analysis_form.html', {'form': form, 'wine_batch': wine_batch})

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
    vessels = Vessel.objects.filter(user=request.user)  # Fetch only vessels belonging to the logged-in user
    return render(request, 'wines/vessel_list.html', {'vessels': vessels})

@login_required
def create_vessel(request):
    if request.method == 'POST':
        form = VesselForm(request.POST)
        if form.is_valid():
            vessel = form.save(commit=False)
            vessel.user = request.user  # Assign the logged-in user
            vessel.save()
            messages.success(request, "Vessel created successfully.")
            return redirect('vessel_list')
    else:
        form = VesselForm()
    return render(request, 'wines/vessel_form.html', {'form': form})

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

def edit_vessel(request, vessel_id):
    vessel = get_object_or_404(Vessel, id=vessel_id)
    if request.method == 'POST':
        form = VesselForm(request.POST, instance=vessel)
        if form.is_valid():
            form.save()
            # Redirect to a success page or the vessel detail view
    else:
        form = VesselForm(instance=vessel)
    return render(request, 'wines/vessel_form.html', {'form': form, 'vessel': vessel})


@login_required
def transfer_to_vessel(request, wine_id):
    wine_batch = get_object_or_404(WineBatch, id=wine_id)
    vessels = Vessel.objects.filter(user=request.user)  # Ensure only the user's vessels are shown
    form = TransferForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        selected_vessel = form.cleaned_data['vessel']

        # Check if the selected vessel is full
        if selected_vessel.current_capacity + wine_batch.volume > selected_vessel.capacity:
            messages.error(request, 'Transfer failed: The selected vessel will be overfilled.')
            return render(request, 'wines/transfer_to_vessel.html', {'form': form, 'wine_batch': wine_batch, 'vessels': vessels})

        # Check if the selected vessel already contains a different lot of wine
        if selected_vessel.current_wine_batch and selected_vessel.current_wine_batch != wine_batch:
            messages.error(request, 'Transfer failed: The selected vessel already contains another wine lot.')
            return render(request, 'wines/transfer_to_vessel.html', {'form': form, 'wine_batch': wine_batch, 'vessels': vessels})

        # If validations pass, proceed with the transfer
        selected_vessel.current_wine_batch = wine_batch  # Update the current wine batch in the vessel
        selected_vessel.current_capacity += wine_batch.volume  # Update the current capacity
        selected_vessel.save()

        # Optionally, update the wine batch status
        wine_batch.current_vessel = selected_vessel
        wine_batch.save()

        # Success message and redirection
        messages.success(request, 'Transfer successful!')
        return redirect('transfer_success')  # Redirect to the new success page

    return render(request, 'wines/transfer_to_vessel.html', {'form': form, 'wine_batch': wine_batch, 'vessels': vessels})




@login_required
def success_page(request):
    return render(request, 'wines/success.html')



