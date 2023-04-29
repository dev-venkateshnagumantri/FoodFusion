from django.urls import path,include
from . import views

app_name='marketplace'
urlpatterns = [
    path('',views.marketplace,name="marketplace"),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
]