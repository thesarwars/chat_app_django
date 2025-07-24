from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, full_name, email, password, **extra_fields):
        if not email:
            raise ValidationError('Email is required')
        if not password:
            raise ValidationError('Password is required')
        
        user = self.model(full_name=full_name.title(), email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, full_name, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must is_staff True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must is_superuser True")
        
        user = self.create_user(full_name, email, password, **extra_fields)
        return user