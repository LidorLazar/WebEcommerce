from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product,Order,OrderItem,Reviwe,ShippingAddress, Profile
from rest_framework_simplejwt.tokens import RefreshToken


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields ='__all__'

    def get_name(self, obj):
        if obj.first_name:
            return obj.first_name
        else:
            return obj.email

    def get_id(self, obj):
        return obj.id

    def get_admin(self, obj):
        return obj.is_staff
  
class UserSerializerWithToken(ProfileSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id',  'username', 'email', 'name', 'admin', 'token', ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ReviweSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviwe
        fields = '__all__'
        
        
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

