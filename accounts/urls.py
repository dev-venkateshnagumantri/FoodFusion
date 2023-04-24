from django.urls import path,include,reverse
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registerUser/',views.registerUser,name="registerUser"),
    path('registerVendor/',views.registerVendor,name="registerVendor"),
    path('login/',views.signin,name="signin"),
    path('logout/',views.signout,name="signout"),
    path('myAccount/',views.myAccount,name="myAccount"),
    path('customerDashboard/',views.customerDashboard,name="customerDashboard"),
    path('vendorDashboard/',views.vendorDashboard,name="vendorDashboard"),

]