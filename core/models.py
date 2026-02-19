from django.db import models
from django.contrib.auth.models import User


# Create your models here.

ROLE_CHOICES=(
    ('ADMIN', 'Admin'),
    ('SUPPLIER', 'Supplier'),
    ('CUSTOMER', 'Customer'),
    ('DELIVERY', 'Delivery'),
)

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    


class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=220)

    def __str__(self):
        return self.company_name
    


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=225)

    def __str__(self):
        return self.user.username
    

class DeliveryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=50)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


class Product(models.Model):
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('ASSIGNED', 'Assigned'),
        ('ON_THE_WAY', 'On the way'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),

    )

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    delivery_person= models.ForeignKey(DeliveryProfile, on_delete=models.SET_NULL, null=True, related_name='orders')

    title= models.CharField(max_length=200)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name
    


class Delivery(models.Model):
    STATUS_CHOICES = (
        ('ASSIGNED', 'Assigned'),
        ('PICKED', 'Picked Up'),
        ('ONWAY', 'On The Way'),
        ('DELIVERED', 'Delivered'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryProfile, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for the order {self.order.id}"
    


class Payment(models.Model):

    METHOD = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for order {self.order.id}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user.username}"
    


class EmailLog(models.Model):
    
    to_email = models.EmailField()
    subject = models.CharField(max_length=200)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.to_email