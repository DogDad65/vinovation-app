from django.urls import path
from .views import LandingView, DashboardView, signup, profile, create_wine, wine_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),  # Landing page
    path('login/', auth_views.LoginView.as_view(template_name='wines/login.html'), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('signup/', signup, name='signup'),  # Sign up page
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Dashboard page
    path('profile/', profile, name='profile'),  # Profile page
    path('create-wine/', create_wine, name='create_wine'),  # Create wine page
    path('wine/<int:wine_id>/', wine_detail, name='wine_detail'),  # Wine detail page
]
