
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .models import Product, Profile, Reviwe, Order, OrderItem
from .serilaizer import ProductSerializer, OrderItemSerializer, ProfileSerializer, ReviweSerializer, OrderSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password


# Create your views here.

######################################################
############# Authentication #########################
######################################################
"""
All the function related in authentication

1. Login 
2. Register -in register i chack if username or email not exist

"""

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add more properties
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    data = request.data
    password = make_password(data['password'])
    name = data['name']
    email = data['email']
    username = data['name']
    address = data['address']
    city = data['city']
    password = password
    # Check if all the inputs is full
    if not (password and name and email and username and address and city):
        return Response({"error": "You need to put all required fields."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Chack if the username is exist in Profile
        profile = Profile.objects.get(username=data['name'])
        return Response({'error': 'The username already exists. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        try:
            # Chack if email is exist in Profile
            profile = Profile.objects.get(email=email)
            return Response({'error': 'The email already exists. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            user = Profile.objects.create(name=data['name'], email=data['email'], username=data['name'],
                                          address=data['address'], city=data['city'], password=password)
            serializer = ProfileSerializer(user, many=False)
            return Response(serializer.data)


class RefreshTokenView(generics.GenericAPIView):
    serializer_class = TokenRefreshSerializer


############################################
########### User ###########################
############################################

"""
All the function related in User

1. Get data per user
2. Update datd per user 

"""



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serilaizer = ProfileSerializer(user, many=False)
    return Response(serilaizer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = ProfileSerializer(
        instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


#################################################################
################### Product #####################################
#################################################################


"""
All the function related in Product

1. Get product per id 
2. Get all the product from spsific category

"""
@api_view(['GET'])
def get_all_products(requset):
    products_serilaizer = ProductSerializer(Product.objects.all(), many=True)
    return Response (products_serilaizer.data)



@api_view(['GET'])
def get_products_id(request, pk):
    try:
        products_serilaizer1 = ProductSerializer(
            Product.objects.get(id=pk), many=False)
        return Response(products_serilaizer1.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def product_from_category(request, pk):
    try:
        serilaizer1 = ProductSerializer(
            Product.objects.filter(category=pk), many=True)
        return Response(serilaizer1.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

################################################
############# Review ###########################
################################################


"""
All the function related in Review

1. Send review + rating on spsific product
2. Get data from review per product

"""

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_review(request):
    data = request.data
    user = request.user

    try:
        product = Product.objects.get(id=data['id'])
        profile = Profile.objects.get(username=user)
        create_review_serilaizer = Reviwe.objects.create(
            product=product,
            user_id=profile,
            name=user.username,
            rating=data['rating'],
            text_comment=data['description']
        )
        return Response('add')
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_review_spsific_prod(request, pk):
    reviews = Reviwe.objects.filter(product=Product.objects.get(id=pk))
    serializer = ReviweSerializer(reviews, many=True)
    return Response(serializer.data)


###########################################
########## order ##########################
###########################################
"""
All the function related in order

1. Create a new order 
2. Get data all products in spsific user buy 
3. Get all the data in orders per user

"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_user(request):
    user = request.user
    order = Order.objects.filter(user=user)
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def return_all_product_in_order_user(request):
    user = request.user
    list_prod = []
    order = OrderItem.objects.filter(name=user)
    serializer = OrderItemSerializer(order, many=True)
    for i in range(len(serializer.data)):
        list_prod.append(serializer.data[i]['product'])
    return Response(list_prod)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_new_order(request): 
    order_serializer = OrderSerializer(data=request.data["orderData"], context={"user": request.user})
    order_serializer.is_valid(raise_exception=True)
    order = order_serializer.save()
    # Create a list of order details and save them
    order_details = [
        {
            "product": item["id"],
            "order": order.id,
            "qty": item["qty"],
            "total": float(item["price"]) * item["qty"],
            "name" : request.user.id
        }
        for item in request.data["orderDetails"]
    ]
    order_detail_serializer = OrderItemSerializer(data=order_details, many=True)
    order_detail_serializer.is_valid(raise_exception=True)
    order_detail_serializer.save()

    # Calculate the order total and qty
    order_total = round(sum(detail["total"] for detail in order_details), 2)
    order_qty = sum(detail["qty"] for detail in order_details)

    # Update the order with the total and qty
    order.total = order_total
    order.qty = order_qty
    order.save()

    # Serialize and return the order in the response
    response_data = OrderSerializer(order).data
    return Response(response_data, status=status.HTTP_201_CREATED)






