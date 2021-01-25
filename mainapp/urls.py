from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('category/<str:name>', views.category, name='category'),
    path('cartpage/', views.cartpage, name='cartpage'),
    path('checkout/', views.checkout, name='checkout'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('product_show/<int:ID>', views.product_show, name='product_show'),
]
