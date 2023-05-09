
#This is utils.py file


def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        long = request.session['long']
        return long, lat
    elif 'lat' and 'long' in request.GET:
        lat = request.GET.get('lat')
        long = request.GET.get('long')
        request.session['lat'] = lat
        request.session['long'] = long
        return long, lat
    else:
        return None