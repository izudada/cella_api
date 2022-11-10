from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, UserSerializer, BrandSerializer, ProductSerializer
from .verify import verify_id
import json
import uuid as my_uuid
from django.contrib.auth import get_user_model

from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Brand, Product, Order, Item
from rest_framework.authtoken.models import Token



try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User  


@api_view(['POST',])
@permission_classes([])
def verify_user(request):
    nin = request.data['nin']
    user_data = verify_id(str(nin))
    print(user_data)
    if user_data["transactionStatus"] == "SUCCESSFUL":
        result = json.dumps(user_data["response"])
        return Response(result)
    message = {"message": user_data["description"]}
    return Response(status=status.HTTP_404_NOT_FOUND, data=message)


# Register API/Checkout
@api_view(["POST"])
@permission_classes([AllowAny])
def checkout(request):
    try:
        data = {}
        user_data = {}
        response = request.data
        user_data['email'] = response['email']
        user_data['first_name'] = response['firstName']
        user_data['last_name'] = response['lastName']
        user_data['state'] = response['state']
        user_data['password'] = response['password']
        user_data['password2'] = response['password2']
        user_data['username'] = response['username']
        user_data['nin'] = response['nin']
        serializer = RegisterSerializer(data=user_data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.is_verified = True
            account.save()
            token = Token.objects.get_or_create(user=account)
            data["message"] = "user registered successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["token"] = token[0].key
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['state'] = account.state

            total = 0
            for i in request.data['products']:
                total += i['price'] * i['quantity']
                
            new_order = Order.objects.create(
                user=account, 
                ref=response['reference'],
                total= total
            )
            new_order.save()

            for i in request.data['products']:
                new_item = Item.objects.create(
                    order=new_order,
                    title = i['title'],
                    image = i['image'],
                    quantity = i['quantity']
                )
                new_item.save()

        else:
            data = serializer.errors

        print(data)     
        return Response(data)
    except Exception as e:
        print(e)
        message = {"message": "issue creating checkout"}
        return Response(status=status.HTTP_400_BAD_REQUEST, data=message)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):

        data = {}
        reqBody = json.loads(request.body)
        email1 = reqBody['Email_Address']
        print(email1)
        password = reqBody['password']
        try:

            Account = User.objects.get(Email_Address=email1)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = Token.objects.get_or_create(user=Account)[0].key
        print(token)
        if not check_password(password, Account.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"
                data["email_address"] = Account.email

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})



@api_view(["GET"])
@permission_classes([AllowAny])
def say_hello(request):
    return Response({"message": "Hello World"})


class BrandApiListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # authentication_classes = (AllowAny,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination


class ProductApiListView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('brand__name', 'name', 'description', 'price',)