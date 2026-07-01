# users/utils.py

from .models import Profile, Speciality
from django.db.models import Q # Import the Q object for complex queries
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):

    page = 1  # Default to the first page
    #page = 2 # Get the 'page' parameter from the GET request. If it's not provided, default to 1. This allows users to navigate through different pages of profiles.
    page = request.GET.get('page', page) # Get the 'page' parameter from the GET request. If it's not provided, default to the value of the 'page' variable (which is 2 in this case). This allows users to navigate through different pages of profiles.
    #results = 3 # Number of profiles to display per page
    paginator = Paginator(profiles, results) # Create a Paginator object with the filtered profiles and the number of results per page.

    profiles = paginator.page(page) # Get the profiles for the current page. This will return a subset of the profiles based on the pagination settings.

    try:
        profiles = paginator.page(page) # Try to get the profiles for the current page. This will return a subset of the profiles based on the pagination settings.
    except PageNotAnInteger:
        page = 1 # If the 'page' parameter is not an integer, default to the first page.
        profiles = paginator.page(page) # Get the profiles for the first page.
    except EmptyPage:
        page = paginator.num_pages # If the 'page' parameter is out of range (e.g., too high), default to the last page.
        profiles = paginator.page(page) # Get the profiles for the last page.

    leftIndex = int(page) - 4 # Calculate the left index for pagination links. This will determine how many page numbers to show before the current page.
    if leftIndex < 1:
        leftIndex = 1 # Ensure the left index does not go below 1.
    
    rightIndex = int(page) + 5 # Calculate the right index for pagination links. This will determine how many page numbers to show after the current page.
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1 # Ensure the right index does not go beyond the total number of pages.

    custom_range = range(leftIndex, rightIndex) # Create a custom range for pagination links. This can be used in the template to display page numbers for navigation.

    return profiles, custom_range

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): 
        search_query = request.GET.get('search_query')

    speciality = Speciality.objects.filter(name__icontains=search_query) 

    profiles = Profile.objects.distinct().filter( 
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) | 
        Q(speciality__in=speciality)) 

    return profiles, search_query
