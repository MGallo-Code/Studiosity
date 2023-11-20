from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from uploads.models import ImageFile


class UserModelManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    validated_account = models.BooleanField(default=False)
    profile_image = models.OneToOneField(
        ImageFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='profile_image_user'
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserModelManager()

    def __str__(self):
        return f"User {self.id}: {self.username} | {self.email}"