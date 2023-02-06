
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .models import Product, Profile, Reviwe
from .serilaizer import ProductSerializer, UserSerializerWithToken, ProfileSerializer, ReviweSerializer
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
        password=make_password(data['password'])
        user = Profile.objects.create(
            name=data['name'],
            email=data['email'],
            username=data['name'],
            address=data['address'],
            city=data['city'],
            password = password
          )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        print(e)
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
    serilaizer = ProfileSerializer(Profile, many=False)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    serilaizer = ProfileSerializer(Profile.objects.all(), many=True)
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
    serilaizer = ProfileSerializer(user, many=False)
    return Response(serilaizer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    serilaizer = ProfileSerializer(Profile.objects.all(), many=True)
    return Response(serilaizer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many= False)
    data = request.data
    print(data)
    # user.image = data['image']
    # data.city = data['city']
    # user.address = data["address"]
    # user.phone_number = data["phone_number"]

    # if data['password'] != '':
    #     user.password = make_password(data['password'])

    print(user)
    # user.save()
    
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
    return Response (serializer.data)


@api_view(['GET'])
def get_review_spsific_prod(request, pk):
    reviews = Reviwe.objects.filter(product=Product.objects.get(id=pk))
    serializer = ReviweSerializer(reviews, many=True)
    return Response(serializer.data)