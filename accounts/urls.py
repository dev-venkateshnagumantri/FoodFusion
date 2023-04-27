from django.urls import path,include,reverse
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',views.myAccount,name="myAccount"),
    path('registerUser/',views.registerUser,name="registerUser"),
    path('registerVendor/',views.registerVendor,name="registerVendor"),
    path('login/',views.signin,name="signin"),
    path('logout/',views.signout,name="signout"),
    path('myAccount/',views.myAccount,name="myAccount"),
    path('customerDashboard/',views.customerDashboard,name="customerDashboard"),
    path('vendorDashboard/',views.vendorDashboard,name="vendorDashboard"),
    path('activate/<uidb64>/<token>/', views.activate,name="activate"),
    path('vendor/', include('vendor.urls')),

]