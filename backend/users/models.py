import re
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

from uploads.models import ImageFile


def validate_no_whitespace(value):
    if re.search(r'\s', value):
        raise ValidationError('No whitespace allowed in username.')


class UserModelManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user with the specified email and password.
        :param email: The email address of the user.
        :param password: The password for the user.
        :param extra_fields: Additional fields to be set on the user model.
        :return: The created user object.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a new superuser with the specified email and password.
        :param email: The email address of the superuser.
        :param password: The password for the superuser.
        :param extra_fields: Additional fields to be set on the user model.
        :return: The created superuser object.
        """
        if not email:
            raise ValueError('The Email field must be set')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractBaseUser):
    """
    Custom user model that uses email instead of username for authentication.
    """
    username = models.CharField(max_length=25, unique=True, validators=[validate_no_whitespace])
    email = models.EmailField(max_length=64, unique=True)
    bio = models.TextField(blank=True, null=True)
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
    REQUIRED_FIELDS = ['username']

    objects = UserModelManager()

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        Simple implementation: if user is active and is a superuser, grant all permissions.
        """
        return self.is_active and self.is_superuser

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Simple implementation: if user is active and is a superuser, grant all permissions.
        """
        return self.is_active and self.is_superuser
    
    def delete(self, *args, **kwargs):
        """
        Overridden delete method to remove the associated profile image 
        from the filesystem and database upon deletion of the user.
        """
        # Check if the user has a profile image and delete the ImageFile object
        if hasattr(self, 'profile_image') and self.profile_image:
            self.profile_image.delete()  # This calls the overridden delete method of ImageFile

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"User {self.id}: {self.username}, {self.email}"
