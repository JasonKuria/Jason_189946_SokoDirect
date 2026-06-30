from django.contrib import admin

# Register your models here.

from .models import Product, Review, Category, County, Speciality
 
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(County)
admin.site.register(Speciality)
