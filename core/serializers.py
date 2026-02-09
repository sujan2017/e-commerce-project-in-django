from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category, Order, OrderItem, SupplierProfile,CustomerProfile,DeliveryProfile,UserRole,Notification
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']    #takes product,price, quantity from db


class OrderSerializer(serializers.ModelSerializer):  #to get details

    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'




class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity= serializers.IntegerField()            #only takes like {"product":1,"quantity":2}
    


class OrderCreateSerializer(serializers.ModelSerializer):

    items = OrderItemCreateSerializer(many= True)

    class Meta:
        model = Order
        fields = ['title', 'description', 'items']

    def create(self, validated_data):
        items_data= validated_data.pop('items')

        customer = validated_data.pop('customer')   #come from apiview

        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                **validated_data
            )
                    
            total = 0

        for item in items_data:
            product = item['product']
            quantity = item['quantity']

            #check stock 
            if product.stock < quantity:
                raise serializers.ValidationError(f"Not Enough Stock for {product.name}. available stock: {product.stock}.")
            
            #reduce stock
            product.stock -=quantity
            product.save()

            #create order item
            OrderItem.objects.create(
                order= order,
                product=product,
                quantity=quantity,
                price = product.price
            )
            total += product.price * quantity
        order.total_price= total
        order.save()

        return order





    
class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    phone = serializers.CharField(required= False)
    address = serializers.CharField(required = False)
    company_name = serializers.CharField(required=False)



    #username check
    
    def validate_username(self, value):
        if User.objects.filter(username= value).exists():
            raise serializers.ValidationError("username alresady taken ")
        return value


    def create(self,data):        

        #create user 

        user= User.objects.create_user(
            username = data['username'],
            password= data['password']
        )

        #create role 

        UserRole.objects.create(
            user =user,
            role = data['role']
            
        )

        #create profile by role 

        role = data['role']

        if role =="CUSTOMER":
            CustomerProfile.objects.create(
                user = user,
                phone = data.get('phone', ''),
                address = data.get('address', '')
                
            )
        elif role == "SUPPLIER":
            SupplierProfile.objects.create(
                user = user,
                phone = data.get('phone', ''),
                address = data.get('address', ''),
                company_name = data.get('company_name', '')

            )
        elif role =="DELIVERY":
            DeliveryProfile.objects.create(
                user= user,
                phone = data.get('phone', ''),
                vehicle_no ="",
                available= True
            )
        return user
    

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notification
        fields='__all__'


# class SupplierRevenueSerializer(serializers.ModelSerializer):
#     total_revenue = serializers.DecimalField(
#         max_digits=12, decimal_places=2
#     )

#     class Meta:
#         model = SupplierProfile
#         fields = ['id', 'company_name', 'total_revenue']
