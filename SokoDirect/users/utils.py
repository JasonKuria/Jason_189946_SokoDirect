
from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage
)
from django.db.models import Q

from .models import Profile, Speciality


def paginateProfiles(request, profiles, results):
    """
    Paginate profile results and generate
    a custom page range for templates.
    """

    page = request.GET.get('page', 1)

    paginator = Paginator(
        profiles,
        results
    )

    try:
        profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = max(
        int(page) - 4,
        1
    )

    right_index = min(
        int(page) + 5,
        paginator.num_pages + 1
    )

    custom_range = range(
        left_index,
        right_index
    )

    return profiles, custom_range


def searchProfiles(request):
    """
    Search profiles by:
    - Name
    - Short introduction
    - Speciality
    """

    search_query = request.GET.get(
        'search_query',
        ''
    )

    speciality = (
        Speciality.objects.filter(
            name__icontains=search_query
        )
    )

    profiles = (
        Profile.objects
        .distinct()
        .filter(
            Q(
                name__icontains=search_query
            )
            |
            Q(
                short_intro__icontains=search_query
            )
            |
            Q(
                specialities__in=speciality
            )
        )
    )

    return profiles, search_query

