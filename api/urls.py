from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('suites/', views.suites_disponiveis, name='suites_disponiveis'),
    path('suites/por-data/', views.suites_por_data, name='suites_por_data'),
    path('rotas/', views.rotas_disponiveis, name='rotas_disponiveis'),
    path('descontos/', views.descontos_idade, name='descontos_idade'),
    path('calcular-valor/', views.calcular_valor_reserva, name='calcular_valor_reserva'),
    path('buscar-customer/', views.buscar_customer, name='buscar_customer'),
    path('criar-customer/', views.criar_customer, name='criar_customer'),
    path('criar-reserva/', views.criar_reserva, name='criar_reserva'),
]