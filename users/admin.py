

# Register your models here.
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import JwtTokenAdmin, User, Client
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.html import format_html
from datetime import timedelta


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'is_staff', 'is_active', 'name', 'created_at')

    # Campos normais do usuário
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'name',
                'client',
            )
        }),
        ('Permissões', {
            'fields': (
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        # 🔹 Fieldset extra apenas para o JWT
        ('JWT Token', {
            'fields': ('jwt_token',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # 🔹 Coloque o método em readonly_fields
    readonly_fields = ('jwt_token',)

    search_fields = ('email',)

    # 🔹 Método que gera o JWT
    def jwt_token(self, obj):
        if not obj.pk:
            return "Salve o usuário para gerar o token"

        # Gera apenas se não existir
        if not obj.jwt_token:
            refresh = RefreshToken.for_user(obj)
            refresh.set_exp(lifetime=timedelta(days=365 * 3))
            refresh.access_token.set_exp(lifetime=timedelta(days=365 * 3))

            obj.jwt_token = str(refresh.access_token)
            obj.save(update_fields=['jwt_token'])
    
        return format_html(
            "<textarea rows='4' cols='90' readonly>{}</textarea>",
            obj.jwt_token
        )

    jwt_token.short_description = "JWT Token (3 anos)"
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'address')
    search_fields = ('phone_number', 'address')
    
    

@admin.register(JwtTokenAdmin)
class JwtTokenAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'gerar_token', 'criado_em')
    readonly_fields = ('criado_em',)

    def gerar_token(self, obj):
        refresh = RefreshToken.for_user(obj.user)

        # força 3 anos
        refresh.set_exp(lifetime=timedelta(days=365 * 3))
        refresh.access_token.set_exp(lifetime=timedelta(days=365 * 3))

        return format_html(
            "<textarea rows='4' cols='80' readonly>{}</textarea>",
            refresh.access_token
        )

    gerar_token.short_description = "JWT (3 anos)"