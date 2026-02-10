
# E-Commerce Platform (Django Backend)

A scalable and modular **E-Commerce Platform backend** built with **Python and Django**, designed to support real-world online shopping workflows such as product management, orders, users, and role-based access.

This project is developed as a **backend system** with clean architecture and REST-style APIs.

---

##  Features

- User authentication and role management
- Product and category management
- Order creation and order tracking
- Supplier, customer, and delivery profiles
- RESTful API structure using Django REST Framework
- Centralized business logic in a single core app
- Clean project structure suitable for scaling

---

## Tech Stack

- **Backend:** Python, Django
- **API:** Django REST Framework (DRF)
- **Database:** SQLite (development)
- **Version Control:** Git & GitHub
- **Environment:** Virtualenv

---
## Project Structure

e-commerce-platform/
│
├── core/
│ ├── models.py # All database models (Product, Order, Profiles, etc.)
│ ├── api_views.py # API views and business logic
│ ├── serializers.py # DRF serializers
│ ├── permissions.py # Custom permissions
│ └── urls.py # API routing
│
├── project/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── manage.py
├── db.sqlite3
├── .gitignore
└── README.md




> 🔹 The project uses a **single `core` app** where all main logic (models, APIs, permissions, serializers) is organized for simplicity and maintainability.

---

## Core Modules Explanation

### Products & Categories
- Manage products with pricing and categories
- Structured for easy extension (inventory, discounts, etc.)

### Orders
- Create and manage customer orders
- Track order items and order status

### User Roles
- Different profiles for:
  - Customer
  - Supplier
  - Delivery
- Role-based access using custom permissions

---


##  Project Purpose

This project is built to:

  -Demonstrate real-world Django backend development
  -Showcase clean API design and project structure


## Future Improvements

  -JWT authentication
  -Payment gateway integration
  -Deployment (Docker / AWS / Railway)



## Author

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