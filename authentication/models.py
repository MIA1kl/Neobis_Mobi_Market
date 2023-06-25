from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):

        if email is None:
            raise TypeError('User should have an email')
        
        if username is None:
            raise TypeError('User should have a username')

        user=self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, username, email,password=None, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password ')
        
        user=self.create_user( username, email, password,  **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



