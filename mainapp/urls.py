from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('category/<str:name>', views.category, name='category'),
    path('cartpage/', views.cart, name='cartpage'),
    path('checkout/', views.checkout, name='checkout'),
    path('PlaceOrder/', views.PlaceOrder, name='PlaceOrder'),

    path('update_item/', views.updateItem, name='update_item'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('product_show/<int:ID>', views.product_show, name='product_show'),
    path('OrderView/', views.OrderView, name='OrderView'),

]
