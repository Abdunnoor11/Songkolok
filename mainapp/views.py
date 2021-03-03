from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


import json
import datetime
from . utils import cookieCart, cartData
from .models import *
import jinja2
# Create your views here.

def index(request):
    if request.method == 'POST' and 'signup' in request.POST:
        email = request.POST['email']
        password = request.POST['password1'] == request.POST['password2']

        if password:
            request.session['email'] = email
            user = User.objects.create_user(username = email, email=email, password=request.POST['password1'])
            customer = Customer(user=user, email=email, password=request.POST['password1'])
            user.save();
            customer.save()
            auth.login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'Password not same.')
            return redirect('index')

    elif request.method == 'POST' and 'login' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        login = Customer.objects.filter(email=email, password=password)
        user = auth.authenticate(username=email, password=password)
        if login and user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, 'Password not matched.')
            return redirect('index')

    else:
        products = Product.objects.all()
        categories = Category.objects.all()

        main_menu = menu()

        posters = Poster.objects.all()

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        return render(request, "mainapp/index.html", {
                "products": products,
                "categories": categories,
                "main_menu": main_menu,
                "cartItems": cartItems,
                "posters":posters
            }
        )

def category(request, name):
    products = Product.objects.filter(subcategory__subcategory_name=name) | Product.objects.filter(subcategory__category__category_name=name)
    main_menu = menu()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, "mainapp/category.html", {
            "main_menu": main_menu,
            "products": products,
            "name": name,
            "cartItems":cartItems
    })

def product_show(request, ID):
    product = Product.objects.get(id=ID)

    data = cartData(request)
    cartItems = data['cartItems']

    main_menu = menu()
    return render(request, "mainapp/product_show.html",{
        "main_menu": main_menu,
        "product":product,
        "cartItems":cartItems
    })


def cart(request):
    main_menu = menu()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, 'mainapp/cartpage.html',{
        'items':items,
        'order': order,
        'main_menu': main_menu,
        'cartItems': cartItems
    })


def checkout(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
    else:
        messages.add_message(request, messages.WARNING, 'Login Please!!!')
        return redirect('cartpage')

    main_menu = menu()
    return render(request, "mainapp/checkout.html",{
            "main_menu": main_menu,
            'items':items,
            'order': order,
            "cartItems": cartItems
        }
    )

def myprofile(request):
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer)        
    else:
        messages.add_message(request, messages.WARNING, 'Login Please!!!')
        return redirect('/')

    main_menu = menu()
    return render(request, "mainapp/myprofile.html",{
            "main_menu": main_menu,
            "cartItems":cartItems,
            "customer":customer,
            "orders":orders
        }
    )


def logout(request):
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


# def updateItem(request):
#     data = json.loads(request.body)
#
#     productId = data['productId']
#     action = data['action']
#
#     print('Action:', action)
#     print('productId:', productId)
#
#
#     device = request.COOKIES['device']
#     customer, created = Customer.objects.get_or_create(device=device)
#
#     product = Product.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
#
#     orderItem.save()
#
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#
#     return JsonResponse('Item was added', safe=False)

def PlaceOrder(request):
    if request.user.is_authenticated:
        name = request.POST['firstname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        transaction_id = datetime.datetime.now().timestamp()

        data = cartData(request)
        order = data['order']
        items = data['items']

        customer = request.user.customer
        order = Order.objects.create(customer=customer, complete=False)
        order.transaction_id = transaction_id

        for item in items:
            product = Product.objects.get(id=item['id'])
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            orderItem.quantity = item['quantity']
            orderItem.save()


        customer.customer_name = name
        customer.phone = phone
        customer.address = address
        customer.save()

        # print(order.shipping)

        if order.get_cart_total:
            order.complete = True
        order.save()

        SA = ShippingAddress(customer=customer, order=order, address=address, city=city)
        SA.save()

    return redirect('Continue')


@staff_member_required
def OrderView(request):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    sa = ShippingAddress.objects.all()

    views = {}
    for order in orders:
        if order.complete == True:
            list = []
            customer = Customer.objects.get(email=order.customer)
            list.append(customer.customer_name)
            list.append(customer.email)
            list.append(customer.phone)
            list.append(order.transaction_id)
            list.append(order.id)
            list.append(order.get_cart_items)
            list.append(order.date_orderd)
            list.append(customer.address)
            views[order] = list

    for i in views:
        print(i)

    return render(request, "mainapp/OrderView.html",{
        "views":views
    })

@staff_member_required
def orderitemview(request, ID):
    order = Order.objects.get(id=ID)
    sa = ShippingAddress.objects.get(order=order)
    items = OrderItem.objects.filter(order=order)

    return render(request, "mainapp/orderitemview.html",{
        "order":order,
        "sa":sa,
        "items":items
    })

def Continue(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    main_menu = menu()

    posters = Poster.objects.all()

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    return render(request, "mainapp/Continue.html", {
            "products": products,
            "categories": categories,
            "main_menu": main_menu,
            "cartItems": cartItems,
            "posters":posters
        }
    )
