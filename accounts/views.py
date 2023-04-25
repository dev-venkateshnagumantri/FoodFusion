from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from vendor.models import Vendor
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged in !")
        return redirect('accounts:myAccount')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()

            #send verification mail
            send_verification_email(request, user)

            messages.success(request,"Great! You just created your account! check your mail to activate.")
            return redirect('accounts:registerUser')
        else:
            print(form.errors)   
    else:    
        form = UserForm()
    return render(request,'accounts/registerUser.html',{'form':form})

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged in !")
        return redirect('accounts:myAccount')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            #send verification mail
            send_verification_email(request, user)
            
            messages.success(request, 'Your account has been registered sucessfully! Please check your mail and wait for the approval.')
            return redirect('accounts:registerVendor')
        else:
            print(form.errors)
    
    else:
        form = UserForm()
        v_form = VendorForm()
    return render(request,'accounts/registerVendor.html',{'form':form,'v_form':v_form})

def signin(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged in !")
        return redirect('accounts:myAccount')
    elif request.method=='POST':
        email=request.POST['e-mail']
        password=request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            # print('success')
            auth.login(request,user)
            messages.success(request,'You are now Logged in.')
            return redirect('accounts:myAccount')
        else:
            # print('fail')
            messages.error(request,'Invalid Login credentials')
            return redirect('accounts:signin')

    else:
        return render(request,"accounts/signin.html")

@login_required
def signout(request):
    auth.logout(request)
    messages.info(request, 'You are Logged out.')
    return redirect('accounts:signin')
    
@login_required
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request,'accounts/customerDashboard.html')

@login_required
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is now activated.')
        return redirect('accounts:myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:myAccount')



    


    
