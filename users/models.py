# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove username
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True) 
    
    objects = UserManager()
    client = models.OneToOneField('Client', on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')
    jwt_token = models.TextField(null=True, blank=True)
    
    class InertiaMeta:
        fields = ('name', 'created_at')
        

class JwtTokenAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "JWT Token"
        verbose_name_plural = "JWT Tokens"

    def __str__(self):
        return f"JWT para {self.user.username}"
    
class Client(models.Model):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f"Client Profile for {self.name or 'Unnamed Client'}"
    class InertiaMeta:
        fields = ('phone_number', 'address', 'name')