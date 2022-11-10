import uuid as my_uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.validators import UnicodeUsernameValidator

from .manager import CustomUserManager
from datetime import datetime


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class TimeStampedUUIDModel(models.Model):
    pkid = models.UUIDField(primary_key=True, editable=False, default="000000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name=_("Username"), max_length=255, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+2348131234568"
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("Country"), default="NG", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Lagos",
        blank=False,
        null=False,
    )
    is_verified = models.BooleanField( default=False )
    nin = models.CharField(max_length=30, default="222333444555" )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    email_verified = models.BooleanField(
        _('email_verified'),
        default=False,
        help_text=_(
            'Designates whether this users email verified. '
        ),
    )
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)


class Product(TimeStampedUUIDModel, models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True)
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )

class Cart(TimeStampedUUIDModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)


    def price_ttc(self):
        return self.price_ht 

    def __str__(self):
        return  self.client + " - " + self.product