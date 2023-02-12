
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .models import Product, Profile, Reviwe, Order
from .serilaizer import ProductSerializer, UserSerializerWithToken, ProfileSerializer, ReviweSerializer, OrderSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.generic import View


# Create your views here.

######################################################
############# Authentication #########################
######################################################


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
    name=data['name']
    email=data['email']
    username=data['name']
    address=data['address']
    city=data['city']
    password=password
    if not (password and name and email and username and address and city): #Check if all the inputs is full
        return Response({"error": "You need to put all required fields."},status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profile.objects.get(username=data['name']) #Chack if the username is exist in Profile 
        return Response({'error': 'The username already exists. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        try:
            profile = Profile.objects.get(email=email)#Chack if the email is exist in Profile 
            return Response({'error': 'The email already exists. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            user = Profile.objects.create( name=data['name'],email=data['email'],username=data['name'],address=data['address'],city=data['city'],password=password)
            serializer = ProfileSerializer(user, many=False)
            return Response(serializer.data)




class RefreshTokenView(generics.GenericAPIView):
    serializer_class = TokenRefreshSerializer


############################################
########### User ###########################
############################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serilaizer = ProfileSerializer(Profile, many=False)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    serilaizer = ProfileSerializer(Profile.objects.all(), many=True)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serilaizer = ProfileSerializer(user, many=False)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    serilaizer = ProfileSerializer(Profile.objects.all(), many=True)
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
@api_view(['GET'])
def get_products(request):
    products_serilaizer = ProductSerializer(Product.objects.all(), many=True)
    return Response(products_serilaizer.data)


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
def get_all_review(request):
    serializer = ReviweSerializer(Reviwe.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_review_spsific_prod(request, pk):
    reviews = Reviwe.objects.filter(product=Product.objects.get(id=pk))
    serializer = ReviweSerializer(reviews, many=True)
    return Response(serializer.data)


###########################################
########## order ##########################
###########################################


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_user(request):
    user = request.user
    order = Order.objects.filter(user_id=user)
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    serializer = OrderSerializer(
        data=request.data["orderData"], context={"user": request.user}
    )
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        print(serializer.data)
        for item in request.data["orderDetails"]:
            # print(request.data)
            order_dets = {}
            order_dets["product"] = item["id"]
            order_dets["order"] = (
                Order.objects.values_list("id", flat=True)
                .filter(user=request.user.id)
                .last()
            )
            serializer2 = OrderItemSerializer(data=order_dets)
            if serializer2.is_valid(raise_exception=True):
                serializer2.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



