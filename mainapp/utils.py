import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id':product.id,
                'product':{
                    'id':product.id,
                    'product_name':product.product_name,
                    'price':product.price,
                    'product_img':product.product_img
                },
                'quantity':cart[i]['quantity'],
                'digital':product.digital,
                'get_total':total,
            }
            items.append(item)

        except:
            pass
    return {'cartItems':cartItems ,'order':order, 'items':items}


def cartData(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    return {'cartItems':cartItems ,'order':order, 'items':items}
