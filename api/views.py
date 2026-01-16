from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import Client
from viagens.models import Suite, Reserva, Rota, ConfigViagem, Customer, PassageirosReserva
from api.Asaas import Asaas
from .serializers import (
    SuiteSerializer, ReservaSerializer, RotaSerializer, 
    RotaDisponibilidadeSerializer, ConfigViagemSerializer,
    CalcularValorReservaSerializer, CustomerSerializer, CriarReservaSerializer
)

from datetime import datetime, date,timedelta
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
# Create your views here.

@api_view(['GET'])
def suites_disponiveis(request):
    """
    Retorna todas as suites disponíveis (ativas)
    """
    
    try:
        suites = Suite.objects.filter(ativo=True, client=request.user.client)
        serializer = SuiteSerializer(suites, many=True)
        return Response({
            'status': 'sucesso',
            'data': serializer.data,
            'total': suites.count()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suites_por_data(request):
    """
    Retorna suites disponíveis para uma data específica
    Query params: data (YYYY-MM-DD)
    """
    try:
        data_str = request.query_params.get('data')
        
        if not data_str:
            return Response({
                'status': 'erro',
                'mensagem': 'Parâmetro "data" é obrigatório no formato YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Converter string para data
        data_viagem = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        # Buscar suites do cliente
        suites = Suite.objects.filter(
            ativo=True,
            client=request.user.client
        )
        
        # Suites que foram reservadas na data
        suites_reservadas = Reserva.objects.filter(
            data_reserva=data_viagem,
            status_reserva__in=['RESERVADA', 'CONFIRMADA', 'UTILIZADA']
        ).values_list('suite_id', flat=True)
        
        # Filtrar apenas suites não reservadas
        suites_disponiveis = suites.exclude(
            id__in=suites_reservadas
        )
        
        serializer = SuiteSerializer(suites_disponiveis, many=True)
        
        return Response({
            'status': 'sucesso',
            'data': data_str,
            'suites_disponiveis': serializer.data,
            'total': len(serializer.data)
        }, status=status.HTTP_200_OK)
        
    except ValueError:
        return Response({
            'status': 'erro',
            'mensagem': 'Data inválida. Use o formato YYYY-MM-DD'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rotas_disponiveis(request):
    """
    Retorna rotas disponíveis com cálculo de capacidade
    Query params: data (YYYY-MM-DD) - opcional
    """
    try:
        data_str = request.query_params.get('data')
        
        # Buscar rotas ativas do cliente
        rotas = Rota.objects.filter(
            ativo=True,
            client=request.user.client
        )
        
        rotas_com_disponibilidade = []
        
        for rota in rotas:
            # Se data foi fornecida, calcular passageiros reservados nessa data
            passageiros_reservados = 0
            
            if data_str:
                try:
                    data_viagem = datetime.strptime(data_str, '%Y-%m-%d').date()
                    
                    # Contar passageiros em reservas ativas para essa rota e data
                    reservas_ativas = Reserva.objects.filter(
                        rota=rota,
                        data_reserva=data_viagem,
                        status_reserva__in=['RESERVADA', 'CONFIRMADA', 'UTILIZADA']
                    )
                    
                    # Contar todos os passageiros dessas reservas
                    for reserva in reservas_ativas:
                        passageiros_reservados += reserva.passageiros.count()
                        
                except ValueError:
                    return Response({
                        'status': 'erro',
                        'mensagem': 'Data inválida. Use o formato YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            vagas_disponiveis = rota.capacidade_diaria - passageiros_reservados
            
            # Adicionar informações ao resultado
            rota_data = {
                'id': rota.id,
                'nome': rota.nome,
                'descricao': rota.descricao,
                'saindo_de': rota.saindo_de,
                'indo_para': rota.indo_para,
                'valor': rota.valor,
                'horario_partida': rota.horario_partida,
                'horario_chegada': rota.horario_chegada,
                'capacidade_diaria': rota.capacidade_diaria,
                'passageiros_reservados': passageiros_reservados,
                'vagas_disponiveis': vagas_disponiveis,
                
            }
            
            rotas_com_disponibilidade.append(rota_data)
        
        response_data = {
            'status': 'sucesso',
            'rotas': rotas_com_disponibilidade,
            'total': len(rotas_com_disponibilidade)
        }
        
        if data_str:
            response_data['data'] = data_str
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def descontos_idade(request):
    """
    GET: Retorna os descontos por idade configurados
    PUT: Atualiza os descontos por idade
    """
    try:
        # Buscar ou criar a configuração do cliente
        config, created = ConfigViagem.objects.get_or_create(
            client=request.user.client
        )
        
        if request.method == 'GET':
            serializer = ConfigViagemSerializer(config)
            return Response({
                'status': 'sucesso',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            serializer = ConfigViagemSerializer(config, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'sucesso',
                    'mensagem': 'Descontos atualizados com sucesso',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                'status': 'erro',
                'mensagem': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calcular_valor_reserva(request):
    """
    Calcula o valor previsto da reserva com base em passageiros e descontos
    """
    try:
        serializer = CalcularValorReservaSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'erro',
                'mensagem': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        rota_id = data.get('rota_id')
        suite_id = data.get('suite_id')
        passageiros = data.get('passageiros', [])
        
        # Validar rota
        try:
            rota = Rota.objects.get(id=rota_id, client=request.user.client)
        except Rota.DoesNotExist:
            return Response({
                'status': 'erro',
                'mensagem': 'Rota não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar suite se fornecida
        suite = None
        if suite_id:
            try:
                suite = Suite.objects.get(id=suite_id, client=request.user.client)
            except Suite.DoesNotExist:
                return Response({
                    'status': 'erro',
                    'mensagem': 'Suíte não encontrada'
                }, status=status.HTTP_404_NOT_FOUND)
        
        # Contar passageiros que usarão a suite
        passageiros_com_suite = 0
        for passageiro in passageiros:
            tem_suite = passageiro.get('suite', False)
            if not suite_id:
                tem_suite = False
            if tem_suite:
                passageiros_com_suite += 1
        
        # Validar limite de passageiros na suite
        if suite and passageiros_com_suite > suite.passageiros_inclusos:
            return Response({
                'status': 'erro',
                'mensagem': f'A suíte "{suite.nome}" permite apenas {suite.passageiros_inclusos} passageiro(s) incluso(s), mas você tentou adicionar {passageiros_com_suite}. Quantidade não permitida!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar configurações de desconto
        config = request.user.client.config_viagem
        
        valor_rota = Decimal(rota.valor)
        valor_suite = Decimal(suite.valor) if suite else Decimal('0.00')
        
        # Calcular valor total
        valor_total = Decimal('0.00')
        detalhes_passageiros = []
        
        for passageiro in passageiros:
            # Se suite não foi selecionada, força suite=false
            tem_suite = passageiro.get('suite', False)
            if not suite_id:
                tem_suite = False
            
            # Passageiro com suíte não paga passagem
            if tem_suite:
                detalhes_passageiros.append({
                    'nome': passageiro.get('nome', 'Passageiro com suíte'),
                    'valor_base': '0.00',
                    'desconto_aplicado': '0.00',
                    'valor_final': '0.00',
                    'motivo': 'Incluso na suíte'
                })
                continue
            
            desconto = Decimal('0')
            motivos_desconto = []
            
            # Desconto PCD
            if passageiro.get('pcd'):
                desconto += Decimal(config.desconto_pcd or 0)
                motivos_desconto.append(f'PCD ({config.desconto_pcd}%)')
            
            # Desconto por idade
            data_nascimento = passageiro.get('data_nascimento')
            if data_nascimento:
                nascimento = data_nascimento if isinstance(data_nascimento, date) else date.fromisoformat(str(data_nascimento))
                hoje = date.today()
                
                idade = hoje.year - nascimento.year - (
                    (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
                )
                
                if 0 <= idade <= 4:
                    desconto += Decimal(config.desconto_crianca_0_4 or 0)
                    motivos_desconto.append(f'Criança 0-4 anos ({config.desconto_crianca_0_4}%)')
                elif 5 <= idade <= 7:
                    desconto += Decimal(config.desconto_crianca_5_7 or 0)
                    motivos_desconto.append(f'Criança 5-7 anos ({config.desconto_crianca_5_7}%)')
                elif 8 <= idade <= 10:
                    desconto += Decimal(config.desconto_crianca_8_10 or 0)
                    motivos_desconto.append(f'Criança 8-10 anos ({config.desconto_crianca_8_10}%)')
                elif 11 <= idade <= 17:
                    desconto += Decimal(config.desconto_acima_11 or 0)
                    motivos_desconto.append(f'Adolescente 11-17 anos ({config.desconto_acima_11}%)')
            
            valor_com_desconto = valor_rota * (Decimal('1') - desconto / Decimal('100'))
            valor_total += valor_com_desconto
            
            detalhes_passageiros.append({
                'nome': passageiro.get('nome', 'Passageiro'),
                'valor_base': str(valor_rota),
                'desconto_aplicado': str(desconto) + '%',
                'valor_final': str(valor_com_desconto.quantize(Decimal('0.01'))),
                'motivos_desconto': motivos_desconto
            })
        
        # Adicionar valor da suíte
        valor_total += valor_suite
        
        return Response({
            'status': 'sucesso',
            'data': {
                'valor_total': str(valor_total.quantize(Decimal('0.01'))),
                'valor_rota': str(valor_rota),
                'valor_suite': str(valor_suite),
                'suite_selecionada': suite is not None,
                'passageiros_com_suite': passageiros_com_suite,
                'limite_suite': suite.passageiros_inclusos if suite else 0,
                'quantidade_passageiros': len(passageiros),
                'detalhes_passageiros': detalhes_passageiros
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_customer(request):
    """
    Busca customer por telefone ou CPF
    Query params: telefone ou cpf
    """
    try:
        telefone = request.query_params.get('telefone')
        cpf_cnpj = request.query_params.get('cpf')
        
        # Validar que pelo menos um parâmetro foi fornecido
        if not telefone and not cpf_cnpj:
            return Response({
                'status': 'erro',
                'mensagem': 'Forneça pelo menos um parâmetro: "telefone" ou "cpf"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Construir query
        customer = None
        
        if telefone:
            customer = Customer.objects.filter(
                client=request.user.client,
                telefone=telefone
            ).first()
        elif cpf_cnpj:
            customer = Customer.objects.filter(
                client=request.user.client,
                cpf_cnpj=cpf_cnpj
            ).first()
        
        if not customer:
            return Response({
                'status': 'erro',
                'mensagem': f'Cliente não encontrado com os parâmetros fornecidos'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer)
        return Response({
            'status': 'sucesso',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_customer(request):
    """
    Cria um novo customer com ID Asaas automaticamente
    """
    try:
        data = request.data.copy()
        data['client'] = request.user.client.id
        
        serializer = CustomerSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'erro',
                'mensagem': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se CPF/CNPJ já existe
        cpf_cnpj = data.get('cpf_cnpj')
        if cpf_cnpj:
            customer_existente = Customer.objects.filter(
                client=request.user.client,
                cpf_cnpj=cpf_cnpj
            ).exists()
            
            if customer_existente:
                return Response({
                    'status': 'erro',
                    'mensagem': f'Já existe um cliente com o CPF/CNPJ: {cpf_cnpj}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Criar customer no banco de dados
        customer = serializer.save(client=request.user.client)
        
        # Criar customer no Asaas
        try:
            asaas = Asaas(request.user.client)
            asaas_response = asaas.create_customer(
                nome=customer.nome,
                email=customer.email,
                telefone=customer.telefone,
                cpf_cnpj=customer.cpf_cnpj
            )
            
            # Salvar ID do Asaas
            customer.asaas_id = asaas_response.get('id')
            customer.save()
            
        except Exception as e:
            # Se falhar no Asaas, deletar customer criado e retornar erro
            customer.delete()
            return Response({
                'status': 'erro',
                'mensagem': f'Erro ao criar cliente no Asaas: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'sucesso',
            'mensagem': 'Cliente criado com sucesso',
            'data': CustomerSerializer(customer).data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_reserva(request):
    """
    Cria uma nova reserva com cálculo automático de valor e integração com Asaas
    """
    try:
        serializer = CriarReservaSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'erro',
                'mensagem': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        customer_id = data.get('customer_id')
        rota_id = data.get('rota_id')
        suite_id = data.get('suite_id')
        passageiros_data = data.get('passageiros', [])
        
        # ===== Validações básicas =====
        try:
            customer = Customer.objects.get(id=customer_id, client=request.user.client)
        except Customer.DoesNotExist:
            return Response({
                'status': 'erro',
                'mensagem': 'Cliente não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            rota = Rota.objects.get(id=rota_id, client=request.user.client)
        except Rota.DoesNotExist:
            return Response({
                'status': 'erro',
                'mensagem': 'Rota não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar suite se fornecida
        suite = None
        if suite_id:
            try:
                suite = Suite.objects.get(id=suite_id, client=request.user.client)
            except Suite.DoesNotExist:
                return Response({
                    'status': 'erro',
                    'mensagem': 'Suíte não encontrada'
                }, status=status.HTTP_404_NOT_FOUND)
        
        # Contar passageiros que usarão a suite
        passageiros_com_suite = 0
        for passageiro in passageiros_data:
            tem_suite = passageiro.get('suite', False)
            if not suite_id:
                tem_suite = False
            if tem_suite:
                passageiros_com_suite += 1
        
        # Validar limite de passageiros na suite
        if suite and passageiros_com_suite > suite.passageiros_inclusos:
            return Response({
                'status': 'erro',
                'mensagem': f'A suíte "{suite.nome}" permite apenas {suite.passageiros_inclusos} passageiro(s) incluso(s), mas você tentou adicionar {passageiros_com_suite}. Quantidade não permitida!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar configurações de desconto
        config = request.user.client.config_viagem
        
        valor_rota = Decimal(rota.valor)
        valor_suite = Decimal(suite.valor) if suite else Decimal('0.00')
        
        # ===== CÁLCULO DO VALOR TOTAL =====
        valor_total = Decimal('0.00')
        
        for passageiro in passageiros_data:
            # Se suite não foi selecionada, força suite=false
            tem_suite = passageiro.get('suite', False)
            if not suite_id:
                tem_suite = False
            
            # Passageiro com suíte não paga passagem
            if tem_suite:
                continue
            
            desconto = Decimal('0')
            
            # Desconto PCD
            if passageiro.get('pcd'):
                desconto += Decimal(config.desconto_pcd or 0)
            
            # Desconto por idade
            data_nascimento = passageiro.get('data_nascimento')
            if data_nascimento:
                nascimento = data_nascimento if isinstance(data_nascimento, date) else date.fromisoformat(str(data_nascimento))
                hoje = date.today()
                
                idade = hoje.year - nascimento.year - (
                    (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
                )
                
                if 0 <= idade <= 4:
                    desconto += Decimal(config.desconto_crianca_0_4 or 0)
                elif 5 <= idade <= 7:
                    desconto += Decimal(config.desconto_crianca_5_7 or 0)
                elif 8 <= idade <= 10:
                    desconto += Decimal(config.desconto_crianca_8_10 or 0)
                elif 11 <= idade <= 17:
                    desconto += Decimal(config.desconto_acima_11 or 0)
            
            valor_com_desconto = valor_rota * (Decimal('1') - desconto / Decimal('100'))
            valor_total += valor_com_desconto
        
        # Adicionar valor da suíte
        valor_total += valor_suite
        
        # ===== Criar cobrança no Asaas =====
        try:
            asaas = Asaas(request.user.client)
            cobranca_asaas = asaas.criar_cobranca_pix(
                customer_id=customer.asaas_id,
                valor=float(valor_total.quantize(Decimal('0.01'))),
                descricao=f"Reserva Rota: {rota.nome} - Cliente: {customer.nome}",
                vencimento=(datetime.now().date() + timedelta(days=3)).isoformat()
            )
            
            # Obter QR Code PIX
            pix_transaction = asaas.pixQrCode(cobranca_asaas.get('id', ''))
            
            qr_code_pix = pix_transaction.get('encodedImage', '') if pix_transaction else ''
            code_pix = pix_transaction.get('payload', '') if pix_transaction else ''
            link_cobranca = cobranca_asaas.get('invoiceUrl', '')
            
        except Exception as e:
            return Response({
                'status': 'erro',
                'mensagem': f'Erro ao criar cobrança no Asaas: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ===== Criar Reserva =====
        try:
            reserva = Reserva.objects.create(
                customer=customer,
                rota=rota,
                suite=suite,
                valor_total=valor_total.quantize(Decimal('0.01')),
                data_reserva=date.today(),
                status_reserva='RESERVADA',
                pago=False,
                qr_code_pix=qr_code_pix,
                code_pix=code_pix,
                cobranca_asaas_id=cobranca_asaas.get('id', ''),
                cobranca_asaas_link=link_cobranca,
            )
            
            # ===== Criar Passageiros =====
            for passageiro_data in passageiros_data:
                # Validar campos obrigatórios do passageiro
                nome = passageiro_data.get('nome')
                documento = passageiro_data.get('documento')
                
                if not nome:
                    return Response({
                        'status': 'erro',
                        'mensagem': 'O nome do passageiro é obrigatório'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not documento:
                    return Response({
                        'status': 'erro',
                        'mensagem': 'O documento do passageiro é obrigatório'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                passageiro = PassageirosReserva.objects.create(
                    nome=nome,
                    documento=documento,
                    data_nascimento=passageiro_data.get('data_nascimento') or None,
                    pcd=passageiro_data.get('pcd', False),
                    suite=suite if passageiro_data.get('suite') and suite else None,
                )
                reserva.passageiros.add(passageiro)
            
            return Response({
                'status': 'sucesso',
                'mensagem': 'Reserva criada com sucesso',
                'data': {
                    'id': reserva.id,
                    'customer_id': customer.id,
                    'rota_id': rota.id,
                    'suite_id': suite.id if suite else None,
                    'valor_total': str(reserva.valor_total),
                    'qr_code_pix': qr_code_pix,
                    'code_pix': code_pix,
                    'link_cobranca': link_cobranca,
                    'cobranca_asaas_id': cobranca_asaas.get('id', ''),
                    'quantidade_passageiros': len(passageiros_data)
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'erro',
                'mensagem': f'Erro ao criar reserva: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def webhook_asaas(request, client_id):
    """
    Webhook para receber notificações do Asaas sobre status de pagamento
    
    Eventos possíveis:
    - PAYMENT_CREATED: Pagamento criado
    - PAYMENT_UPDATED: Pagamento atualizado
    - PAYMENT_CONFIRMED: Pagamento confirmado
    - PAYMENT_RECEIVED: Pagamento recebido
    - PAYMENT_OVERDUE: Pagamento vencido
    - PAYMENT_DELETED: Pagamento deletado
    - PAYMENT_RESTORED: Pagamento restaurado
    - PAYMENT_REFUNDED: Pagamento reembolsado
    - PAYMENT_RECEIVED_IN_CASH: Pagamento recebido em dinheiro
    - PAYMENT_CHARGEBACK_REQUESTED: Chargeback solicitado
    - PAYMENT_CHARGEBACK_DISPUTE: Disputa de chargeback
    - PAYMENT_AWAITING_CHARGEBACK_REVERSAL: Aguardando reversão de chargeback
    """
    client = Client.objects.get(id=client_id)  # Apenas para validar se o client existe
    
    try:
        # Captura o payload do webhook
        webhook_data = json.loads(request.body.decode('utf-8'))
        
        # Pega o evento e os dados do pagamento
        event = webhook_data.get('event')
        payment = webhook_data.get('payment', {})
        
        # ID da cobrança no Asaas
        cobranca_id = payment.get('id')
        
        if not cobranca_id:
            return Response({
                'status': 'erro',
                'mensagem': 'ID da cobrança não encontrado no webhook'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Busca a reserva pelo ID da cobrança
        try:
            reserva = Reserva.objects.get(cobranca_asaas_id=cobranca_id,customer__client=client)
        except Reserva.DoesNotExist:
            return Response({
                'status': 'erro',
                'mensagem': f'Reserva com cobrança {cobranca_id} não encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Atualiza o status da reserva baseado no evento
        if event == 'PAYMENT_CONFIRMED' or event == 'PAYMENT_RECEIVED':
            reserva.pago = True
            reserva.status_reserva = 'CONFIRMADA'
            
        elif event == 'PAYMENT_REFUNDED':
            reserva.status_reserva = 'REEMBOLSADA'
            reserva.pago = False
            
        elif event == 'PAYMENT_OVERDUE':
            reserva.status_reserva = 'CANCELADA'
            reserva.pago = False
            
        elif event == 'PAYMENT_DELETED':
            reserva.status_reserva = 'CANCELADA'
            reserva.pago = False
        
        # Salva as alterações
        reserva.save()
        
        return Response({
            'status': 'sucesso',
            'mensagem': f'Webhook processado com sucesso. Evento: {event}',
            'data': {
                'reserva_id': reserva.id,
                'status_reserva': reserva.status_reserva,
                'pago': reserva.pago,
                'evento': event
            }
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({
            'status': 'erro',
            'mensagem': 'Erro ao decodificar JSON do webhook'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'erro',
            'mensagem': f'Erro ao processar webhook: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
