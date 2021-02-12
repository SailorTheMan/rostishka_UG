from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin  = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # avatar = models.ImageField('logo.png', upload_to='avatars/', height_field=400, width_field=400)
    first_name = models.CharField(default='Имя', max_length=64)
    second_name = models.CharField(default='Фамилия', max_length=64)
    bio = models.TextField()
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    join_time = models.DateTimeField(default=timezone.now)
    expiry_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=15))

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin