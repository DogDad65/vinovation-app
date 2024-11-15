from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import edit_wine

# Authentication URLs
auth_patterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='wines/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Main URL Patterns
wine_patterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Wine URLs
    path('wine/create/', views.create_wine, name='create_wine'),
    path('wines/', views.wine_list, name='wine_list'),
    path('wine/<int:pk>/', views.wine_detail, name='wine_detail'),
    path('wine/<int:wine_id>/add-analysis/', views.add_analysis, name='add_analysis'),
    path('wine/<int:pk>/edit/', edit_wine, name='edit_wine'),
    path('wine/<int:pk>/delete/', views.delete_wine, name='delete_wine'),
    path('analysis/<int:analysis_id>/edit/', views.edit_analysis, name='edit_analysis'),
    path('analysis/<int:analysis_id>/delete/', views.delete_analysis, name='delete_analysis'),
    path('wine/<int:wine_id>/transfer/', views.transfer_to_vessel, name='transfer_to_vessel'),
    
    # New success page URL
    path('transfer/success/', views.success_page, name='transfer_success'),  

    # Vessel URLs
    path('vessels/', views.vessel_list, name='vessel_list'),
    path('vessels/create/', views.create_vessel, name='create_vessel'),
    path('vessels/<int:vessel_id>/', views.vessel_detail, name='vessel_detail'),
    path('vessels/<int:vessel_id>/clean/', views.clean_vessel, name='clean_vessel'),
    path('vessels/<int:vessel_id>/edit/', views.edit_vessel, name='edit_vessel'),
    path('vessels/<int:vessel_id>/delete/', views.delete_vessel, name='delete_vessel'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Combine all URL patterns
urlpatterns = auth_patterns + wine_patterns
