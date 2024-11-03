from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import WineBatch


from .models import WineBatch, Analysis
from .forms import WineBatchForm, AnalysisForm

# Landing Page View
class LandingView(TemplateView):
    template_name = 'wines/landing.html'

# Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'wines/dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wine_batches'] = WineBatch.objects.filter(user=self.request.user)
        return context

# User Registration (Signup) View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'wines/signup.html', {'form': form})

# Profile View
@login_required
def profile(request):
    """Displays user profile information."""
    return render(request, 'wines/profile.html')

# Edit Profile View
@login_required
def edit_profile(request):
    """Allows the user to update their profile information."""
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'wines/edit_profile.html', {'form': form})

# WineBatch CRUD Views
@login_required
def create_wine(request):
    """Creates a new wine batch."""
    if request.method == 'POST':
        form = WineBatchForm(request.POST)
        if form.is_valid():
            if WineBatch.objects.filter(lot_name=form.cleaned_data['lot_name'], user=request.user).exists():
                messages.error(request, "A batch with this lot name already exists. Please choose a different name.")
                return redirect('create_wine')
            wine_batch = form.save(commit=False)
            wine_batch.user = request.user
            wine_batch.save()
            return redirect('dashboard')
    else:
        form = WineBatchForm()
    return render(request, 'wines/wine_form.html', {'form': form, 'is_edit': False})

@login_required
def edit_wine(request, wine_id):
    """Edits an existing wine batch for the logged-in user."""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    if request.method == 'POST':
        form = WineBatchForm(request.POST, instance=wine_batch)
        if form.is_valid():
            form.save()
            messages.success(request, "Wine batch updated successfully.")
            return redirect('dashboard')
    else:
        form = WineBatchForm(instance=wine_batch)
    return render(request, 'wines/wine_form.html', {'form': form, 'wine_batch': wine_batch, 'is_edit': True})

@login_required
def delete_wine(request, wine_id):
    """Deletes a wine batch after user confirmation."""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    if request.method == 'POST':
        wine_batch.delete()
        messages.success(request, "Wine batch deleted successfully.")
        return redirect('dashboard')
    return render(request, 'wines/confirm_delete.html', {'wine_batch': wine_batch})

@login_required
def wine_detail(request, wine_id):
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    print("Viewing details for wine batch:", wine_batch)
    return render(request, 'wines/wine_detail.html', {'wine_batch': wine_batch})




@login_required
def winebatch_list(request):
    """Displays a list of all wine batches for the logged-in user."""
    wine_batches = WineBatch.objects.filter(user=request.user)
    print("Wine batches for user:", wine_batches)  # Debugging line
    return render(request, 'wines/wine_list.html', {'wine_batches': wine_batches})




# Analysis CRUD Views
@login_required
def add_analysis(request, wine_id):
    """Adds a new analysis to a specific wine batch."""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.wine_batch = wine_batch
            analysis.save()
            messages.success(request, "New analysis added successfully.")
            return redirect('wine_detail', wine_id=wine_batch.id)
    else:
        form = AnalysisForm()
    return render(request, 'wines/add_analysis.html', {'form': form, 'wine_batch': wine_batch})

@login_required
def edit_analysis(request, wine_id, analysis_id):
    """Edits an existing analysis for a specific wine batch."""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    analysis = get_object_or_404(Analysis, id=analysis_id, wine_batch=wine_batch)

    if request.method == 'POST':
        form = AnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, "Analysis updated successfully.")
            return redirect('wine_detail', wine_id=wine_batch.id)
    else:
        form = AnalysisForm(instance=analysis)
    
    return render(request, 'wines/edit_analysis.html', {'form': form, 'wine_batch': wine_batch, 'analysis': analysis})

@login_required
def delete_analysis(request, wine_id, analysis_id):
    """Deletes an analysis after user confirmation."""
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    analysis = get_object_or_404(Analysis, id=analysis_id, wine_batch=wine_batch)

    if request.method == 'POST':
        analysis.delete()
        messages.success(request, "Analysis deleted successfully.")
        return redirect('wine_detail', wine_id=wine_batch.id)
    
    return render(request, 'wines/delete_analysis.html', {'wine_batch': wine_batch, 'analysis': analysis})
