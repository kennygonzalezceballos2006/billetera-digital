from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transferir/', views.transferir_view, name='transferir'),
    path('procesar/', views.procesar_transferencia_view, name='procesar_transferencia'),
    
]