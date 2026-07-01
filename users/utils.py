# users/utils.py

from .models import Profile, Speciality
from django.db.models import Q # Import the Q object for complex queries
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):

    page = 1  
    #page = 2 # Get the 'page' parameter from the GET request. If it's not provided, default to 1. This allows users to navigate through different pages of profiles.
    page = request.GET.get('page', page) 
    #results = 3 # Number of profiles to display per page
    paginator = Paginator(profiles, results) # Create a Paginator object with the filtered profiles and the number of results per page.

    profiles = paginator.page(page) # Get the profiles for the current page. This will return a subset of the profiles based on the pagination settings.

    try:
        profiles = paginator.page(page) # Try to get the profiles for the current page. This will return a subset of the profiles based on the pagination settings.
    except PageNotAnInteger:
        page = 1 
        profiles = paginator.page(page) 
    except EmptyPage:
        page = paginator.num_pages # If the 'page' parameter is out of range (e.g., too high), default to the last page.
        profiles = paginator.page(page)

    leftIndex = int(page) - 4 # Calculate the left index for pagination links. This will determine how many page numbers to show before the current page.
    if leftIndex < 1:
        leftIndex = 1 
    
    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex) 
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
