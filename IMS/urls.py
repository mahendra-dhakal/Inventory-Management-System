"""
URL configuration for IMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from base.views import ProductApiView,ProductTypeApiView,ProductTypeDetailApiView,register_employee,login,register_management

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/',ProductApiView.as_view({'get':'list','post':'create'})),
    path('product/<int:pk>/',ProductApiView.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    path('product-type/',ProductTypeApiView.as_view()),
    path('product-type/<int:pk>/',ProductTypeDetailApiView.as_view()),
    path('register-employee/',register_employee,name='register-employee'),
    path('register-management/',register_management,name='register-management'),
    path('login/',login,name='login')
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
