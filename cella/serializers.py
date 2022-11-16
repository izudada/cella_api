from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from .models import Brand, Product


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User  


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'nin', 'username','password', 'password2', 'nin', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        """
            A method overiding DRF serializer's save method
        """
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            nin = self.validated_data['nin'],
            is_verified = True
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()

        return user


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'uuid', 'created_at']

    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['brand', 'name', 'description', 'price', 'sold', 'in_stock', 'total', 'created_at']