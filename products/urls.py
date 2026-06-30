from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product/<str:pk>/', views.single_product, name='single-product'),

    # New — form page for adding a produce listing
    path('create-product/', views.create_product, name='create-product'),

    # Update needs the product ID in the URL so we know which to edit
    path('update-product/<str:pk>/', views.update_product, name='update-product'),

    # Delete also needs the product ID so we know which to delete
    path('delete-product/<str:pk>/', views.delete_product, name='delete-product'),

    # category management page for adding and managing categories and subcategories
    # This is a new view that allows users to manage categories and subcategories
    # It is a new view that allows users to manage categories and subcategories
    path('manage-categories/', views.manage_categories, name='manage-categories'),

]
