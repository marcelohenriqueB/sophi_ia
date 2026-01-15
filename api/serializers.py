from rest_framework import serializers
from viagens.models import Suite, Reserva, Rota, Customer, PassageirosReserva, ConfigViagem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'nome', 'email', 'telefone', 'cpf_cnpj', 'criado_em', 'asaas_id']
        read_only_fields = ['id', 'criado_em']


class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = ['id', 'nome', 'valor', 'passageiros_inclusos', 'ativo', 'criado_em']
        read_only_fields = ['id', 'criado_em']


class RotaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rota
        fields = [
            'id', 'nome', 'descricao', 'saindo_de', 'indo_para', 
            'ativo', 'capacidade_diaria', 'valor', 'horario_partida',
            'horario_chegada', 'criado_em',
        ]
        read_only_fields = ['id', 'criado_em']


class RotaDisponibilidadeSerializer(serializers.Serializer):
    """Serializer para mostrar rotas com disponibilidade de passageiros"""
    id = serializers.IntegerField()
    nome = serializers.CharField()
    descricao = serializers.CharField()
    saindo_de = serializers.CharField()
    indo_para = serializers.CharField()
    valor = serializers.DecimalField(max_digits=10, decimal_places=2)
    horario_partida = serializers.TimeField()
    horario_chegada = serializers.TimeField()
    capacidade_diaria = serializers.IntegerField()
    passageiros_reservados = serializers.IntegerField()
    vagas_disponiveis = serializers.IntegerField()


class PassageirosReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassageirosReserva
        fields = ['id', 'nome', 'documento', 'data_nascimento', 'pcd', 'suite']
        read_only_fields = ['id']


class ReservaSerializer(serializers.ModelSerializer):
    suite_info = SuiteSerializer(source='suite', read_only=True)
    passageiros_info = PassageirosReservaSerializer(source='passageiros', many=True, read_only=True)
    
    class Meta:
        model = Reserva
        fields = [
            'id', 'rota', 'customer', 'suite', 'suite_info', 'valor_total', 
            'pago', 'status_reserva', 'data_reserva', 'criado_em', 
            'passageiros', 'passageiros_info', 'cobranca_asaas_id', 
            'cobranca_asaas_link', 'qr_code_pix', 'code_pix'
        ]
        read_only_fields = ['id', 'data_reserva', 'criado_em']


class ReservaListSerializer(serializers.ModelSerializer):
    suite_info = SuiteSerializer(source='suite', read_only=True)
    
    class Meta:
        model = Reserva
        fields = [
            'id', 'rota', 'customer', 'suite', 'suite_info', 'valor_total', 
            'pago', 'status_reserva', 'data_reserva', 'criado_em'
        ]
        read_only_fields = ['id', 'data_reserva', 'criado_em']


class ConfigViagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigViagem
        fields = [
            'desconto_pcd', 'desconto_idoso', 
            'desconto_crianca_0_4', 'desconto_crianca_5_7', 
            'desconto_crianca_8_10', 'desconto_acima_11',
        ]
        read_only_fields = ['id', 'criado_em']


class PassageiroCalculoSerializer(serializers.Serializer):
    """Serializer para passageiros no cálculo de valor"""
    nome = serializers.CharField(required=False)
    documento = serializers.CharField(required=False)
    data_nascimento = serializers.DateField(required=False, allow_null=True)
    pcd = serializers.BooleanField(default=False)
    suite = serializers.BooleanField(default=False)


class CalcularValorReservaSerializer(serializers.Serializer):
    """Serializer para calcular valor da reserva"""
    rota_id = serializers.IntegerField()
    suite_id = serializers.IntegerField(required=False, allow_null=True)
    passageiros = PassageiroCalculoSerializer(many=True)


class CriarReservaSerializer(serializers.Serializer):
    """Serializer para criar reserva"""
    customer_id = serializers.IntegerField()
    rota_id = serializers.IntegerField()
    suite_id = serializers.IntegerField(required=False, allow_null=True)
    passageiros = PassageiroCalculoSerializer(many=True)
