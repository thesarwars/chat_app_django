from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import CustomUserManager
# from django.contrib.auth import get_user_model

# # Create your models here.
# User = get_user_model()


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name', 'password')
    objects = CustomUserManager()

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    

class Messages(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_message")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_message")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"sender: {self.sender.full_name} receiver: {self.receiver.full_name}"
    
    class Meta:
        ordering = ['timestamp']

    