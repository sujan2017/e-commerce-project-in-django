

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import CustomerProfile,SupplierProfile, Product, Category, Order, UserRole


class OrderTest(APITestCase):

    
    # Setup common test data
   
    def setUp(self):

        #Create supplier user
        self.supplier_user = User.objects.create_user(
            username="supplier",
            password="testpass123"
        )

        self.supplier= SupplierProfile.objects.create(
            user=self.supplier_user,
            phone="99999",
            address= "kathmandu",
            company_name= "test company"
        )
        # Create Customer user
        self.user = User.objects.create_user(
            username="customer",
            password="testpass123"
        )

        UserRole.objects.create(
            user=self.user,
            role="CUSTOMER"
        )

        # Create customer profile
        self.customer = CustomerProfile.objects.create(
            user=self.user,
            phone="123456",
            address="Kathmandu"
        )

        # Create category
        self.category = Category.objects.create(
            name="Electronics"
        )

        # Create product with supplier
        self.product = Product.objects.create(
            name="Laptop",
            price=1000,
            stock=10,
            category=self.category,
            supplier = self.supplier
        )

    # Helper method to login and get token
    def get_token(self):
        url = reverse("login")
        response = self.client.post(url, {
            "username": "customer",
            "password": "testpass123"
        })
        return response.data["token"]

   
    # Test 1: Customer can create order successfully
    
    def test_create_order_success(self):

        token = self.get_token()

        # Add authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        url = reverse("create-order")

        data = {
            "title": "Test Order",
            "description": "Test Description",
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 2
                }
            ]
        }

        response = self.client.post(url, data, format="json")

        # Order should be created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        # Stock should reduce (10 - 2 = 8)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

        # Total price should be correct (1000 * 2)
        order = Order.objects.first()
        self.assertEqual(order.total_price, 2000)

    
    # Test 2: Order fails if stock not enough
  
    def test_insufficient_stock(self):

        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        url = reverse("create-order")

        data = {
            "title": "Big Order",
            "description": "Too much quantity",
            "items": [
                {
                    "product": self.product.id,
                    "quantity": 50
                }
            ]
        }

        response = self.client.post(url, data, format="json")

        # Should return validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Order should NOT be created
        self.assertEqual(Order.objects.count(), 0)

   
    # Test 3: Unauthorized user cannot create order
   
    def test_unauthorized_user(self):

        url = reverse("create-order")

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)