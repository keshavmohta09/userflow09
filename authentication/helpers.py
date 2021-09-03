from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
    
class CustomUserManager(BaseUserManager):
    """
    Custom User manager
    """

    def create_user(self, username, email, password=None,first_name=None,last_name=None):
        """create user"""
        if username is None:
            return False , "Username is required"
        if email is None:
            return False , "Email is required"

        user = self.model(username=username, email=self.normalize_email(email))
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.set_password(password)
        user.save()

        return True, user

    def create_superuser(self, username, email, password):
        """
        Create superuser
        """
        if password is None:
            raise ValidationError('Password is required')

        _success , user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user