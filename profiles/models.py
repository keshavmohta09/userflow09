from django.db import models
from authentication.models import User

# Create your models here.
class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        

class Profile(Base):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField()
    
    def __str__(self) -> str:
        return self.user.email