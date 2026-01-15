
from django import forms
from .models import Customer, Rota, Suite

class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ['nome', 'descricao', 'saindo_de', 'indo_para', 'ativo', 'capacidade_diaria', 'horario_partida', 'valor', 'client']
        

class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['nome', 'email', 'telefone', 'cpf_cnpj', 'client']
        
        
class SuiteForm(forms.ModelForm):
    class Meta:
        model = Suite
        fields = ['nome', 'ativo', 'valor', 'passageiros_inclusos', 'client']
        