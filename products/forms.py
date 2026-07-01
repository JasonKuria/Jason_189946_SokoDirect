# products/forms.py - add these lines

from django.forms import ModelForm
from django import forms
from .models import Product, Review, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'county', 'title', 'description', 'price', 
            'quantity_available', 'unit', 'featured_image', 
            'contact_link', 'farm_link', 'categories'
        ]
    
    def __init__(self, *user_args, **user_kwargs):
        super(ProductForm, self).__init__(*user_args, **user_kwargs)
        
        # 1. Style every input control field uniformly using clean classes
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input-styled-field'})
            
        # 2. Refine the query selection logic: Only show the leaf (deepest) subcategories 
        # so users cannot mistakenly tag a whole generic root tier container.
        self.fields['categories'].queryset = Category.objects.filter(children__isnull=True)
        self.fields['categories'].label = "Select Produce Sub-Categories"

        

class ReviewForm(ModelForm):
    class Meta: # specify which model to use and which fields to include in the form
        model = Review # specify the model to use for this form
        fields = ['value', 'body'] # specify which fields from the model to include in the form, the value field is the rating (up/down) and body is the review text

        label = {
            'value': 'Place your vote',
            'body': 'Add a review with your vote'
        }

    # this function is called to style the form fields when the form is rendered in the template
    # kwargs allows us to pass any number of arguments to the function, 
    # which we then pass to the parent init function
    # args is used to pass any number of positional arguments 
    # to the function, which we also pass to the parent init function
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) # add the CSS class 'input' to each form field for styling purposes

class CategoryManagementForm(forms.ModelForm): # define a form class for managing categories, inheriting from Django's ModelForm
    class Meta:
        model = Category
        fields = ['name', 'parent']
        labels = { # specify the labels for the form fields to make them more user-friendly
            'name': 'New Category / Sub-Category Name', # specfy the subcategory name field label to be more descriptive for the user
            'parent': 'Assign Parent Category (Leave blank if creating a Main Top-Level Category)',
        }

    def __init__(self, *args, **kwargs):
        super(CategoryManagementForm, self).__init__(*args, **kwargs) # call the parent class's __init__ method to initialize the form with any arguments passed to it
        # Apply clean, uniform styling to match your marketplace look
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input-styled-field'})
        
        # Display the choice list using the clean ancestral paths from your __str__ method
        self.fields['parent'].queryset = Category.objects.all().order_by('name')
        self.fields['parent'].empty_label = "--- No Parent (Root Category Tier) ---"