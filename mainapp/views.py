from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
import json
from .models import *
import jinja2
# Create your views here.

def index(request):
    if request.method == 'POST' and 'signup' in request.POST:
        email = request.POST['email']
        password = request.POST['password1'] == request.POST['password2']

        if password:
            customer = Customer(email=email, password=request.POST['password1'])
            request.session['email'] = email
            user = User.objects.create_user(username = email, email=email, password=request.POST['password1'])
            user.save();
            customer.save()
            return redirect('index')

    elif request.method == 'POST' and 'login' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        login = Customer.objects.filter(email=email, password=password)
        user = auth.authenticate(username=email, password=password)
        if login and user is not None:
            request.session['email'] = email
            auth.login(request, user)
            return redirect('index')
    else:
        products = Product.objects.all()
        categories = Category.objects.all()

        main_menu = menu()

        if request.session.has_key('email'):
            isloggedin = True
        else:
            isloggedin = False

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']

        return render(request, "mainapp/index.html", {
                "products": products,
                "categories": categories,
                "isloggedin": isloggedin,
                "main_menu": main_menu,
                "cartItems": cartItems
            }
        )

def category(request, name):
    products = Product.objects.filter(subcategory__subcategory_name=name) | Product.objects.filter(subcategory__category__category_name=name)
    main_menu = menu()

    return render(request, "mainapp/category.html", {
            "main_menu": main_menu,
            "products": products,
            "name": name
        })

def product_show(request, ID):
    print(ID)
    return redirect('/')

def cart(request):
    main_menu = menu()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order.get_cart_items


    return render(request, 'mainapp/cartpage.html',{
        'items':items,
        'order': order,
        'main_menu': main_menu,
        'cartItems': cartItems
    })

def checkout(request):
    if request.session.has_key('email'):
        isloggedin = True
        main_menu = menu()
        return render(request, "mainapp/checkout.html",{
                "main_menu": main_menu,
                "isloggedin": isloggedin
            }
        )
    else:
        return redirect('/')

def myprofile(request):
    main_menu = menu()
    return render(request, "mainapp/myprofile.html",{
            "main_menu": main_menu
        }
    )



def logout(request):
    del request.session['email']
    auth.logout(request)
    return redirect('/')

def menu():
    main_menu = {}
    categories = Category.objects.all()
    for categor in categories:
        subcategorys = SubCategory.objects.filter(category=categor.id)
        list = []
        for subcategory in subcategorys:
            list.append(subcategory.subcategory_name)
        main_menu[categor.category_name] = list
    return main_menu




def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
