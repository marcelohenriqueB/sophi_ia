from django.contrib import admin

# Register your models here.

from .models import Reserva, Rota, Suite, ConfigViagem,Customer
@admin.register(Rota)
class RotaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'saindo_de', 'indo_para', 'ativo', 'capacidade_diaria', 'horario_partida', 'valor')
    search_fields = ('nome', 'descricao', 'saindo_de', 'indo_para')
    list_filter = ('ativo',)
    
@admin.register(Suite)
class SuiteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo', 'valor', 'passageiros_inclusos', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('ativo',)
@admin.register(ConfigViagem)
class ConfigViagemAdmin(admin.ModelAdmin):
    list_display = ('client', 'desconto_idoso', 'desconto_crianca_5_7', 'desconto_crianca_8_10', 'desconto_pcd', 'criado_em')
    search_fields = ('client__name',)
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cpf_cnpj', 'client', 'asaas_id', 'criado_em')
    search_fields = ('nome', 'email', 'telefone', 'cpf_cnpj', 'client__name', 'asaas_id')
    list_filter = ('criado_em',)
    
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'rota', 'customer', 'suite', 'valor_total', 'pago', 'data_reserva', 'criado_em')
    search_fields = ('customer__nome', 'rota__nome', 'suite__nome', 'cobranca_asaas_id')
    list_filter = ('pago', 'data_reserva', 'criado_em')
