from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from accounts.utils import send_notification
from marketplace.context_processors import get_cart_amounts
from django.contrib.auth.decorators import login_required

from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderedFood, Payment
import simplejson as json

from .utils import *
# Create your views here.
@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            #order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() #order.id is generated
            order.order_number = generate_order_number(order.id) #generating order number
            order.save()

            context = {
                'order' : order,
                'cart_items' : cart_items,
            }
            return render(request,'orders/place_order.html',context)
        else:
            print(form.errors)
    else:
        return render(request,'orders/place_order.html')

@login_required
def payment(request):

    #check whether given request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        #store the data in payment model
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        #update the order model
        order.payment = payment
        order.is_ordered = True
        if status=="COMPLETED":
            order.status = "Completed"
        order.save()

        #store the data in orderedfood model 
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            if item.fooditem.vendor.is_open():
                ordered_food = OrderedFood()
                ordered_food.order = order
                ordered_food.payment = payment
                ordered_food.user = request.user
                ordered_food.fooditem = item.fooditem
                ordered_food.quantity = item.quantity
                ordered_food.price = item.fooditem.price
                ordered_food.amount = item.fooditem.price * item.quantity # total amount
                ordered_food.save()

        #send order confirmation email to customer
        mail_subject = 'Thank you for ordering in our website.'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
        }
        send_notification(mail_subject, mail_template, context)
        

        #send order received email to vendors
        mail_subject = 'You have received a new order.'
        mail_template = 'orders/new_order_received.html'
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
        
    
        #clear the cart items
        for item in cart_items:
            if item.fooditem.vendor.is_open():
                item.delete()
        
        #return back to ajax whether status success or failure,incase success return order no. & trans. id
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id,
        }

        return JsonResponse(response)
    
    else:
        return HttpResponse("Ajax Request Failure")

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        tax_data = json.loads(order.tax_data)
        #print(tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        #print(1)
        return render(request,'orders/order_complete.html',context)

    except:
        return redirect('home')
   
