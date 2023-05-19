from django.shortcuts import render
from vendor.models import Vendor
from orders.models import Order

#GeoDjango
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

from .utils import get_or_set_current_location

def home(request):

    #Near by restaurants
    if get_or_set_current_location(request) is not None:
        pnt = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=600))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
        for v in vendors:
            v.kms = round(v.distance.km, 1)
    else:
        vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    
    #Popularity based restuarants
    arr=[]
    pop_vendors = vendors[:6]
    for vendor in pop_vendors:
        orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')
        orders_count = orders.count()
        arr.append((vendor,orders_count))
    
    arr.sort(key=lambda x:x[1],reverse=True)

    popular_vendors = {}
   
    for item in arr:
        # print("vendor_name=>",item[0]," count=>",item[1])
        popular_vendors[item[0]] = item[1]
 
    context = {
        'vendors': vendors[:4],
        'popular_vendors': popular_vendors,
    }
    return render(request,'home.html',context)

    