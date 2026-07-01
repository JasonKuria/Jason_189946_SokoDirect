# users/views.py   

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q 
from .models import Profile, Speciality, Message
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SpecialityForm, MessageForm
from .utils import searchProfiles, paginateProfiles

import json
#from orders.utils import cartData # 1. Import cartData to read the cookie contents
#from orders.models import Order, OrderItem
from products.models import Product

def loginUser(request):
    page = 'login' 

    if request.user.is_authenticated:
        return redirect('products') 

    # Fetch guest cookie data for the navbar display badge
    #data = cartData(request)
    #cart_items_count = data['cartItems']

    if request.method == 'POST':
        username_input = request.POST.get('username').strip().lower()
        password_input = request.POST.get('password')
        
        try:
            user_exists = User.objects.get(username=username_input)
        except User.DoesNotExist:
            messages.error(request, "Account username does not exist.")
            #context = {'page': page, 'cartItems': cart_items_count}
            context = {'page': page,}            
            return render(request, 'users/login_register.html', context)

        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            try:
                cart = json.loads(request.COOKIES.get('cart', '{}'))
            except Exception:
                cart = {}

            login(request, user)
            messages.success(request, f"Welcome back to SokoDirect, {user.username}!")

            # Migrate items over to database models cleanly
            # Inside users/views.py -> loginUser function

            # Migrate items over to database models cleanly
            if cart:
                # --- FIXED: Changed user=user to customer=user to match your model layout ---
                #order, created = Order.objects.get_or_create(customer=user, complete=False)
                
                for product_id, item_data in cart.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        quantity = int(item_data.get('quantity', 0))
                        
                        #order_item, item_created = OrderItem.objects.get_or_create(
                        #    order=order, 
                        #    product=product,
                        #    defaults={'quantity': quantity}
                        #)
                        
                        #if not item_created:
                        #    order_item.quantity += quantity
                            
                        #order_item.save()
                    except (Product.DoesNotExist, ValueError):
                        continue

            # --- REDIRECTION ---
            next_url = request.GET.get('next')
            if next_url:
                response = redirect(next_url)
                response.delete_cookie('cart')
                return response
            
            response = redirect('products')
            response.delete_cookie('cart')
            return response
        else:
            messages.error(request, "Username or password incorrect. Please try again.")

    context = {
        'page': page, 
        #'cartItems': cart_items_count 
    }
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request) 
    messages.info(request, "You have successfully logged out of your session.")
    response = redirect('login')
    # Clear the browser cart cookie on logout
    response.delete_cookie('cart')
    return response

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('products')
        
    page = 'register' 
    form = CustomUserCreationForm()
    
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 
            
            messages.success(request, "Your SokoDirect farmer account was created successfully!")
            login(request, user)
            return redirect('edit-account') 
        else:
            messages.error(request, "An error occurred during account creation.")
            
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request) 
    profiles, custom_range = paginateProfiles(request, profiles, 12) 
    
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def user_Profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSpeciality = Speciality.objects.filter(owner=profile).exclude(description__isnull=True).exclude(description__exact="")
    otherSpeciality = Speciality.objects.filter(owner=profile, description__isnull=True) | Speciality.objects.filter(owner=profile, description="")
    
    context = {
        'profile': profile, 
        'topSpeciality': topSpeciality, 
        'otherSpeciality': otherSpeciality
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    specialities = profile.speciality_set.all()
    products = profile.product_set.all()

    context = {
        'profile': profile,
        'specialities': specialities,
        'products': products
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login') 
def editAccount(request):
    profile = request.user.profile 
    form = ProfileForm(instance=profile) 
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)    

@login_required(login_url='login') 
def createSpeciality(request):
    profile = request.user.profile 
    form = SpecialityForm()

    if request.method == 'POST':
        form = SpecialityForm(request.POST)
        if form.is_valid():
            speciality = form.save(commit=False) 
            speciality.owner = profile 
            speciality.save() 
            messages.success(request, "Speciality added successfully!")
            return redirect('account') 
        
    context = {'form': form}
    return render(request, 'users/speciality_form.html', context)

@login_required(login_url='login') 
def updateSpeciality(request, pk):
    profile = request.user.profile 
    speciality = profile.speciality_set.get(id=pk) 
    form = SpecialityForm(instance=speciality) 

    if request.method == 'POST':
        form = SpecialityForm(request.POST, instance=speciality) 
        if form.is_valid():
            form.save() 
            messages.success(request, "Speciality updated successfully!")
            return redirect('account') 
        
    context = {'form': form}
    return render(request, 'users/speciality_form.html', context)

@login_required(login_url='login')
def deleteSpeciality(request, pk):
    profile = request.user.profile 
    speciality = profile.speciality_set.get(id=pk) 

    if request.method == 'POST':
        speciality.delete() 
        messages.success(request, "Speciality deleted successfully!")
        return redirect('account') 
    
    context = {'object': speciality} 
    return render(request, 'delete-template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()

    context = {'messageRequest': messageRequest, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except AttributeError:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)      
            message.sender = sender  
            message.recipient = recipient

        if sender:
            message.name = sender.name
            message.email = sender.email
        message.save()     

        messages.success(request, 'Your message was successfully sent!')       
        return redirect('user_profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


def userManagementDashboard(request):
    # 1. Fetch exact structural segments for your analytics badges
    total_users_count = Profile.objects.count()
    
    buyers_only_count = Profile.objects.filter(is_buyer=True, is_farmer=False).count()
    farmers_only_count = Profile.objects.filter(is_buyer=False, is_farmer=True).count()
    both_count = Profile.objects.filter(is_buyer=True, is_farmer=True).count()

    # 2. Extract choice selection value from the drop-down filter form
    role_filter = request.GET.get('role_filter', '')
    profiles = Profile.objects.all()

    # 3. Apply precise filtering conditions based on dropdown select choice
    if role_filter == 'buyer_only':
        profiles = profiles.filter(is_buyer=True, is_farmer=False)
    elif role_filter == 'farmer_only':
        profiles = profiles.filter(is_buyer=False, is_farmer=True)
    elif role_filter == 'both':
        profiles = profiles.filter(is_buyer=True, is_farmer=True)

    context = {
        'profiles': profiles,
        'role_filter': role_filter,
        'total_users_count': total_users_count,
        'buyers_only_count': buyers_only_count,
        'farmers_only_count': farmers_only_count,
        'both_count': both_count
    }
    return render(request, 'users/user_dashboard.html', context)
