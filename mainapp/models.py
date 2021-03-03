from multiselectfield import MultiSelectField
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poster(models.Model):
    img = models.ImageField(upload_to='poster')

class Category(models.Model):
    # category_id = models.IntegerField()
    category_name = models.CharField(max_length=100)
    category_img = models.ImageField(upload_to='pics', null=True, blank=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    # subcategory_id = models.IntegerField()
    subcategory_name = models.CharField(max_length=100)
    subcategory_img = models.ImageField(upload_to='pics')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name

class Product(models.Model):
    CHOOSE_SIZE = (
        ('Extra Small', 'XS'),
        ('Small', 'S'),
        ('Medium', 'M'),
        ('Large', 'L'),
        ('Extra Large', 'XL'),
        ('Double Large', 'XXL'),
        ('Triple Large', 'XXXL'),
    )

    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='pics')
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    offer = models.BooleanField(default = False)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    size = MultiSelectField(choices=CHOOSE_SIZE)
    highlights = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.product_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(default='DEFAULT VALUE', max_length=100, blank=True, null=True)
    email = models.EmailField(default='', max_length=70, blank=True, null= True, unique= True)
    password = models.CharField(max_length=50, blank=True, null=True)
    customer_img = models.ImageField(upload_to='pics', blank=True, null= True)
    address = models.TextField(blank=True, null= True)
    phone = models.CharField(max_length=15, blank=True, null= True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.email


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)    

    def __str__(self):
        return str(self.id)

    @property
    def shipping():
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total + 50

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
