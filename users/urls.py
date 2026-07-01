# users/urls.py (new file)
from django.urls import path
from . import views

urlpatterns = [
    # Farmer profiles listing - will be the homepage
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_Profile, name='user_profile'),

    # Secure Session Routes
    # Onboarding Session Management Engine Paths
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'), # <--- Added sign-up route

    # Secure Account Space Tracking Paths
    path('account/', views.userAccount, name='account'), # <--- New User Account Route
    path('edit-account/', views.editAccount, name='edit-account'), # <--- Profile Form Path

    # Creaste Speciality Path
    path('create-speciality/', views.createSpeciality, name='create-speciality'),
    path('update-speciality/<str:pk>/', views.updateSpeciality, name='update-speciality'),
    path('delete-speciality/<str:pk>/', views.deleteSpeciality, name='delete-speciality'),

    # Messages
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.viewMessage, name='message'),  
    path('create-message/<str:pk>', views.createMessage, name='create-message'),   

    # User Management Dashboard    
    path('userdashboard/', views.userManagementDashboard, name='userdashboard'),      

]
