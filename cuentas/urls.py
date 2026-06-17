from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('bolsillos/', views.bolsillos_view, name='bolsillos'),
    path('cuentas/', views.cuentas_view, name='cuentas'),
    path('bolsillos/crear/', views.crear_bolsillo_view, name='crear_bolsillo'),
    path('bolsillos/eliminar/<int:bolsillo_id>/', views.eliminar_bolsillo_view, name='eliminar_bolsillo'),
]