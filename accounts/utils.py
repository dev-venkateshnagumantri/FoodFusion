
def detectUser(user):
    redirectUrl = ''
    if user.role == 1:
        redirectUrl = 'accounts:vendorDashboard'
        
    elif user.role == 2:
        redirectUrl = 'accounts:customerDashboard'
        
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin/'
    
    return redirectUrl