from datetime import datetime
from django.db import models

from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
import simplejson as json

#time related operations
import pytz

# Create your models here.

request_object = ''
class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal', 'PayPal'),
        ('RazorPay', 'RazorPay'), # Only for Indian Students.
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",null=True)
    total_data = models.JSONField(blank=True, null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])
    
    def get_ist_time(self):
        order = Order.objects.get(pk=self.pk)     
        # print(order)
        # Get the order's created_at datetime in UTC
        created_at_utc = order.created_at.replace(tzinfo=pytz.UTC)
        # print(created_at_utc)
        # Convert the UTC datetime to IST
        ist_tz = pytz.timezone('Asia/Kolkata')
        created_at_ist = created_at_utc.astimezone(ist_tz)
        # print(created_at_ist)

        # Remove the timezone offset
        created_at_without_offset = created_at_ist.replace(tzinfo=None)
        return created_at_without_offset
    
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        subtotal = 0
        tax = 0
        tax_dict = {}
        if self.total_data:
            total_data = json.loads(self.total_data)
            #print(total_data)
            data = total_data.get(str(vendor.id))
            
            
            for key, val in data.items():
                subtotal += float(key)
                val = val.replace("'", '"')
                val = json.loads(val)
                tax_dict.update(val)

                # calculate tax
                # {'CGST': {'9.00': '6.03'}, 'SGST': {'7.00': '4.69'}}
                for i in val:
                    for j in val[i]:
                        tax += float(val[i][j])
        
        grand_total = float(subtotal) + float(tax)
        #print("grand_total =>",grand_total)
        context = {
            'subtotal': subtotal,
            'tax_dict': tax_dict, 
            'grand_total': grand_total,
        }
        return context
    
    def is_cancelable(self):
        order = Order.objects.get(pk=self.pk)     
        # print(order)
        # Get the order's created_at datetime in UTC
        created_at_utc = order.created_at.replace(tzinfo=pytz.UTC)

        # Convert the UTC datetime to IST
        ist_tz = pytz.timezone('Asia/Kolkata')
        created_at_ist = created_at_utc.astimezone(ist_tz)

        # Remove the timezone offset
        created_at_without_offset = created_at_ist.replace(tzinfo=None)


        ordered_time = created_at_without_offset
        present_time = datetime.now()
        # print("Ordered Time:", created_at_without_offset)
        # print("Present Time:", present_time)
        timediff = present_time - ordered_time
        # print("Time Difference:", timediff)
        tsecs = timediff.total_seconds()
        tmins = tsecs/60
        # print("Time Difference in Minutes:", tmins)
        cancel = None
        if tmins>0 and tmins<10:
            cancel = True
        else:
            cancel = False
        # print("Cancel Decision:", cancel)
        return cancel

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title