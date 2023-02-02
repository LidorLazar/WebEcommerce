
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .models import Product
from django.contrib.auth.models import User
from .serilaizer import ProductSerializer,  UserSerializer, UserSerializerWithToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView


# Create your views here.

######################################################
############# Authentication #########################
######################################################

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         serializer = UserSerializerWithToken(self.user).data
#         for key, vlaue in serializer.items():
#             data[key] = vlaue
#         return data


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

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
    try:
        data = request.data
        user = User.objects.create(
            first_name=data['name'],
            email=data['email'],
            username=data['name'],
            password=make_password(data['password']))
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)



class RefreshTokenView(generics.GenericAPIView):
    serializer_class = TokenRefreshSerializer

    

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.validated_data, status=status.HTTP_200_OK)

############################################
########### User ###########################
############################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serilaizer = UserSerializer(user, many=False)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    serilaizer = UserSerializer(User.objects.all(), many=True)
    return Response(serilaizer.data)



@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>/reviwes/',
        '/api/products/top/',
        '/api/products/<id>',
        '/api/products/delete/<id>',
        '/api/products/<update>/<id>',
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serilaizer = UserSerializer(user, many=False)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    serilaizer = UserSerializer(User.objects.all(), many=True)
    return Response(serilaizer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many= False)


    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data["email"]

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()
    
    return Response(serializer.data)

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
