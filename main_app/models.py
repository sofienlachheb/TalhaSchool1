from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
class CustomUser(AbstractUser):
    USER_TYPE = (
        (1, 'Manager'), 
        (2, 'Teacher'),
        (3, 'Student'),
        (4, 'employee'),
        )
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    username = None
    email=models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Additional teacher-specific fields

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Additional student-specific fields

class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Additional parent-specific fields

class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Additional manager-specific fields
