from inertia import share
import json
from django.shortcuts import redirect

def inertia_share_middleware(get_response):
    def middleware(request):
        if request.content_type == 'application/json':
            try:
                request.json = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError as e:
                request.json = {}
        else:
            request.json = {}

        share(
            request,
            auth=lambda: {
                "user": {
                    "id": request.user.id,
                    "email": request.user.email,
                    "name": request.user.name,
                }
            } if request.user.is_authenticated else {"user": None}
        )

        return get_response(request)

    return middleware


def redirect_if_not_authenticated(get_response):
    """Middleware para redirecionar usuários não autenticados para login"""
    def middleware(request):
        # Rotas públicas que não precisam de autenticação
        public_paths = ['/login', '/logout', '/admin/', '/static/', '/assets/']
        
        # Verificar se a rota é pública
        is_public = any(request.path.startswith(path) for path in public_paths)
        
        # Se não for uma rota pública e o usuário não estiver autenticado
        if not is_public and not request.user.is_authenticated:
            return redirect('/login')
        
        return get_response(request)
    
    return middleware
