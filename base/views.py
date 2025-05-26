from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Product,ProductType
from .serializers import ProductSerializer,ProductTypeSerializer,UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,IsAdminUser,DjangoModelPermissions
from django.contrib.auth.models import Group

# Create your views here.

class ProductApiView(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated,DjangoModelPermissions]# DjangoModelPermissions allows only users with the right permissions to access this view.
    # DjangoModelPermissions checks the user's permissions against the model's permissions.
    filterset_fields=['type','department']
    search_fields=['name','description']
    

class ProductTypeApiView(GenericAPIView):
    queryset=ProductType.objects.all()
    serializer_class=ProductTypeSerializer
    permission_classes=[IsAuthenticated,DjangoModelPermissions]   
    def get(self,request):
        product_type_objs= self.get_queryset()
        
         # Apply filtering only if there are query parameters
        if request.query_params:
            product_type_objs = self.filter_queryset(product_type_objs)
        
        #for pagination in custom method
        paginate_data=self.paginate_queryset(product_type_objs)
        serializer=self.get_serializer(paginate_data,many=True)
        response=self.get_paginated_response(serializer.data)
        return Response(response)
    
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
    permission_classes=[IsAuthenticated,DjangoModelPermissions]   
    
    
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
def register_employee(request):
    if request.user.groups.filter(name='Management').exists():
        # Check if the user is in the Management group
        try:
            employee_group=Group.objects.get(name='Employee')
        except:
            return Response('No employee group found!',status=status.HTTP_400_BAD_REQUEST)
        
        password=request.data.get('password')
        hash_password=make_password(password)
        
        data={}
        for key,value in request.data.items():
            data[key]=value
            
        data['password']=hash_password
        data['groups']=[employee_group.id]
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('You are not authorized to register an employee!',status=status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_management(request):
    try:
        management_group=Group.objects.get(name='Management')
    except:
        return Response('No management groups found !',status=status.HTTP_400_BAD_REQUEST)
    
    password=request.data.get('password')
    hash_password=make_password(password)
    
    data={}
    for key,value in request.data.items():   # here copying manually instead of copy() because copy() is deep copying the data. and file cannot be copied.
        data[key]=value
        
    data['password']=hash_password
    data['groups']=[management_group.id ]  #here id must be passed on...serializers takes id in relational field if we're creating data from serializers. 
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
        token,_=Token.objects.get_or_create(user=user)  
        #here instead of _ we can use any variable ..
        # get_or_create gives tuples with two values (Token,bool)
        return Response(token.key,status=status.HTTP_200_OK)
    else:
        return Response('Invalid username or password!',status=status.HTTP_400_BAD_REQUEST)