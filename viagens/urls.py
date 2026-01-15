from django.urls import path

from viagens.views import (
    CreateClienteView, CreateReservaView, CreateRotaView, CreateSuiteView, DashboardView, EditClienteView, 
    EditReservaView, EditRotaView, EditSuiteView, ListClientesView, ListRotaView, ReservaView, SuiteView
)

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('rotas/create', CreateRotaView.as_view(), name='create_rota'),
    path('rotas/<int:rota_id>/edit', EditRotaView.as_view(), name='edit_rota'),
    path('rotas/list', ListRotaView.as_view(), name='list_rota'),
    path('clientes/create', CreateClienteView.as_view(), name='create_cliente'),  # Placeholder for Clientes view
    path('clientes/<int:cliente_id>/edit', EditClienteView.as_view(), name='edit_cliente'),  # Placeholder for Clientes view
    path('clientes/list', ListClientesView.as_view(), name='list_cliente'),  # Placeholder for Clientes view
    path('suites/create', CreateSuiteView.as_view(), name='create_suite'),  # Placeholder for Suites view
    path('suites/<int:suite_id>/edit', EditSuiteView.as_view(), name='edit_suite'),  # Placeholder for Suites view
    path('suites/list', SuiteView.as_view(), name='list_suite'),
    path('reservas/list',ReservaView.as_view(), name='list_reserva'),  # Placeholder for Reservas view
    path('reservas/create', CreateReservaView.as_view(), name='create_reserva'),  # Placeholder for Reservas view
    path('reservas/<int:reserva_id>/edit', EditReservaView.as_view(), name='edit_reserva'),  # Placeholder for Reservas view
]