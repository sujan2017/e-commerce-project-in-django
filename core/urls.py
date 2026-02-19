from django.urls import path
from .api_views import (
    TestAPI,
    ProductListAPI,
    SupplierProductCreateAPI,
    RegisterAPI,
    LoginAPI,

    
    OrderCreateAPI,
    OrderDetailAPI,

    AdminOrderListAPI,
    CustomerOrderListAPI,
    SupplierOrderListAPI,
    DeliveryOrderListAPI,
    
    AdminPendingProductListAPI,
    AdminProductApproveAPI,
    AdminAnalyticsAPI,

    AdminOrderAcceptAPI,
    AdminAssignDeliveryAPI,
    DeliveryOrderStatusUpdateAPI,

    NotificationListAPI,
    NotificationSeenAPI,

    SupplierProductListAPI,

    CancelOrderAPI,
)


urlpatterns = [

    # Test
    path('test/', TestAPI.as_view()),

    # Auth
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),

    # Products
    path('products/', ProductListAPI.as_view(), name='product-list'),   # all approved products
                                           
    path('supplier/products/add/', SupplierProductCreateAPI.as_view()),
    path('supplier/orders/', SupplierOrderListAPI.as_view()),

    # Orders (Customer)
    path('orders/', CustomerOrderListAPI.as_view()),                           # view own orders
    path('orders/create/', OrderCreateAPI.as_view()),                  # create order
    path('orders/<int:id>/', OrderDetailAPI.as_view()),                # order detail

    # Admin – Product Approval
    path('admin/products/pending/', AdminPendingProductListAPI.as_view()),
    path('admin/products/<int:pk>/approve/', AdminProductApproveAPI.as_view()),

    # Admin – Order Management
    path('admin/orders/<int:id>/accept/', AdminOrderAcceptAPI.as_view()),
    path('admin/orders/<int:id>/assign-delivery/', AdminAssignDeliveryAPI.as_view()),
    path('admin/orders/', AdminOrderListAPI.as_view()),

    # Delivery
    path('delivery/orders/<int:id>/status/', DeliveryOrderStatusUpdateAPI.as_view()),
    path('delivery/orders/', DeliveryOrderListAPI.as_view()),

    # Notifications
    path('notifications/', NotificationListAPI.as_view()),
    path('notifications/<int:id>/seen/', NotificationSeenAPI.as_view()),

    # Admin Analytic
    path('admin/analytics/', AdminAnalyticsAPI.as_view()),

    path('supplier/products/', SupplierProductListAPI.as_view()),

    path('customer/order/<int:id>/cancel/', CancelOrderAPI.as_view()),
    

    
]

    




    


    
    

