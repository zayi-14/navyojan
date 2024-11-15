import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group, User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as django_login


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',
        related_query_name='user',
    )
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    package = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

    @staticmethod
    def custom_authenticate(username, password):
        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                return user
        except CustomUser.DoesNotExist:
            pass
        return None

    @classmethod
    def login(cls, request, user):
        # Perform any additional actions needed before logging in
        # ...

        # Finally, log in the user
        django_login(request, user)


class Payment_webhook(models.Model):
    payment_amount = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    checkout_session_id = models.CharField(max_length=250)
    payment_intent_id = models.CharField(null=True, max_length=250)
    payment_date = models.DateTimeField()
    payment_status = models.CharField(max_length=250, null=True)
    expiry_date = models.DateTimeField(null=True)
