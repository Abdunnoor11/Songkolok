from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('category/<str:name>', views.category, name='category'),
    path('product_show/<int:ID>', views.product_show, name='product_show'),
]
