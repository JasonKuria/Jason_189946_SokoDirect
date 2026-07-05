from django.db import models

# Create your models here.
from django.contrib.auth.models import User # Using Django's built-in User model for authentication and user management
from products.models import Product  # Importing your existing farmer product model


class Order(models.Model): 
    # If user is logged in, bind profile. If anonymous/guest, keep null.
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Order No: {self.id} — Status Completed: {self.complete}"

    # The Order model will also have methods to calculate the total cost of the order and the total number of items in the order,
   
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        # Force conversion to float during summation loop to protect memory constraints
        total = sum([float(item.get_total) for item in orderitems])
        return total

    # The get_cart_items method will iterate through all the OrderItem instances related to the Order and sum up the total quantity of 
    # items in the cart. This will be useful for displaying the number of items in the cart icon on the website and for providing a 
    # summary of the order to the user.
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([int(item.quantity) for item in orderitems])
        return total
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This prevents the database from ever allowing a duplicate
        unique_together = ('order', 'product')    

    @property
    def get_total(self):
        # Explicit conversion to float/int before math operations prevents string errors
        price = float(self.product.price) if self.product and self.product.price else 0.0
        qty = int(self.quantity) if self.quantity else 0
        return price * qty

# The ShippingAddress model will represent the shipping details for an order, including the customer's address, city, county, and phone number.
# This model will have a foreign key relationship with the Order model and will be used to store the shipping information for each order.
# The ShippingAddress model will be a child to the Order model and will contain fields for the address, city, county, and phone number, 
# which are essential for processing the order and ensuring that it is delivered to the correct location. 

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False) # e.g., Nairobi, Nyeri, Nakuru
    county = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True) # Essential for M-Pesa/Logistics
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}, {self.city}"
