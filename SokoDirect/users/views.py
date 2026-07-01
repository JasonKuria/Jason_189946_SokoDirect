

import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product

from .forms import (
    CustomUserCreationForm,
    ProfileForm,
    SpecialityForm,
    MessageForm
)

from .models import (
    Profile,
    Speciality,
    Message
)

from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('products')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Account username does not exist.')
            return render(
                request,
                'users/login_register.html',
                {'page': page}
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            try:
                cart = json.loads(
                    request.COOKIES.get('cart', '{}')
                )
            except Exception:
                cart = {}

            login(request, user)

            if cart:
                for product_id, item in cart.items():
                    try:
                        Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        continue

            messages.success(
                request,
                f'Welcome back to SokoDirect, {user.username}!'
            )

            next_url = request.GET.get('next')

            response = redirect(next_url or 'products')
            response.delete_cookie('cart')

            return response

        messages.error(
            request,
            'Username or password incorrect.'
        )

    return render(
        request,
        'users/login_register.html',
        {'page': page}
    )


def logoutUser(request):
    logout(request)

    messages.info(
        request,
        'You have successfully logged out.'
    )

    response = redirect('login')
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

            login(request, user)

            messages.success(
                request,
                'Your account was created successfully!'
            )

            return redirect('edit-account')

        messages.error(
            request,
            'An error occurred during registration.'
        )

    return render(
        request,
        'users/login_register.html',
        {
            'page': page,
            'form': form
        }
    )


def profiles(request):

    profiles, search_query = searchProfiles(request)

    profiles, custom_range = paginateProfiles(
        request,
        profiles,
        12
    )

    return render(
        request,
        'users/profiles.html',
        {
            'profiles': profiles,
            'search_query': search_query,
            'custom_range': custom_range
        }
    )


def user_Profile(request, pk):

    profile = get_object_or_404(
        Profile,
        id=pk
    )

    topSpeciality = (
        profile.speciality_set
        .exclude(description__isnull=True)
        .exclude(description='')
    )

    otherSpeciality = (
        profile.speciality_set
        .filter(description__in=['', None])
    )

    return render(
        request,
        'users/user-profile.html',
        {
            'profile': profile,
            'topSpeciality': topSpeciality,
            'otherSpeciality': otherSpeciality
        }
    )


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profile

    context = {
        'profile': profile,
        'specialities': profile.speciality_set.all(),
        'products': profile.product_set.all()
    }

    return render(
        request,
        'users/account.html',
        context
    )


@login_required(login_url='login')
def editAccount(request):

    profile = request.user.profile

    form = ProfileForm(
        instance=profile
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('account')

    return render(
        request,
        'users/profile_form.html',
        {'form': form}
    )


@login_required(login_url='login')
def createSpeciality(request):

    form = SpecialityForm()

    if request.method == 'POST':

        form = SpecialityForm(
            request.POST
        )

        if form.is_valid():

            speciality = form.save(
                commit=False
            )

            speciality.owner = (
                request.user.profile
            )

            speciality.save()

            messages.success(
                request,
                'Speciality added.'
            )

            return redirect(
                'account'
            )

    return render(
        request,
        'users/speciality_form.html',
        {'form': form}
    )


@login_required(login_url='login')
def inbox(request):

    profile = request.user.profile

    messageRequest = (
        profile.messages.all()
    )

    unreadCount = (
        messageRequest
        .filter(is_read=False)
        .count()
    )

    return render(
        request,
        'users/inbox.html',
        {
            'messageRequest': messageRequest,
            'unreadCount': unreadCount
        }
    )


@login_required(login_url='login')
def viewMessage(request, pk):

    message = get_object_or_404(
        request.user.profile.messages,
        id=pk
    )

    if not message.is_read:

        message.is_read = True
        message.save()

    return render(
        request,
        'users/message.html',
        {'message': message}
    )


def createMessage(request, pk):

    recipient = get_object_or_404(
        Profile,
        id=pk
    )

    sender = (
        getattr(
            request.user,
            'profile',
            None
        )
        if request.user.is_authenticated
        else None
    )

    form = MessageForm()

    if request.method == 'POST':

        form = MessageForm(
            request.POST
        )

        if form.is_valid():

            message = form.save(
                commit=False
            )

            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(
                request,
                'Message sent successfully.'
            )

            return redirect(
                'user_profile',
                pk=recipient.id
            )

    return render(
        request,
        'users/message_form.html',
        {
            'recipient': recipient,
            'form': form
        }
    )

