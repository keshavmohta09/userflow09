from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta
from django.conf import settings
import jwt
from jwt import algorithms
from .helpers import CustomUserManager

# Create your models here.

        
class User(AbstractUser):    
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def token(self):
        return self.generate_token()

    def get_full_name(self):
        full_name = self.first_name
        if self.last_name:
            full_name += " " + self.last_name
        return full_name


    def generate_token(self):
        """
        Generate jwt token
        """
        
        token = jwt.encode({
            'id': self.pk,
            'exp': now() + timedelta(minutes=5) 
        }, settings.SECRET_KEY, algorithm="HS256")

        return token.decode('utf-8')
        