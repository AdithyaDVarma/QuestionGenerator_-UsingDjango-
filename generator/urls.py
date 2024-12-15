from django.urls import path
from . import views

urlpatterns = [
    # ... other patterns ...
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.history_view, name='history'),
    path('results/<int:history_id>/', views.results_view, name='results'),
    path('profile/', views.profile_view, name='profile'),
]