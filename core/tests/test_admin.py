from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Order, CustomerProfile, UserRole, DeliveryProfile


class AdminTest(APITestCase):

    def setUp(self):

        # Create Admin
        self.admin = User.objects.create_superuser(
            username="admin",
            password="adminpass"
        )

        UserRole.objects.create(
            user=self.admin,
            role="ADMIN"
        )

        # Create Customer
        self.customer_user = User.objects.create_user(
            username="customer",
            password="testpass123"
        )

        UserRole.objects.create(
            user=self.customer_user,
            role="CUSTOMER"
        )

        self.customer = CustomerProfile.objects.create(
            user=self.customer_user
        )

        # Create Delivery User
        self.delivery_user = User.objects.create_user(
            username="delivery",
            password="deliverypass"
        )

        UserRole.objects.create(
            user=self.delivery_user,
            role="DELIVERY"
        )

        self.delivery_profile = DeliveryProfile.objects.create(
            user=self.delivery_user,
            phone="1234567890",
            vehicle_no="BA-1-PA-1234",
            available=True
        )

        # Create Order (ACCEPTED state)
        self.order = Order.objects.create(
            title="Test Order",
            customer=self.customer,
            status="ACCEPTED"
        )

        # Assign URL
        self.assign_url = reverse("assign-delivery", args=[self.order.id])

    # ✅ TEST 1
    def test_admin_can_assign_delivery(self):

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            self.assign_url,
            {"delivery_person_id": self.delivery_profile.id},
            format="json"
        )

        print(response.data)
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ❌ TEST 2
    def test_non_admin_cannot_assign_delivery(self):

        self.client.force_authenticate(user=self.customer_user)

        response = self.client.post(
            self.assign_url,
            {"delivery_person_id": self.delivery_profile.id},
            format="json"
        )

        print(response.data)
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)