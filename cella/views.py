from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer, UserSerializer, BrandSerializer, ProductSerializer, ChangePasswordSerializer
from .verify import verify_id
import json
from django.contrib.auth import get_user_model

from django.contrib.auth import login
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



# def check_user_request(user):
#     """
#         Function to check if user
#     """
#     if user.is_authenticated and user.is_staff:
#         return True
#     else:
#         return False


@api_view(['POST',])
@permission_classes([])
def verify_user(request):
    nin = request.data['nin']
    user_data = verify_id(str(nin))
    print(user_data)
    if user_data["transactionStatus"] == "SUCCESSFUL":
        if len(user_data["response"]) > 1:
            result = json.dumps(user_data["response"])
            return Response(result)
        else:
            return Response(user_data)
    message = {"message": user_data["description"]}
    return Response(status=status.HTTP_404_NOT_FOUND, data=message)


# Register API/Checkout
@api_view(["POST"])
@permission_classes([AllowAny])
def checkout(request):
    try:
        data = {}
        user_data = {}
        user_data['email'] = request.data['email']
        user_data['first_name'] = request.data['firstName']
        user_data['last_name'] = request.data['lastName']
        user_data['state'] = request.data['state']
        user_data['password'] = request.data['password']
        user_data['password2'] = request.data['password2']
        user_data['username'] = request.data['username']
        user_data['nin'] = request.data['nin']
        message = ""
        try:
            account = User.objects.get(email=request.data['email'])
            message = "Checout created succesfuly"
        except User.DoesNotExist:
            message = "user registered successfully"
            serializer = RegisterSerializer(data=user_data)

            if serializer.is_valid():
                account = serializer.save()
                account.is_active = True
                account.save()
            
            else:
                data = serializer.errors

        token = Token.objects.get_or_create(user=account)
        data["message"] = message
        data["email"] = account.email
        data["username"] = account.username
        data["token"] = token[0].key
        data['first_name'] = account.first_name
        data['last_name'] = account.last_name
        data['state'] = account.state
        data['nin'] = account.nin

        try:
            total = 0
            for i in request.data['products']:
                total += i['price'] * i['quantity']
                
            new_order = Order.objects.create(
                user=account, 
                ref= request.data['reference'],
                total= total
            )
            new_order.save()
        except Exception as e:
            print(e)
            message = {"message": "issue creating order for checkout"}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=message)

        try:
            for i in request.data['products']:
                new_item = Item.objects.create(
                    order=new_order,
                    title = i['title'],
                    image = i['image'],
                    quantity = i['quantity']
                )
                new_item.save()
        except Exception as e:
            print(e)
            message = {"message": "issue creating items for checkout"}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=message)


   
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
        email1 = reqBody['email']
        password = reqBody['password']
        try:

            Account = User.objects.get(email=email1)
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination


class ProductApiListView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('brand__name', 'name', 'description', 'price',)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def brand_create_view(request):
    """
        An endpoint to create a brand

        variables:
            - serializer = serialize request data
            - is_admin = admin user authentication and auth
    """
    serializer = BrandSerializer(data=request.data)
    #   Check if serializer is valid
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def brand_update_view(request):
    """
        An endpoint to update a brand

        variables:
                - brand = stores the uuid of the brand
                - serializer = stores the serialized data
                - data = a dictionary that stores response
    """

    #   Check if item id exists using try block
    try:
        uuid = request.data['uuid']
        brand = Brand.objects.get(uuid=uuid)
    except Brand.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #   Save and return serialized data
    serializer = BrandSerializer(brand, data=request.data)
    data = {}

    #   Serializer checks if data sent is valid
    if serializer.is_valid():
        serializer.save()
        data["success"] = "update successful"
        return Response(data=data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def brand_delete_view(request):
    """
        An endpoint to delete a brand

        variables:
            - uuid = uuid of the brand
            - brand = Brand object 
            - data = dictionary to be returned 
    """

    #   Check if item id exists using try block
    try:
        uuid = request.data['uuid']
        brand = Brand.objects.get(uuid=uuid)
    except Brand.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    action = brand.delete()
    data = {}

    #   Check if action was sucessful or not
    if action:
        data["success"] = "delete successful"
    else:
        data["failure"] = "delete failed"
    return Response(data=data)


@api_view(['GET',])
@permission_classes((AllowAny,))
def brand_detail_view(request, uuid):
    """
        An endpoint to get the detail of a brand and its products

        variables:
                - brand = stores the brand object
                - serializer = stores the serialized data
    """
    data = {}
    #   Check if item id exists using try block
    try:
        brand = Brand.objects.get(uuid=uuid)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    products = brand.get_products()

    product_serializer = ProductSerializer(products, many =True)
    print(brand.get_products())
    data['products'] = product_serializer.data
    brand_serializer = BrandSerializer(brand)
    data['brand'] = brand_serializer.data
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def product_create_view(request):
    """
        An endpoint to create a brand

        variables:
            - serializer = serialize request data
            - brand = brand which product belongs to
            - data = dictionary to be returned
    """

    serializer = ProductSerializer(data=request.data)
    brand = Brand.objects.get(uuid=request.data['brand'])
    if serializer.is_valid():
        serializer.save(brand=brand, in_stock=request.data['total'])
        data = serializer.data
        data['brand'] = brand.name
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def product_update_view(request):
    """
        An endpoint to update a product

        variables:
                - product = stores the product object
                - serializer = stores the serialized data
                - data = a dictionary that stores response
    """

    #   Check if item id exists using try block
    try:
        uuid = request.data['uuid']
        product = Product.objects.get(uuid=uuid)
    except Product.DoesNotExist:
        return Response(data={"message": "Product doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    #   Save and return serialized data
    serializer = ProductSerializer(product, data=request.data)
    data = {}
    print("Bug````````````````")

    #   Serializer checks if data sent is valid
    if serializer.is_valid():
        if request.data['total']:
            stock = request.data['total'] - product.sold
            serializer.save(in_stock=stock)
        serializer.save()
        data = serializer.data
        data["message"] = "update successful"
        return Response(data=data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def product_delete_view(request):
    """
        An endpoint to delete a product

        variables:
                - product = stores the product object
                - data = a dictionary that stores response
                - action = for deleting an item
                - uuid = uuid from the request data
    """

    #   Check if item id exists using try block
    try:
        uuid = request.data["uuid"]
        product = Product.objects.get(uuid=uuid)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    action = product.delete()
    data = {}

    #   Check if action was sucessful or not
    if action:
        data["success"] = "delete successful"
    else:
        data["failure"] = "delete failed"
    return Response(data=data)


@api_view(['GET',])
@permission_classes((AllowAny,))
def product_detail_view(request, uuid):
    """
        An endpoint to get the detail of a brand

        variables:
                - product = stores the product object
                - serializer = stores the serialized data
    """

    #   Check if item id exists using try block
    try:
        product = Product.objects.get(uuid=uuid)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #   Save and return serialized data
    serializer = ProductSerializer(product)
    return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    """
        An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)