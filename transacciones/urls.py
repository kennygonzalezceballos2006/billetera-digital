from django.urls import path
from . import views

urlpatterns = [
    path('transferir/', views.transferir_view, name='transferir'),
    path('historial/', views.historial_view, name='historial'),
]