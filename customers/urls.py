from django.urls import path,include,reverse
from accounts import views as AccountViews
from . import views

app_name = 'customers'
urlpatterns = [
    path('',AccountViews.customerDashboard,name="customers"),
    path('profile/', views.profile, name='profile'),
]
