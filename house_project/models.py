from typing import Type
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.manager import BaseManager
from django.utils.translation import gettext_lazy as _



# Create your models here.
class House(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=100)
    description = models.TextField()
    house_host = models.ForeignKey('User', on_delete=models.CASCADE, related_name='hosted_houses')
    guest = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='rented_houses')
    is_rented = models.BooleanField(default=False)
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} is located in {self.country}, {self.city}, {self.state}"


class House_image(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.image} belong to {self.house.name}"

    

class User(AbstractUser):
    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="house_project_user",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="house_project_user_permissions",
        related_query_name="user",
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    is_House_owner = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    


