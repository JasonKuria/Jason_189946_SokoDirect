# SokoDirect
### A Farm-to-Buyer Agricultural Marketplace Built with Django

# Project Overview

SokoDirect is a web-based agricultural marketplace that connects farmers directly with buyers without requiring intermediaries. The platform enables farmers to advertise agricultural produce while allowing buyers to browse products, communicate with farmers, leave reviews, and place orders through an intuitive online marketplace.

The system was developed using the Django web framework following the Model-View-Template (MVT) architecture.


# Problem Statement

Small-scale farmers often struggle to reach customers because they depend on brokers and middlemen who significantly reduce their profits. Buyers also face difficulties locating trustworthy farmers who offer fresh produce at fair prices.

SokoDirect addresses these challenges by providing a centralized online marketplace where farmers can directly market their products and buyers can purchase fresh agricultural produce conveniently.



# Objectives

## Main Objective

To develop an online agricultural marketplace that facilitates direct interaction between farmers and buyers.

## Specific Objectives

- Allow farmers to create accounts and manage product listings.
- Allow buyers to browse agricultural products.
- Enable secure user authentication.
- Provide product categorization and search functionality.
- Allow customers to review agricultural products.
- Provide shopping cart and checkout functionality.
- Support messaging between buyers and farmers.
- Build a scalable marketplace using Django.



# Features

### User Management

- User Registration
- Login & Logout
- Farmer Profiles
- Buyer Profiles
- Profile Editing

### Product Management

- Add Products
- Edit Products
- Delete Products
- Upload Product Images
- Product Categories
- County-based Listings

### Marketplace

- Browse Products
- Search Products
- Product Details
- Product Reviews
- Product Ratings

### Shopping

- Shopping Cart
- Guest Cart Support
- Checkout System
- Shipping Address Management
- Order History

### Communication

- Buyer-Farmer Messaging
- Inbox System

### Administration

- Django Admin Dashboard
- Product Management
- User Management
- Category Management
- County Management

---

# Technologies Used

## Backend

- Python 3
- Django 5.x
- Django ORM
- Django REST Framework
- Simple JWT Authentication

## Frontend

- HTML5
- CSS3
- JavaScript
- UIkit CSS Framework

## Database

- SQLite (Development)

## Image Handling

- Pillow

## Version Control

- Git
- GitHub



# Installation Guide

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SokoDirect.git
```

```bash
cd SokoDirect
```



## 2. Create Virtual Environment

Windows

```bash
python -m venv EnvSoko
```

Activate

```bash
EnvSoko\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv EnvSoko
source EnvSoko/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

or manually

```bash
pip install django
pip install pillow
pip install djangorestframework
pip install djangorestframework-simplejwt
```

---

## 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 6. Run Development Server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

---

# Setup Instructions

### Populate Sample Data (Optional)

Run the provided scripts in the following order:

```bash
python populate_all_counties.py

python populate_categories.py

python populate_profiles.py

python populate_specialities.py

python populate_products.py

python populate_reviews.py
```

---

### Static Files

Ensure:

```
STATIC_URL
STATICFILES_DIRS
MEDIA_URL
MEDIA_ROOT
```

are correctly configured inside

```
settings.py
```

---

# Usage Instructions

## Farmer

- Register/Login
- Complete profile
- Create product listings
- Upload product images
- Manage products
- View orders
- Respond to buyer messages

---

## Buyer

- Browse marketplace
- Search products
- View farmer profiles
- Add items to cart
- Checkout
- Leave reviews
- Message farmers

---

## Administrator

Access

```
http://127.0.0.1:8000/admin
```

Manage

- Users
- Products
- Categories
- Counties
- Orders
- Reviews

---

# Sample Screenshots

> Replace the placeholders below with screenshots from your project.

## Homepage

```
docs/screenshots/homepage.png
```

---

## Product Listing

```
docs/screenshots/products.png
```

---

## Product Details

```
docs/screenshots/product-details.png
```

---

## Farmer Dashboard

```
docs/screenshots/dashboard.png
```

---

## Shopping Cart

```
docs/screenshots/cart.png
```

---

## Django Admin

```
docs/screenshots/admin.png
```

---

# Folder Structure

```
SokoDirect/
│
├── products/
│   ├── templates/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── utils.py
│
├── users/
│   ├── templates/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── orders/
│   ├── templates/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── utils.py
│
├── static/
│
├── media/
│
├── templates/
│   ├── main.html
│   ├── navbar.html
│   ├── footer.html
│   └── pagination.html
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# API Documentation

The project includes Django REST Framework support for future API integration.

Example endpoints include:

| Endpoint | Method | Description |
|-----------|----------|-------------|
| `/api/products/` | GET | Retrieve products |
| `/api/products/<id>/` | GET | Product details |
| `/api/users/login/` | POST | User authentication |
| `/api/token/` | POST | JWT token generation |
| `/api/orders/` | GET | User orders |

Authentication is handled using **JSON Web Tokens (JWT)**.

---

# Known Limitations

- SQLite is intended only for development.
- Online payment gateways (Mpesa/Card) are not yet integrated.
- Email verification has not been implemented.
- Push notifications are not available.
- Product recommendations are not AI-powered.
- Live chat functionality is not yet implemented.
- Production deployment configuration is pending.

---

# Future Improvements

- Mpesa Integration
- AI Product Recommendations
- Mobile Application
- SMS Notifications
- Email Verification
- Product Analytics Dashboard
- Farmer Verification System
- Payment Gateway Integration
- Cloud Deployment (AWS/Azure)

---

# Contributors

**Jason Kuria**

Bachelor of Science in Informatics and Computer Science

Project Developer

GitHub:
https://github.com/JasonKuria

---

# License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Jason Kuria

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software
and associated documentation files to deal in
the Software without restriction...
```

---

# Acknowledgements

Special thanks to:

- Django Software Foundation
- Python Software Foundation
- UIkit Framework
- Open Source Community

---

## ⭐ If you find this project useful, consider giving it a star on GitHub!
