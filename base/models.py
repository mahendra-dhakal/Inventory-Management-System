from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
#user: username,password,email,image,address,contact number
class User(AbstractUser):
    username=models.CharField(max_length=100, unique=True)
    password=models.CharField(max_length=100,)
    email=models.EmailField()
    image=models.FileField()
    address=models.TextField()
    contact_no=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class ProductType(models.Model):
    name=models.CharField(max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name=models.CharField(max_length=300)
    floor=models.CharField(max_length=300)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name=models.CharField(max_length=300)
    description=models.TextField()
    stock=models.IntegerField()
    type=models.ForeignKey(ProductType,on_delete=models.SET_NULL,null=True)
    department=models.ManyToManyField(Department,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    
class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    vendor=models.ForeignKey('Vendor',on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Purchase of {self.quantity} {self.product}"

class Sell(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    customer_name=models.CharField(max_length=300)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sell of {self.quantity} {self.product}"
   
class Vendor(models.Model):
    name=models.CharField(max_length=300)
    address=models.CharField(max_length=300)
    contact=models.CharField(max_length=300)
    email=models.EmailField(blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


    


