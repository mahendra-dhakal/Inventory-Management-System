from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product
# Create your views here.

class ProductApiView(ModelViewSet):
    queryset=Product.objects.all()
    