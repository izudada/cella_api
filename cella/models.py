import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=255, unique=True)
    state = models.CharField(verbose_name=_("State"), max_length=55, default="Lagos")
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    nin = models.CharField(default="22233344455", max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}/{}?token={}".format(settings.DOMAIN, reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@info.cella.com",
        # to:
        [reset_password_token.user.email]
    )
    return {"token": reset_password_token.key}


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref = models.CharField(default="scotch", max_length=50, unique=True)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)  

    def __str__(self):
        return self.ref

    def get_items(self):
        return list(self.item_set.all())


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(default="scotch", max_length=200)
    image = models.URLField()
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)  

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(default="scotch", max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)  

    def __str__(self):
        return self.name

    def get_products(self):
        return list(self.product_set.all())


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(default="name", max_length=50, unique=True)
    description = models.TextField(default="describe product")
    price = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    in_stock = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)  

    def __str__(self):
        return self.name
