from django.shortcuts import render , get_object_or_404
from .models import Product

# Create your views here.
def products(request):

    pro = Product.objects.all()
    name = None
    desc = None
    p_from = None
    p_to = None
    cs = None

    if 'CS' in request.GET:
        cs = request.GET['CS']
        if not cs:
            cs = 'off'
    
    if 'search_name' in request.GET or 'search_price_from' in request.GET or 'search_price_to' in request.GET:
        name = request.GET['search_name']
        if name:
            if cs == 'on':
                pro = pro.filter(name__contains=name)
            else:
                pro = pro.filter(name__icontains=name)

    if 'search_desc' in request.GET:
        desc = request.GET['search_desc']
        if desc:
            if cs == 'on':
                pro = pro.filter(desc__contains=desc)
            else:
                pro = pro.filter(desc__icontains=desc)
    
    if 'search_price_from' in request.GET and 'search_price_to' in request.GET:
        p_from = request.GET['search_price_from']
        p_to = request.GET['search_price_to']
        if p_from and p_to:
            if p_from.isdigit() and p_to.isdigit():
                pro = pro.filter( price__gte=p_from , price__lte=p_to )

    context = {
        'product': pro
    }
    return render( request , 'products/products.html', context )

def product(request, pro_id):
    context = {
        'pro': get_object_or_404(Product , pk=pro_id)
    }
    return render( request , 'products/product.html' , context ) 

def search(request):
    return render( request , 'products/search.html' ) 