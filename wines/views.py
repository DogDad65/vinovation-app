from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WineBatch
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Landing Page View
class LandingView(TemplateView):
    template_name = 'wines/landing.html'

# Dashboard View
class DashboardView(TemplateView):
    template_name = 'wines/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch only wine batches associated with the logged-in user
        context['wine_batches'] = WineBatch.objects.filter(user=self.request.user)
        return context

@login_required
def create_wine(request):
    if request.method == 'POST':
        lot_name = request.POST.get('lot_name')
        grape_variety = request.POST.get('grape_variety')
        volume = request.POST.get('volume')
        status = request.POST.get('status')
        
        # Check if the lot_name already exists for this user
        if WineBatch.objects.filter(lot_name=lot_name, user=request.user).exists():
            messages.error(request, "A batch with this lot name already exists. Please choose a different name.")
            return redirect('create_wine')  # Redirect back to the creation form

        # Create the WineBatch instance
        WineBatch.objects.create(
            lot_name=lot_name,
            grape_variety=grape_variety,
            volume=volume,
            status=status,
            user=request.user
        )
        return redirect('dashboard')
    
    return render(request, 'wines/create_wine.html')

@login_required
def wine_detail(request, wine_id):
    wine_batch = get_object_or_404(WineBatch, id=wine_id, user=request.user)
    return render(request, 'wines/wine_detail.html', {'wine_batch': wine_batch})

@login_required
def profile(request):
    return render(request, 'wines/profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'wines/signup.html', {'form': form})
@login_required
def winebatch_list(request):
    # Fetch all wine batches associated with the logged-in user
    wine_batches = WineBatch.objects.filter(user=request.user)
    return render(request, 'wines/winebatch_list.html', {'wine_batches': wine_batches})
