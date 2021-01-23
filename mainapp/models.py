from django.db import models


# Create your models here.

class Category(models.Model):
    # category_id = models.IntegerField()
    category_name = models.CharField(max_length=100)
    category_img = models.ImageField(upload_to='pics')

    # def __str__(self):
    #     return self.category_name

class SubCategory(models.Model):
    # subcategory_id = models.IntegerField()
    subcategory_name = models.CharField(max_length=100)
    subcategory_img = models.ImageField(upload_to='pics')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name

class Product(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='pics')
    description = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default = False)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    highlights = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name

class Customer(models.Model):
    customer_name = models.CharField(max_length=100, blank=True, null= True)
    email = models.EmailField(default='DEFAULT VALUE', max_length=70, blank=False, null= True, unique= True)
    password = models.CharField(max_length=50, blank=False)
    customer_img = models.ImageField(upload_to='pics', blank=True, null= True)
    address = models.TextField(blank=True, null= True)
    phone = models.CharField(max_length=15, blank=True, null= True)


class Orders(models.Model):
    pass

class OrderHistory(models.Model):
    pass
