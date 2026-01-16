from django.shortcuts import render
from inertia import render
from django.views import View
from django.shortcuts import redirect
from django.db import models

from api.Asaas import Asaas
from viagens.forms import CustomersForm, RotaForm, SuiteForm
from viagens.models import Customer, Reserva, Rota, Suite, ConfigViagem
from users.models import JwtTokenAdmin
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
import time
from viagens.models import PassageirosReserva
import json

from datetime import date, datetime, timedelta
from decimal import Decimal
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# # Create your views here.
# def create_rota(request):
#     return render(request, 'Rotas/Create')

class CreateRotaView(View):
    def get(self, request):
        return render(request, 'Rotas/Create')
    
    def post(self, request):
    
        request_data = request.POST.copy()
        user = request.user
        request_data['client'] = user.client
        
        # print("Request Data:", request_data)
        form = RotaForm(request_data)
        if form.is_valid():
            rota = form.save(commit=False)
            rota.usuario = request.user
            rota.save()
            
            return redirect(f'/viagens/rotas/{rota.id}/edit')  # Redirect to the list of rotas or any other page
        
        return redirect('/viagens/rotas/create')


class EditRotaView(View):
    def get(self, request, rota_id):
        rota = Rota.objects.get(id=rota_id)
        
        return render(request, 'Rotas/Edit', {'rota': lambda: rota})
    
    def post(self, request, rota_id):
        rota = Rota.objects.get(id=rota_id)
        request_data = request.POST.copy()
        user = request.user
        request_data['client'] = user.client
        
        form = RotaForm(request_data, instance=rota)
        if form.is_valid():
            rota = form.save(commit=False)
            rota.usuario = request.user
            rota.save()
            
            return render(request, 'Rotas/Edit', {'rota': lambda: rota})
        
        else:
            return render(request, 'Rotas/Edit', {
                "errors": form.errors,
                "rota": lambda: rota
            })
    
    def delete(self, request, rota_id):
        rota = Rota.objects.get(id=rota_id, client=request.user.client)
        rota.delete()
        return redirect('/viagens/rotas/list')
    
    
class ListRotaView(View):
    def get(self, request):
        rotas = Rota.objects.filter(client=request.user.client)
        page_obj = Paginator(rotas, 10).get_page(request.GET.get('page', 1))
        
        return render(request, 'Rotas/Index', {
            'rotas': list(page_obj),  # transforma QuerySet em lista
            'pagination': {
                'current_page': page_obj.number,
                'num_pages': page_obj.paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })

class ListClientesView(View):
    def get(self, request):
        clientes = Customer.objects.filter(client=request.user.client)
        page_obj = Paginator(clientes, 10).get_page(request.GET.get('page', 1))
        
        return render(request, 'Customers/Index', {
            'clientes': list(page_obj),  # transforma QuerySet em lista
            'pagination': {
                'current_page': page_obj.number,
                'num_pages': page_obj.paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })

class CreateClienteView(View):
    def get(self, request):
        
        return render(request, 'Customers/Create')
    
    def post(self, request):
        request_data = request.POST.copy()
        user = request.user
        request_data['client'] = user.client.id  # Atribui o client do usuário logado
        
        
        form = CustomersForm(request_data)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.client = user.client  # Atribui o client do usuário logado
            asaas =  Asaas(user.client)
            asaas_api = asaas.create_customer(cliente.nome, cliente.email, cliente.telefone, cliente.cpf_cnpj)
            cliente.asaas_id = asaas_api.get('id')
            
            cliente.save()
            
            
            return redirect(f'/viagens/clientes/{cliente.id}/edit')  # Redireciona para a página de edição do cliente
        
        return render(
            request, 'Customers/Create',
            {
                "errors": form.errors,
            }    
        )  # Redireciona para a página de edição do cliente
        
class EditClienteView(View):
    def get(self, request, cliente_id):
        cliente = Customer.objects.get(id=cliente_id)
        
        return render(request, 'Customers/Edit', {'cliente': lambda: cliente})
    
    def post(self, request, cliente_id):
        cliente = Customer.objects.get(id=cliente_id, client=request.user.client)
        request_data = request.POST.copy()
        user = request.user
        request_data['client'] = user.client.id
        
        form = CustomersForm(request_data, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.client = user.client
            cliente.save()
            
            return render(request, 'Customers/Edit', {'cliente': lambda: cliente})
        
        else:
            print("Form Errors:", form.errors)
            return render(request, 'Customers/Edit', {
                "errors": form.errors,
                "cliente": lambda: cliente
            })  
    def delete(self, request, cliente_id):
        cliente = Customer.objects.get(id=cliente_id, client=request.user.client)
        cliente.delete()
        return redirect('/viagens/clientes/list')
    

class SuiteView(View):
    def get(self, request):
        page_obj = Paginator(Suite.objects.filter(client=request.user.client), 10).get_page(request.GET.get('page', 1))
        return render(request, 'Suites/Index', {
            'suites': list(page_obj),  # transforma QuerySet em lista
            'pagination': {
                'current_page': page_obj.number,
                'num_pages': page_obj.paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })

class CreateSuiteView(View):
    def get(self, request):
        return render(request, 'Suites/Create')
    
    def post(self, request):
        
        request_data = request.POST.copy()
        user = request.user
        request_data['client'] = user.client.id  # Atribui o client do usuário logado
        
        
        form = SuiteForm(request_data)
        if form.is_valid():
            suite = form.save(commit=False)
            suite.client = user.client  # Atribui o client do usuário logado
            suite.save()
            
            return redirect(f'/viagens/suites/{suite.id}/edit')  # Redireciona para a página de edição do suite
        
        return render(
            request, 'Suites/Create',
            {
                "errors": form.errors,
            }    
        )  # Redireciona para a página de edição do suite
    
class EditSuiteView(View):
    def get(self, request, suite_id):
        suite = Suite.objects.get(id=suite_id)
        return render(request, 'Suites/Edit', {'suite': lambda: suite})
    
    def post(self, request, suite_id):
        suite = Suite.objects.get(id=suite_id, client=request.user.client)
        request_data = request.POST.copy()
        user = request.user
        request_data['client'] = user.client.id
        
        form = SuiteForm(request_data, instance=suite)
        if form.is_valid():
            suite = form.save(commit=False)
            suite.client = user.client
            suite.save()
            
            return render(request, 'Suites/Edit', {'suite': lambda: suite})
        
        else:
            return render(request, 'Suites/Edit', {
                "errors": form.errors,
                "suite": lambda: suite
            })
    def delete(self, request, suite_id):
        suite = Suite.objects.get(id=suite_id, client=request.user.client)
        suite.delete()
        return redirect('/viagens/suites/list')
    
class ReservaView(View):
    def get(self, request):
        # Inicia a queryset base
        reservas = Reserva.objects.filter(customer__client=request.user.client).select_related(
            'customer', 'rota', 'suite'
        )

        # Aplicar filtros
        cliente_filtro = request.GET.get('cliente', '').strip()
        rota_filtro = request.GET.get('rota', '').strip()
        pago_filtro = request.GET.get('pago', '').strip()
        data_filtro = request.GET.get('data', '').strip()
        suite_filtro = request.GET.get('suite', '').strip()
        status_filtro = request.GET.get('status', '').strip()

        if cliente_filtro:
            reservas = reservas.filter(customer__nome__icontains=cliente_filtro)

        if rota_filtro:
            reservas = reservas.filter(rota_id=rota_filtro)

        if suite_filtro:
            reservas = reservas.filter(suite_id=suite_filtro)

        if pago_filtro:
            if pago_filtro.lower() == 'true':
                reservas = reservas.filter(pago=True)
            elif pago_filtro.lower() == 'false':
                reservas = reservas.filter(pago=False)

        if status_filtro:
            reservas = reservas.filter(status_reserva=status_filtro)

        if data_filtro:
            try:
                data_obj = datetime.strptime(data_filtro, '%Y-%m-%d').date()
                reservas = reservas.filter(data_reserva=data_obj)
            except ValueError:
                pass

        # Ordenar
        reservas = reservas.order_by('-data_reserva')

        # Datas distintas para o calendário (após filtros e antes da paginação)
        datas_reservas = list(reservas.values_list('data_reserva', flat=True).distinct())

        # Paginação
        paginator = Paginator(reservas, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        rotas = Rota.objects.filter(client=request.user.client, ativo=True)
        suites = Suite.objects.filter(client=request.user.client, ativo=True)

        return render(request, 'Reservas/Index', {
            'reservas': list(page_obj),
            'rotas': list(rotas),
            'suites': list(suites),
            'pagination': {
                'current_page': page_obj.number,
                'num_pages': paginator.num_pages,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
                'total': paginator.count,
            },
            'filters': {
                'cliente': cliente_filtro,
                'rota': rota_filtro,
                'pago': pago_filtro,
                'data': data_filtro,
                'suite': suite_filtro,
                'status': status_filtro,
            },
            'reserved_dates': [d.isoformat() for d in datas_reservas if d],
        })

class PublicReservaView(View):
    def get(self, request, token):
        try:
            reserva = Reserva.objects.select_related('customer', 'rota', 'suite').prefetch_related('passageiros__suite').get(embarque_uuid=token)
        except Reserva.DoesNotExist:
            from django.shortcuts import render as django_render
            return django_render(request, 'public_reserva.html', {
                'error': True,
                'message': 'Reserva não encontrada'
            }, status=404)

        passageiros = reserva.passageiros.all()
        qr_link = request.build_absolute_uri(f'/viagens/reservas/{reserva.embarque_uuid}/embarque')
        
        from django.shortcuts import render as django_render
        from django.utils import timezone
        
        return django_render(request, 'public_reserva.html', {
            'reserva': reserva,
            'passageiros': passageiros,
            'qr_link': qr_link,
            'now': timezone.now(),
        })

@method_decorator(login_required, name='dispatch')
class EmbarqueReservaView(View):
    def get(self, request, token):
        try:
            reserva = Reserva.objects.select_related('customer', 'rota', 'suite').prefetch_related('passageiros__suite').get(embarque_uuid=token)
        except Reserva.DoesNotExist:
            from django.shortcuts import render as django_render
            return django_render(request, 'public_reserva.html', {
                'error': True,
                'message': 'Reserva não encontrada'
            }, status=404)

        passageiros = reserva.passageiros.all()
        qr_link = request.build_absolute_uri()
        
        from django.shortcuts import render as django_render
        from django.utils import timezone
        
        return django_render(request, 'validar_embarques.html', {
            'reserva': reserva,
            'passageiros': passageiros,
            'qr_link': qr_link,
            'now': timezone.now(),
        })

    def post(self, request, token):
        try:
            reserva = Reserva.objects.get(embarque_uuid=token)
            reserva.data_embarque = datetime.now()
            reserva.status_reserva = 'EMBARCADO'
            reserva.save()
            
            return JsonResponse({'success': True, 'message': 'Embarque confirmado com sucesso.'})
        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reserva não encontrada.'}, status=404)

@method_decorator(login_required, name='dispatch')
class AlterarStatusReservaView(View):
    """View para alterar o status de uma reserva"""
    def post(self, request, token):
        try:
            import json
            body = json.loads(request.body)
            novo_status = body.get('status')
            
            if not novo_status:
                return JsonResponse({'success': False, 'message': 'Status não informado'}, status=400)
            
            reserva = Reserva.objects.get(embarque_uuid=token)
            
            # Validar status
            status_validos = ['AGUARDANDO_PAGAMENTO', 'PAGAMENTO_CONFIRMADO', 'AGUARDANDO_EMBARQUE', 'EMBARCADO', 'CANCELADA', 'REEMBOLSADA']
            if novo_status not in status_validos:
                return JsonResponse({'success': False, 'message': 'Status inválido'}, status=400)
            
            # Atualizar status
            status_anterior = reserva.get_status_reserva_display()
            reserva.status_reserva = novo_status
            
            # Se alterar para EMBARCADO, registrar data
            if novo_status == 'EMBARCADO' and not reserva.data_embarque:
                from django.utils import timezone
                reserva.data_embarque = timezone.now()
            
            reserva.save()
            
            return JsonResponse({
                'success': True, 
                'message': f'Status alterado de "{status_anterior}" para "{reserva.get_status_reserva_display()}"',
                'novo_status': novo_status
            })
        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reserva não encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


class CreateReservaView(View):
    def get(self, request):
        clientes = Customer.objects.filter(client=request.user.client)
        rotas = Rota.objects.filter(client=request.user.client, ativo=True)
        suites = Suite.objects.filter(client=request.user.client, ativo=True)
        config_viagem = request.user.client.config_viagem

        return render(request, 'Reservas/Create', {
            'clientes': list(clientes),
            'rotas': list(rotas),
            'suites': list(suites),
            'config_viagem': lambda: config_viagem,
        })
    def post(self, request):
        try:
            data = request.json
            customer_id = data.get('customer_id')
            rota_id = data.get('rota_id')
            suite_id = data.get('suite_id',0)
            data_reserva = data.get('data_reserva')
            status_reserva = data.get('status_reserva', 'RESERVADA')
            passageiros = data.get('passageiros', [])
            
            print("suite_id:", suite_id)

            # ===== Validações básicas =====
            customer = Customer.objects.get(id=customer_id, client=request.user.client)
            rota = Rota.objects.get(id=rota_id, client=request.user.client)
            suite = None
            if suite_id:
                suite = Suite.objects.filter(
                    id=suite_id,
                    client=request.user.client
                ).first()
            config = request.user.client.config_viagem

            valor_rota = Decimal(rota.valor)
            
            valor_suite = Decimal(suite.valor) if suite else Decimal('0.00')

            # ===== CÁLCULO DO VALOR TOTAL =====
            valor_total = Decimal('0.00')

            for passageiro in passageiros:

                # Passageiro com suíte não paga passagem
                if passageiro.get('suite'):
                    continue

                desconto = Decimal('0')

                # Desconto PCD
                if passageiro.get('pcd'):
                    desconto += Decimal(config.desconto_pcd or 0)

                # Desconto por idade
                data_nascimento = passageiro.get('data_nascimento')
                if data_nascimento:
                    nascimento = date.fromisoformat(data_nascimento)
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

            # Soma valor da suíte (uma única vez)
            valor_total += valor_suite

            Asaas_instance = Asaas(request.user.client)
            print("Criando cobrança no Asaas...")
            cobranca_asaas = Asaas_instance.criar_cobranca_pix(
                customer_id=customer.asaas_id,
                valor=float(valor_total.quantize(Decimal('0.01'))),
                descricao=f"Reserva Rota: {rota.nome} - Cliente: {customer.nome}",
                #adicionar 3 dias para
                vencimento=(datetime.now().date() + timedelta(days=3)).isoformat()  
            )
            print("Cobranca criada no Asaas:", cobranca_asaas)
            # print("Cobranca criada:", cobranca_asaas)
            pixTransaction = Asaas_instance.pixQrCode(cobranca_asaas.get('id',''))
            
            print("Pix Transaction:", pixTransaction)
            
            qr_code_pix = pixTransaction.get('encodedImage','') if pixTransaction else ''
            code_pix = pixTransaction.get('payload','') if pixTransaction else ''
            
            link_cobranca = cobranca_asaas.get('invoiceUrl','')
            
            # ===== Criar Reserva =====
            reserva = Reserva.objects.create(
                customer=customer,
                rota=rota,
                suite=suite,
                valor_total=valor_total.quantize(Decimal('0.01')),
                data_reserva=data_reserva,
                status_reserva=status_reserva,
                pago=False,
                qr_code_pix=qr_code_pix,
                code_pix=code_pix,
                cobranca_asaas_id=cobranca_asaas.get('id',''),
                cobranca_asaas_link=link_cobranca,
            )
            
            # ===== Criar Passageiros =====
            for passageiro_data in passageiros:
                passageiro = PassageirosReserva.objects.create(
                    nome=passageiro_data.get('nome'),
                    documento=passageiro_data.get('documento'),
                    data_nascimento=passageiro_data.get('data_nascimento') or None,
                    pcd=passageiro_data.get('pcd', False),
                    suite=Suite.objects.get(id=suite_id) if passageiro_data.get('suite') and suite_id else None,
                )
                reserva.passageiros.add(passageiro)

            return redirect('/viagens/reservas/list')

        except Exception as e:
            clientes = Customer.objects.filter(client=request.user.client)
            rotas = Rota.objects.filter(client=request.user.client, ativo=True)
            suites = Suite.objects.filter(client=request.user.client, ativo=True)

            return render(request, 'Reservas/Create', {
                'clientes': list(clientes),
                'rotas': list(rotas),
                'suites': list(suites),
                'errors': {'erro': str(e)}
            })
class EditReservaView(View):
    def get(self, request, reserva_id):
        reserva = Reserva.objects.get(id=reserva_id, customer__client=request.user.client)
        
        # print("Carregando reserva para edição:", reserva)
        clientes = Customer.objects.filter(client=request.user.client)
        rotas = Rota.objects.filter(client=request.user.client, ativo=True)
        suites = Suite.objects.filter(client=request.user.client, ativo=True)
        
        # Carrega os passageiros da reserva
        passageiros = list(reserva.passageiros.all())
        
        return render(request, 'Reservas/Edit', {
            'reserva': lambda: reserva,
            'passageiros': passageiros,
            'clientes': list(clientes),
            'rotas': list(rotas),
            'suites': list(suites),
        })

    def delete(self, request, reserva_id):
        reserva = Reserva.objects.get(id=reserva_id, customer__client=request.user.client)
        reserva.delete()
        return redirect('/viagens/reservas/list')


class DashboardView(View):
    def get(self, request):
        user = request.user
        client = user.client
        
        # Data de hoje
        hoje = date.today()
        
        # Total de reservas para hoje
        reservas_hoje = Reserva.objects.filter(
            customer__client=client,
            data_reserva=hoje
        ).count()
        
        # Reservas dos últimos 7 dias (com contagem por dia)
        sete_dias_atras = hoje - timedelta(days=6)
        reservas_7_dias = []
        for i in range(7):
            dia = sete_dias_atras + timedelta(days=i)
            count = Reserva.objects.filter(
                customer__client=client,
                data_reserva=dia
            ).count()
            reservas_7_dias.append({
                'data': dia.strftime('%Y-%m-%d'),
                'total': count
            })
        
        # Vendas dos últimos 30 dias (com valor total por dia)
        trinta_dias_atras = hoje - timedelta(days=29)
        vendas_30_dias = []
        for i in range(30):
            dia = trinta_dias_atras + timedelta(days=i)
            total_vendas = Reserva.objects.filter(
                customer__client=client,
                data_reserva=dia
            ).aggregate(total=models.Sum('valor_total'))['total'] or Decimal('0.00')
            
            vendas_30_dias.append({
                'data': dia.strftime('%Y-%m-%d'),
                'valor': float(total_vendas)
            })
        
        # Total de vendas dos últimos 30 dias
        total_vendas_30_dias = Reserva.objects.filter(
            customer__client=client,
            data_reserva__gte=trinta_dias_atras
        ).aggregate(total=models.Sum('valor_total'))['total'] or Decimal('0.00')
        
        # Total de reservas dos últimos 7 dias
        total_reservas_7_dias = Reserva.objects.filter(
            customer__client=client,
            data_reserva__gte=sete_dias_atras
        ).count()
        
        # Total de suítes reservadas hoje
        suites_reservadas_hoje = Reserva.objects.filter(
            customer__client=client,
            data_reserva=hoje,
            suite__isnull=False
        ).count()
        
        # Total de passageiros no dia
        reservas_hoje_ids = Reserva.objects.filter(
            customer__client=client,
            data_reserva=hoje
        ).values_list('id', flat=True)
        
        total_passageiros_hoje = PassageirosReserva.objects.filter(
            reservas__id__in=reservas_hoje_ids
        ).count()
        
        # Rota mais usada (baseado em reservas de hoje)
        rota_mais_usada = Reserva.objects.filter(
            customer__client=client,
            data_reserva=hoje,
            rota__isnull=False
        ).values('rota__nome').annotate(
            total=models.Count('id')
        ).order_by('-total').first()
        
        rota_mais_usada_nome = rota_mais_usada['rota__nome'] if rota_mais_usada else 'Nenhuma'
        rota_mais_usada_count = rota_mais_usada['total'] if rota_mais_usada else 0
        
        return JsonResponse({
            'reservas_hoje': reservas_hoje,
            'total_reservas_7_dias': total_reservas_7_dias,
            'reservas_7_dias': reservas_7_dias,
            'vendas_30_dias': vendas_30_dias,
            'total_vendas_30_dias': float(total_vendas_30_dias),
            'suites_reservadas_hoje': suites_reservadas_hoje,
            'total_passageiros_hoje': total_passageiros_hoje,
            'rota_mais_usada': {
                'nome': rota_mais_usada_nome,
                'total': rota_mais_usada_count
            }
        })


class ConfigViagemView(View):
    def get(self, request):
        # Buscar ou criar a configuração
        config, created = ConfigViagem.objects.get_or_create(
            client=request.user.client,
            defaults={
                'desconto_pcd': 0.00,
                'desconto_idoso': 0.00,
                'desconto_crianca_0_4': 0.00,
                'desconto_crianca_5_7': 0.00,
                'desconto_crianca_8_10': 0.00,
                'desconto_acima_11': 0.00,
            }
        )
        
        admin_token = JwtTokenAdmin.objects.filter(user=request.user).first()
        return render(request, 'Configuracoes/ConfigViagem', {
            'config': {
                'id': config.id,
                'desconto_pcd': float(config.desconto_pcd),
                'desconto_idoso': float(config.desconto_idoso),
                'desconto_crianca_0_4': float(config.desconto_crianca_0_4),
                'desconto_crianca_5_7': float(config.desconto_crianca_5_7),
                'desconto_crianca_8_10': float(config.desconto_crianca_8_10),
                'desconto_acima_11': float(config.desconto_acima_11),
                'token_asaas': config.token_asaas or '',
                'token_scale4': config.token_scale4 or '',
                'criado_em': config.criado_em.isoformat() if config.criado_em else '',
                'admin_jwt_token': admin_token.token if admin_token and admin_token.token else '',
                'admin_jwt_expira_em': admin_token.expira_em.isoformat() if admin_token and admin_token.expira_em else '',
            }
        })
    
    def post(self, request):
        # Buscar ou criar a configuração
        config, _ = ConfigViagem.objects.get_or_create(
            client=request.user.client,
            defaults={
                'desconto_pcd': 0.00,
                'desconto_idoso': 0.00,
                'desconto_crianca_0_4': 0.00,
                'desconto_crianca_5_7': 0.00,
                'desconto_crianca_8_10': 0.00,
                'desconto_acima_11': 0.00,
            }
        )
        
        # Atualizar os campos
        config.desconto_pcd = request.POST.get('desconto_pcd', config.desconto_pcd)
        config.desconto_idoso = request.POST.get('desconto_idoso', config.desconto_idoso)
        config.desconto_crianca_0_4 = request.POST.get('desconto_crianca_0_4', config.desconto_crianca_0_4)
        config.desconto_crianca_5_7 = request.POST.get('desconto_crianca_5_7', config.desconto_crianca_5_7)
        config.desconto_crianca_8_10 = request.POST.get('desconto_crianca_8_10', config.desconto_crianca_8_10)
        config.desconto_acima_11 = request.POST.get('desconto_acima_11', config.desconto_acima_11)
        config.token_asaas = request.POST.get('token_asaas', config.token_asaas)
        config.token_scale4 = request.POST.get('token_scale4', config.token_scale4)
        config.save()
        
        admin_token = JwtTokenAdmin.objects.filter(user=request.user).first()
        return render(request, 'Configuracoes/ConfigViagem', {
            'config': {
                'id': config.id,
                'desconto_pcd': float(config.desconto_pcd),
                'desconto_idoso': float(config.desconto_idoso),
                'desconto_crianca_0_4': float(config.desconto_crianca_0_4),
                'desconto_crianca_5_7': float(config.desconto_crianca_5_7),
                'desconto_crianca_8_10': float(config.desconto_crianca_8_10),
                'desconto_acima_11': float(config.desconto_acima_11),
                'token_asaas': config.token_asaas or '',
                'token_scale4': config.token_scale4 or '',
                'criado_em': config.criado_em.isoformat() if config.criado_em else '',
                'admin_jwt_token': admin_token.token if admin_token and admin_token.token else '',
                'admin_jwt_expira_em': admin_token.expira_em.isoformat() if admin_token and admin_token.expira_em else '',
            },
            'mensagem': 'Configuração atualizada com sucesso'
        })