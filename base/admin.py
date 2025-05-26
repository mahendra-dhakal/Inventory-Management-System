from django.contrib import admin
from .models import User,Product,ProductType,Department
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Department)