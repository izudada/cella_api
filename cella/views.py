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
from .models import Brand, Product
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


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
        "token": Token.objects.get_or_create(user=user)[0][1]
        })


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):

#         data = {}
#         body = json.loads(request.body)
#         email = body['email']
#         password = body['password']
#         try:

#             account = User.objects.get(email=email)
#         except BaseException as e:
#             raise ValidationError({"400": f'{str(e)}'})

#         token = Token.objects.get_or_create(user=account)[0].digest
#         if not check_password(password, account.password):
#             raise ValidationError({"message": "Incorrect Login credentials"})

#         if account:
#             if account.is_active:
#                 login(request, account)
#                 data["message"] = "user logged in"
#                 data["email_address"] = account.email

#                 Res = {"data": data, "token": token}

#                 return Response(Res)

        #     else:
        #         raise ValidationError({"400": f'Account not active'})

        # else:
        #     raise ValidationError({"400": f'Account doesnt exist'})

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