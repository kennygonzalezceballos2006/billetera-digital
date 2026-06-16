from django.urls import path
from . import views

urlpatterns = [
    path('', views.notificaciones_view, name='notificaciones'),
    path('<int:notificacion_id>/leida/', views.marcar_leida_view, name='marcar_leida'),
]