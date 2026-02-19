from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsDelivery, IsCustomer, IsSupplier
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .services import create_notification, send_email_and_log
from django.db.models import Sum, Count



from .models import Product, SupplierProfile,CustomerProfile,DeliveryProfile, UserRole,User, Order, Notification, OrderItem
from .serializers import ProductSerializer, RegisterSerializer, LoginSerializer, OrderSerializer, OrderCreateSerializer, NotificationSerializer



class TestAPI(APIView):
    def get(self, request):
        return Response({"msg": "api alive"})



class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    

class ProductListAPI(APIView):

    def get(self, request):

        products = Product.objects.filter(
            approved=True
        ).select_related('category', 'supplier')

        search = request.query_params.get('search')
        if search:
            products = products.filter(
                name__icontains=search.strip()
            )

        category = request.query_params.get('category')
        if category:
            products = products.filter(
                category__name__iexact=category.strip()
            )

        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        try:
            if min_price:
                products = products.filter(price__gte=float(min_price))
            if max_price:
                products = products.filter(price__lte=float(max_price))
        except ValueError:
            return Response({"error": "Invalid price format"}, status=400)

        order = request.query_params.get('order')
        if order == 'price_low':
            products = products.order_by('price')
        elif order == 'price_high':
            products = products.order_by('-price')
        elif order == 'new':
            products = products.order_by('-created_at')

        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(products, request)

        if result_page is not None:
            serializer = ProductSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


        

    

class SupplierProductCreateAPI(APIView):
    """
    Supplier can add products.
    Product is saved as unapproved by default.
    only suoolier can hit api 
    """
    permission_classes = [IsSupplier]

    def post(self, request):
        supplier = SupplierProfile.objects.get(user=request.user)

        data = request.data.copy()
        data['supplier'] = supplier.id

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save(approved=False)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
class SupplierProductListAPI(APIView):
    permission_classes = [IsSupplier]

    def get(self, request):
        products = Product.objects.filter(supplier=request.user)

        # Search
        search = request.GET.get('search')
        if search:
            products = products.filter(name__icontains=search)

        # Price filter
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price:
            products = products.filter(price__gte=min_price)

        if max_price:
            products = products.filter(price__lte=max_price)

        # Approval filter
        approved = request.GET.get('approved')
        if approved is not None:
            if approved.lower() == 'true':
                products = products.filter(approved=True)
            elif approved.lower() == 'false':
                products = products.filter(approved=False)

        # Ordering
        order = request.GET.get('order')
        if order == 'price_low':
            products = products.order_by('price')
        elif order == 'price_high':
            products = products.order_by('-price')
        elif order == 'new':
            products = products.order_by('-created_at')

        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(products, request)

        if result_page is not None:
            serializer = ProductSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class RegisterAPI(APIView):

    def post(self, request):

        data= request.data
        username =data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({
                "error": "Username already taken"
            })
        
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)

            return Response({
                "message": "User Registered Successfully"
            }, status=201)
        return Response(serializer.errors, status=400)
    


class LoginAPI(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username= serializer.validated_data['username'],
            password= serializer.validated_data['password']
        )
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username
        })
    


class CustomerOrderListAPI(ListAPIView):

    serializer_class=OrderSerializer
    permission_classes= [IsCustomer]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)
    

class AdminOrderListAPI(ListAPIView):

    serializer_class=OrderSerializer
    permission_classes=[IsAdmin]

    def get_queryset(self):
        return Order.objects.all()
    
    
class SupplierOrderListAPI(ListAPIView):

    serializer_class=OrderSerializer
    permission_classes=[IsSupplier]

    def get_queryset(self):
        return Order.objects.filter(
            items__product__supplier__user=self.request.user
        ).distinct()
    

class DeliveryOrderListAPI(ListAPIView):

    serializer_class=OrderSerializer
    permission_classes=[IsDelivery]

    def get_queryset(self):
        return Order.objects.filter(
            delivery_person__user=self.request.user
        )



class OrderCreateAPI(APIView):

    permission_classes= [IsCustomer]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_profile= CustomerProfile.objects.get(user=request.user)
        
        order= serializer.save(customer=customer_profile)
               

        return Response(OrderSerializer(order).data, status=201)
    
    


class OrderDetailAPI(APIView):
    """
    Admin can view any order
    Customer can view own order only
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        role = request.user.role.role

        if role == "ADMIN":
            order = Order.objects.get(id=id)

        elif role == "CUSTOMER":
            customer = CustomerProfile.objects.get(user=request.user)
            order = Order.objects.get(id=id, customer=customer)

        else:
            return Response({"error": "Access denied"}, status=403)

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class AdminPendingProductListAPI(APIView):

    permission_classes=[IsAdmin]

    def get(self,request):
        
        pendingproducts= Product.objects.filter(approved=False)
       
        serializer= ProductSerializer(pendingproducts, many=True)
        return Response(serializer.data)
    


class AdminProductApproveAPI(APIView):

    permission_classes=[IsAdmin]

    def patch(self,request,pk):
       
        product = Product.objects.get(id=pk)
        product.approved=True
        product.save()

        return Response({"msg":"Product approved Successfully."})
    

# admin order adccept api 

class AdminOrderAcceptAPI(APIView):

    permission_classes=[IsAdmin]    #only admin can change order status

    def post(self, request, id):
        try: 
            order= Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        
        if order.status !='PENDING':
            return Response({"error": "Order already processed"}, status=400)
        
        order.status= "ACCEPTED" # change order status
        order.save()

        #notification for customer
        create_notification(
            order.customer.user, f"Your order '{order.title}' (Order #{order.id}) has been accepted."
        )

        # email 
        send_email_and_log(
            "Order Accepted",
            f"Your order '{order.title}' (Order #{order.id}) has been accepted.",
            order.customer.user.email
        )

        return Response({"message": "Order accepted successfully"})
    

# admin assign delivery api 

class AdminAssignDeliveryAPI(APIView):

    permission_classes = [IsAdmin]

    def post(self, request, id):
        delivery_id = request.data.get('delivery_person_id')

        try:
            order = Order.objects.get(id=id)
            delivery_person = DeliveryProfile.objects.get(id=delivery_id)
        except:
            return Response({"error": "Invalid order or delivery person"}, status=400)

        if order.status != 'ACCEPTED':   # Keep status consistent
            return Response({"error": "Order must be accepted first"}, status=400)

        order.delivery_person = delivery_person
        order.status = "ASSIGNED"
        order.save()

        # Notification for delivery person
        create_notification(
            delivery_person.user,
            f"You have been assigned order '{order.title}' (#{order.id})"
        )

        #  Email to customer
        send_email_and_log(
            "Order Assigned for Delivery",
            f"Your order '{order.title}' (Order #{order.id}) has been assigned for delivery.",
            order.customer.user.email
        )

        #  Email to delivery person
        send_email_and_log(
            "New Delivery Assignment",
            f"You have been assigned order '{order.title}' (Order #{order.id}).",
            delivery_person.user.email
        )

        return Response({"message": "Delivery person assigned successfully"})



class DeliveryOrderStatusUpdateAPI(APIView):

    permission_classes = [IsDelivery]

    def post(self, request, id):

        status_value = request.data.get("status")

        try:
            order = Order.objects.get(
                id=id,
                delivery_person__user=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or not assigned to you"},
                status=404
            )

        # Allowed transitions
        allowed_transitions = {
            "ASSIGNED": "ON_THE_WAY",
            "ON_THE_WAY": "DELIVERED",
        }

        if order.status not in allowed_transitions:
            return Response(
                {"error": "Invalid current order status"},
                status=400
            )

        if status_value != allowed_transitions[order.status]:
            return Response(
                {
                    "error": f"Order can only move to {allowed_transitions[order.status]}"
                },
                status=400
            )

        order.status = status_value
        order.save()

        # Notify customer
        create_notification(
            order.customer.user,
            f"Your order '{order.title}' (Order #{order.id}) status is now {status_value}."
        )

        # Email customer
        send_email_and_log(
            "Order Status Updated",
            f"Your order '{order.title}' (Order #{order.id}) status is now {status_value}.",
            order.customer.user.email
        )

        return Response(
            {"message": "Order status updated successfully"},
            status=200
        )



# get notification 

class NotificationListAPI(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        notifications= Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer= NotificationSerializer(notifications, many=True)

        return Response(serializer.data)



# mark seen 
class NotificationSeenAPI(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, id):
        
        try:
            notification=Notification.objects.get(id=id, user=request.user)

        except Notification.DoesNotExist:
            return Response({"error": "Not fund"}, status=404)
        
        notification.seen= True
        notification.save()

        return Response({"message": "Notification marked as seen"})
    

class AdminAnalyticsAPI(APIView):
    """
    Admin dashboard analytics:
    - total orders
    - order status breakdown
    - total revenue
    - top suppliers
    - recent orders
    """
    permission_classes = [IsAdmin]

    def get(self, request):

        # 1. Total orders
        total_orders = Order.objects.count()

        # 2. Orders by status
        orders_by_status = (
            Order.objects
            .values('status')
            .annotate(count=Count('id'))
        )

        # 3. Total revenue (only delivered orders)
        total_revenue = (
            Order.objects
            .filter(status='DELIVERED')
            .aggregate(total=Sum('total_price'))
            ['total'] or 0
        )

        # 4. Top suppliers (by number of sold items)
        top_suppliers = (
            OrderItem.objects
            .values(
                'product__supplier__id',
                'product__supplier__company_name'
            )
            .annotate(
                total_sold=Sum('quantity'),
                total_earned=Sum('price')
            )
            .order_by('-total_sold')[:5]
        )

        # 5. Recent orders
        recent_orders = Order.objects.order_by('-created_at')[:5]
        recent_orders_data = OrderSerializer(recent_orders, many=True).data

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "orders_by_status": orders_by_status,
            "top_suppliers": top_suppliers,
            "recent_orders": recent_orders_data
        })



