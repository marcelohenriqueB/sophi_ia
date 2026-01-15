from django.db import models
from users.models import Client
# Create your models here.



class ConfigViagem(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='config_viagem')
    desconto_pcd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    desconto_idoso = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Descontos para crianças por faixa etária porcentagem
    desconto_crianca_0_4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    desconto_crianca_5_7 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    desconto_crianca_8_10 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    desconto_acima_11 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    desconto_idoso = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    desconto_pcd = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    token_asaas = models.CharField(max_length=255, null=True, blank=True)              
    criado_em = models.DateTimeField(auto_now_add=True)

    class InertiaMeta:
        fields = ('id','client','desconto_pcd','desconto_idoso','desconto_crianca_0_4','desconto_crianca_5_7','desconto_crianca_8_10','desconto_acima_11', 'criado_em' )
        
    def __str__(self):
        return f"Configuração de Viagem - {self.client.name}"
    
    
class Suite(models.Model):
    nome = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='suites', null=True, blank=True)
    passageiros_inclusos = models.PositiveIntegerField(default=0)
    
    class InertiaMeta:
        fields = ('nome','id', 'criado_em', 'ativo','passageiros_inclusos','valor' )
        
    def __str__(self):
        return self.nome


class Rota(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    saindo_de = models.CharField(max_length=255)
    indo_para = models.CharField(max_length=255)
    ativo = models.BooleanField(default=True)
    # suites = models.ManyToManyField(Suite, related_name='rotas', blank=True,)
    usuario = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='rotas', null=True, default=None)
    capacidade_diaria = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    horario_partida = models.TimeField(null=True, blank=True)
    horario_chegada = models.TimeField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='rotas', null=True, blank=True)

    class InertiaMeta:
        fields = (
            'id','nome', 'descricao', 'criado_em', 'saindo_de', 'indo_para', 'ativo',
            'capacidade_diaria', 'valor', 'horario_partida',
        )
    def __str__(self):
        return self.nome


class Customer(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=20, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clientes',)
    asaas_id = models.CharField(max_length=255, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cpf_cnpj', 'client')
        
    class InertiaMeta:
        fields = ( 'id','nome', 'email', 'telefone', 'cpf_cnpj', 'criado_em', 'asaas_id' )
        
    def __str__(self):
        return self.nome
    

class Reserva(models.Model):
    STATUS_CHOICES = (
        ('RESERVADA', 'Reservada'),
        ('CONFIRMADA', 'Confirmada'),
        ('UTILIZADA', 'Utilizada'),
        ('CANCELADA', 'Cancelada'),
        ('REEMBOLSADA', 'Reembolsada'),
    )
    
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, related_name='reservas', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservas')
    passageiros = models.ManyToManyField('PassageirosReserva', related_name='reservas', blank=True)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='reservas', null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pago = models.BooleanField(default=False)
    status_reserva = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RESERVADA')
    cobranca_asaas_id = models.CharField(max_length=255, null=True, blank=True)
    cobranca_asaas_link = models.URLField(null=True, blank=True)
    data_reserva = models.DateField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    qr_code_pix = models.TextField(null=True, blank=True)
    code_pix = models.CharField(max_length=255, null=True, blank=True)
    
    class InertiaMeta:
        fields = (
            'id','rota', 'customer', 'suite', 'valor_total', 'pago', 'status_reserva', 'cobranca_asaas_id',
            'cobranca_asaas_link', 'data_reserva', 'criado_em', 'qr_code_pix', 'code_pix'
        )
        
    def __str__(self):
        return f"Reserva {self.id} - {self.customer.nome} - {self.rota.nome}"
    

class PassageirosReserva(models.Model):
    nome = models.CharField(max_length=255)
    documento = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True, blank=True)
    pcd = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, related_name='passageiros', null=True, blank=True)
    class InertiaMeta:
        fields = ('id','nome', 'documento', 'data_nascimento', 'pcd', 'criado_em', 'suite' )
        
    def __str__(self):
        return self.nome
    