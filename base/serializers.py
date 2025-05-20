from rest_framework import serializers
from .models import Product,ProductType,User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email','image','address','contact_no','created_at','updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'
        
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductType
        fields='__all__'
        