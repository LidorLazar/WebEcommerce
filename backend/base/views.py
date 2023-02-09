
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
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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
    try:
        user = Profile.objects.create(
            name=data['name'],
            email=data['email'],
            username=data['name'],
            address=data['address'],
            city=data['city'],
            password=password
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        return Response({"msg": 'errrrroooorrrrrr'}, status=status.HTTP_404_NOT_FOUND)


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
