
# E-Commerce Platform (Django REST Framework)

A role-based E-Commerce backend system built using Django 6, Django REST Framework, and WebSocket (Django Channels).

This project supports Admin, Supplier, Customer, and Delivery roles with advanced order management, filtering, analytics, and real-time notifications.

---

## 🚀 Features

### 🔐 Authentication
- JWT Authentication (SimpleJWT)
- Role-based permissions (Admin, Supplier, Customer, Delivery)

### 🛍 Product Management
- Supplier can create/update/delete products
- Admin approval system
- Product search & filtering
- Price range filtering
- Category filtering
- Sorting (price low/high, newest)
- Pagination

### 📦 Order Management
- Customers can place orders
- Admin can accept orders
- Admin assigns delivery person
- Delivery availability tracking
- Order status control system

### 📊 Admin Analytics
- Order statistics
- Revenue tracking
- Product approval monitoring

### 🔔 Notifications
- Database notifications
- Real-time WebSocket notifications (Django Channels)

### 📧 Email System
- Order confirmation emails
- Delivery assignment emails

### 📘 API Documentation
- Swagger UI available via drf-spectacular

---

## 🛠 Tech Stack

- Python 3.13
- Django 6
- Django REST Framework
- Django Channels (WebSocket)
- JWT Authentication (SimpleJWT)
- drf-spectacular (OpenAPI Documentation)
- SQLite (Development)

---

## ⚙ Installation Guide

### 1️⃣ Clone Repository
git clone https://github.com/sujan2017/e-commerce-project-in-django.git



### 2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Apply Migrations
python manage.py migrate

### 4️⃣ Create Superuser
python manage.py createsuperuser

### 5️⃣ Run Server
python manage.py runserver



## 📘 API Documentation

Swagger UI available at: http://127.0.0.1:8000/api/docs/

Open API Schema: http://127.0.0.1:8000/api/schema/


## 🔔 WebSocket Endpoint
ws://127.0.0.1:8000/ws/notifications/




Sujan Thapa
Python & Django Backend Developer
GitHub: https://github.com/sujan2017




admin1 ef0bb86ad840a2381476a7535f59e98243e95a89


supplier1 register
{
  "username": "supplier1",
  "password": "123456",
  "role": "SUPPLIER",
  "phone": "980000001",
  "address": "Kathmandu",
  "company_name": "Sujan Traders"
}Token 78aa70263dab3654bd2dd56758487ed62445fd5b

supplier2 
{
  "username": "supplier2",
  "password": "123456",
  "role": "SUPPLIER",
  "phone": "980000002",
  "address": "Pokhara",
  "company_name": "Himal Suppliers"
}a10ab4cb58a263cc01a7b91b06928d64d1e685af


customer1
{
  "username": "customer1",
  "password": "123456",
  "role": "CUSTOMER",
  "phone": "981111111",
  "address": "Lalitpur"
}a292b7687b024c72b28feda50caf4dea7c072dda

customer2
{
  "username": "customer2",
  "password": "123456",
  "role": "CUSTOMER",
  "phone": "982222222",
  "address": "Bhaktapur"
}f15f7255889d3f1879ef50588dcae582f0c28122



add product 

{
  "name": "iPhone 15",
  "description": "Apple phone",
  "price": 80000,
  "stock": 20,
  "category": "phone"
}