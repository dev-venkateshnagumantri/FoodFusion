from django.shortcuts import render,get_object_or_404,redirect
from accounts.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.utils import send_notification
from marketplace.models import Cart

from orders.models import Order, OrderedFood
import simplejson as json

# Create your views here.
@login_required(login_url='accounts:signin')
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('customers:profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form' : user_form,
        'profile': profile,
    }
    
    return render(request,'customers/cprofile.html',context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request,'customers/my_orders.html',context)


def order_detail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'customers/order_detail.html', context)
    except:
        return redirect('customers:customers')
    
def cancel_order(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        messages.success(request,'Order has been cancelled successfully! Money will be refunded within 24 hours')
        cart_items = Cart.objects.filter(user=request.user)

        #send order cancellation email to customer
        mail_subject = 'Your order is cancelled as per your request.'
        mail_template = 'orders/order_cancelled_by_customer_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
        }
        send_notification(mail_subject, mail_template, context)

        #send order cancelled email to vendors
        mail_subject = 'The order is cancelled. refer to this mail for more details.'
        mail_template = 'orders/order_cancelled.html'
        to_emails = []
        for i in cart_items:
            if i.fooditem.vendor.is_open():
                if i.fooditem.vendor.user.email not in to_emails:
                    #print(i.fooditem.vendor.user.email)
                    to_emails.append(i.fooditem.vendor.user.email)

        context = {
            'order':order,
            'to_email':to_emails,
        }

        send_notification(mail_subject, mail_template, context)
        for food in ordered_food:
            food.delete()
        order.delete()
        return redirect('customers:my_orders')
    except:
        return redirect('customers:customers')