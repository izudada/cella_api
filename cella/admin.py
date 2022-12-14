

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Brand, Product, Order, Item



admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Item)