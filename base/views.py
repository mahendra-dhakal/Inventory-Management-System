from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import Product,ProductType
from .serializers import ProductSerializer,ProductTypeSerializer


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
        