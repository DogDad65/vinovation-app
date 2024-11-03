from django.urls import path
from . import views
from .views import LandingView, DashboardView, signup, profile, create_wine, wine_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='wines/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='wines/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='wines/password_change_done.html'), name='password_change_done'),
    path('wine/', views.winebatch_list, name='wine_list'),  # <- Check for comma here

    path('create-wine/', views.create_wine, name='create_wine'),  # <- Check for comma here
    path('wine/<int:wine_id>/', views.wine_detail, name='wine_detail'),  # <- Check for comma here
    path('wine/<int:wine_id>/edit/', views.edit_wine, name='edit_wine'),  # <- Check for comma here
    path('wine/<int:wine_id>/add-analysis/', views.add_analysis, name='add_analysis'),  # <- Check for comma here
    path('wine/<int:wine_id>/delete/', views.delete_wine, name='delete_wine'),  # <- Check for comma here
    path('wine/<int:wine_id>/analysis/<int:analysis_id>/edit/', views.edit_analysis, name='edit_analysis'),  
    path('wine/<int:wine_id>/analysis/<int:analysis_id>/delete/', views.delete_analysis, name='delete_analysis'),  # <- Check for comma here
]
