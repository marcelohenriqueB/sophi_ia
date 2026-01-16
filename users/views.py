from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inertia import render as inertia_render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone
from datetime import timedelta
import secrets
from django.http import JsonResponse
from .models import JwtTokenAdmin

@ensure_csrf_cookie
def login_view(request):
    """View para renderizar e processar o login"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember', False)
        
        # Autenticar usuário
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Se "lembrar-me" não estiver marcado, sessão expira ao fechar navegador
            if not remember:
                request.session.set_expiry(0)
            
            return redirect('/')
        else:
            return inertia_render(request, 'Auth/Login', props={
                'errors': {
                    'credentials': 'Email ou senha incorretos.'
                }
            })
    
    # GET request - renderizar página de login
    return inertia_render(request, 'Auth/Login')


def logout_view(request):
    """View para processar o logout"""
    logout(request)
    return redirect('/login')


@login_required
def profile_view(request):
    """View para visualizar perfil do usuário"""
    return inertia_render(request, 'Auth/Profile', props={
        'user': {
            'name': request.user.name,
            'email': request.user.email,
        }
    })


@login_required
def dashboard_view(request):
    """View para renderizar a página inicial do dashboard"""
    return inertia_render(request, 'Dashboard/Index')


@login_required
@csrf_exempt
def admin_token_view(request):
    """Gera ou regenera o token de admin do usuário logado, válido por 5 anos.
    Retorna JSON com token e data de expiração. Em GET, apenas retorna o atual.
    """
    if request.method == 'GET':
        jwt_admin = JwtTokenAdmin.objects.filter(user=request.user).first()
        return JsonResponse({
            'success': True,
            'token': jwt_admin.token if jwt_admin and jwt_admin.token else '',
            'expira_em': jwt_admin.expira_em.isoformat() if jwt_admin and jwt_admin.expira_em else ''
        })

    # POST: gerar novo token
    token = secrets.token_urlsafe(64)
    expira = timezone.now() + timedelta(days=365*5)

    jwt_admin, _ = JwtTokenAdmin.objects.get_or_create(user=request.user)
    jwt_admin.token = token
    jwt_admin.expira_em = expira
    jwt_admin.save()

    # Também salva no perfil do usuário por conveniência
    request.user.jwt_token = token
    request.user.save(update_fields=['jwt_token'])

    return JsonResponse({
        'success': True,
        'token': token,
        'expira_em': expira.isoformat()
    })
