

# Create your views here.
# products/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm, ReviewForm, CategoryManagementForm
from .utils import searchProducts, paginateProducts

#from orders.models import Order   # Import your new e-commerce order model
#from orders.utils import cartData          # Import your new e-commerce utility function for cart data
#from orders.utils import cartData  # Ensure your cart utility is imported

def products(request):
    products, search_query = searchProducts(request) 
    products, custom_range = paginateProducts(request, products, 3) 

    # --- FIXED E-COMMERCE INTEGRATION ---
    # Call cartData utility to seamlessly parse logged-in OR guest cart states
    # 1. Fetch the cookie data total and item count for navbar badge display
    #data = cartData(request)
    #cart_items_count = data['cartItems']
    #
    #order = data['order']

    #categories = Category.objects.all().order_by('name')

    # Only fetch ROOT categories (parent=None) — children load via parent.children.all in template
    #categories = Category.objects.filter(parent=None).order_by('name').prefetch_related(
    #    'children__children'  # prefetch 2 levels deep in one query (efficient)
    #)

    # Fetch ALL root parent categories (parent=None) — no limit, ordered alphabetically
    # prefetch_related loads children + grandchildren in just 2 extra DB queries (very efficient)
    #categories = Category.objects.filter(
    #    parent=None
    #).order_by('name').prefetch_related(
    #    'children',           # level 2
    #    'children__children'  # level 3
    #)    

    category_id = request.GET.get('category_id', '')
 
    categories = Category.objects.filter(
        parent=None
    ).order_by('name').prefetch_related(
        'children',
        'children__children'
    )    

    # Work out which parent panel to auto-open when a child/grandchild is active
    # Work out which parent accordion to auto-open when a child is the active filter
    active_parent_id = None
    if search_query:
        matched = Category.objects.filter(name__iexact=search_query).first()
        if matched:
            if matched.parent is None:
                active_parent_id = None
            elif matched.parent.parent is None:
                active_parent_id = str(matched.parent.id)
            else:
                active_parent_id = str(matched.parent.parent.id)
 
    context = {
        'products':         products,
        'search_query':     search_query,
        'custom_range':     custom_range,
        'categories':       categories,
        'active_parent_id': active_parent_id,
        'category_id':      category_id,      # ← new: passed to template for active state
    }

    return render(request, 'products/products.html', context)

def single_product(request, pk):
    productObj = Product.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = productObj
            review.owner = request.user.profile
            review.save()
            productObj.getVoteCount

            messages.success(request, 'Your review was submitted successfully!')
            return redirect('single-product', pk=productObj.id)
        
    # --- FIXED E-COMMERCE INTEGRATION ---
    # Dynamically tracking user vs guest sessions for detail layout display metrics
    #data = cartData(request)
    #cart_items_count = data['cartItems']

    #order = data['order']

    context = {
        'product': productObj, 
        #'cartItems': cart_items_count, # <--- Add this line!        
        'form': form,
        #'order': order
    }        
    return render(request, 'products/single-product.html', context)

@login_required(login_url='login')
def create_product(request):
    profile = request.user.profile 
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = profile  
            product.save() # Saves core instance
            
            form.save_m2m() # Crucial! Saves clean, non-duplicated ManyToMany records safely.
            
            # --- AUTOMATIC ROLE UPGRADE ENGINE ---
            if not profile.is_farmer:
                profile.is_farmer = True
                profile.save() # Persists the new status in the database
            
            # Add user feedback message before redirecting
            messages.success(request, "Produce AD published successfully!")
            return redirect('account')

    context = {'form': form}
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def update_product(request, pk):
    profile = request.user.profile 
    product = profile.product_set.get(id=pk)
    form = ProductForm(instance=product)   

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save() # Automatically updates core information and ManyToMany associations
            return redirect('account')

    context = {'form': form, 'product': product}
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def delete_product(request, pk):

    profile = request.user.profile  # get logged-in user's profile
    product = profile.product_set.get(id=pk) # only allow deleting products owned by the logged-in user

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {'object': product}
    return render(request, 'delete-template.html', context)

@login_required(login_url='login')
def manage_categories(request):
    # Restrict this portal view to administrators or verified managers
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Only marketplace administrators can manage category architecture.')
        return redirect('account')

    form = CategoryManagementForm()
    
    if request.method == 'POST':
        form = CategoryManagementForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Successfully registered structural tier: "{category}"')
            return redirect('manage-categories')

    # Fetch root records only; our template will cascade down through children branches automatically
    root_categories = Category.objects.filter(parent__isnull=True).prefetch_related('children__children')

    context = {
        'form': form,
        'root_categories': root_categories
    }
    return render(request, 'products/manage-categories.html', context)

def homepage_view(request):
    return render(request, 'homepage.html')
 
 
def contact_view(request):
    if request.method == 'POST':
        # Simple: just flash a success message for now
        # Later you can wire this to send an actual email via Django's send_mail
        first_name = request.POST.get('first_name', '')
        messages.success(request, f"Thank you {first_name}! Your message has been received. We'll be in touch within 24 hours.")
        # To send real email later, add:
        # from django.core.mail import send_mail
        # send_mail(subject, message, from_email, [to_email])
    return render(request, 'contact.html')
 
 
def faq_view(request):
    return render(request, 'faq.html')
