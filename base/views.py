from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Product,ProductType
from .serializers import ProductSerializer,ProductTypeSerializer,UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.

class ProductApiView(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
    

class ProductTypeApiView(GenericAPIView):
    queryset=ProductType.objects.all()
    serializer_class=ProductTypeSerializer

    def get(self,request):
        product_type_objs= self.get_queryset()
        serializer=self.get_serializer(product_type_objs,many=True)
        return Response(serializer.data) 
    
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class ProductTypeDetailApiView(GenericAPIView):
    
    queryset=ProductType.objects.all()
    serializer_class=ProductTypeSerializer
    
    def get(self,request,pk):
        product_type_obj=self.get_object()
        serializer=self.get_serializer(product_type_obj)
        return Response(serializer.data)

    def put(self,request,pk):
        product_type_obj=self.get_object()
        serializer=self.get_serializer(product_type_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        product_type_obj=self.get_object()
        product_type_obj.delete()
        return Response(
            {
                "message":"Deleted successfully"
            },
            status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    password=request.data.get('password')
    hash_password=make_password(password)
    data=request.data.copy()
    data['password']=hash_password
    serializer=UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')
    
    user=authenticate(username=username,password=password)
    if user:
        token,_=Token.objects.get_or_create(user=user)  #here instead of _ we can use any variable ..get_or_create gives tuples with two values (Token,bool)
        return Response(token.key,status=status.HTTP_200_OK)
    else:
        return Response('Invalid username or password!',status=status.HTTP_400_BAD_REQUEST)