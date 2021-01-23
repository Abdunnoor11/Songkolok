from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, SubCategory, Customer
import jinja2
# Create your views here.

def index(request):
    if request.method == 'POST' and 'signup' in request.POST:
        email = request.POST['email']
        password = request.POST['password1'] == request.POST['password2']
        print(request.POST['password1'] == request.POST['password1'])
        if password:
            customer = Customer(email=email, password=request.POST['password1'])
            request.session['email'] = email
            customer.save()
        return redirect('index')

    elif request.method == 'POST' and 'login' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        login = Customer.objects.filter(email=email, password=password)
        if login:
            request.session['email'] = email
            return redirect('index')

    else:
        main_menu = {}
        products = Product.objects.all()
        categories = Category.objects.all()

        for category in categories:
            subcategorys = SubCategory.objects.filter(category=category.id)
            list = []
            for subcategory in subcategorys:
                list.append(subcategory.subcategory_name)
            main_menu[category.category_name] = list

        if request.session.has_key('email'):
            isloggedin = True
        else:
            isloggedin = False
        return render(request, "mainapp/index.html", {
                "products": products,
                "categories": categories,
                "isloggedin": isloggedin,
                "main_menu": main_menu
            }
        )

def category(request, name):
    products = Product.objects.filter(subcategory__subcategory_name=name) | Product.objects.filter(subcategory__category__category_name=name)
    main_menu = {}
    categories = Category.objects.all()
    for categor in categories:
        subcategorys = SubCategory.objects.filter(category=categor.id)
        list = []
        for subcategory in subcategorys:
            list.append(subcategory.subcategory_name)
        main_menu[categor.category_name] = list

    return render(request, "mainapp/category.html", {
            "main_menu": main_menu,
            "products": products,
            "name": name
        })

def product_show(request, ID):
    print(ID)
    return redirect('/')

def logout(request):
    del request.session['email']
    return redirect('/')
