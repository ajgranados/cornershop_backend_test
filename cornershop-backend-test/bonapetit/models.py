from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, blank=True, null=True)

"""class Role(models.Model):
    name = models.CharField(max_length=50)"""

class User(AbstractBaseUser, PermissionsMixin):
    CHEF = 1
    EMPLOYEE = 2

    ROLE_CHOICES = (
        (CHEF, 'Chef'),
        (EMPLOYEE, 'Employee')
    )

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Menu(models.Model):
    name = models.CharField(max_length=100)
    available_date = models.DateField()
    uuid = models.UUIDField()

class MenuOption(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

class EmployeeMenu(models.Model):
    user_id = models.IntegerField()
    option_id = models.IntegerField()
    without = models.TextField(blank=True, null=True)
    extra = models.TextField(blank=True, null=True)
