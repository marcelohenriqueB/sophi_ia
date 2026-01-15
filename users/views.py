from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inertia import render as inertia_render
from django.views.decorators.csrf import ensure_csrf_cookie

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
