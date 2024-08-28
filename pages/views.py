from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
#from mycoffe.settings import LANGUAGE_CODE

# Create your views here.

def index(request):
    context = {
        'product': Product.objects.all()
    }
    return render( request , 'pages/index.html' , context )

def about(request):
    return render( request , 'pages/about.html' )

def coffee(request):
    return render( request , 'pages/coffee.html' )

# def navbar(request):
#     context = None
#     title = None
#     home = None
#     welcome = None
#     join_us = None
#     profile = None
#     favorites = None
#     my_card = None
#     my_orders = None
#     logout = None

#     if 'en-us' in LANGUAGE_CODE:
#         context = {
#             'title': 'My Coffee',
#             'home': 'Home',
#             'welcome': 'Welcome',
#             'join_us': 'Join us',
#             'profile': 'Profile',
#             'favorites': 'Favorites',
#             'my_card': 'My Card',
#             'my_orders': 'My Orders',
#             'logout': 'Logout'
#         }
#     else:
#         context = {
#             'title': 'قهوتي',
#             'home': 'الرئيسيه',
#             'welcome': 'مرحباً',
#             'join_us': 'إنضم لنا',
#             'profile': 'الملف الشخصي',
#             'favorites': 'المفضلات',
#             'my_card': 'السله',
#             'my_orders': 'الطلبات',
#             'logout': 'تسجيل الخروج'
#         }

#     return render( request , 'partials/_navbar.html', context )