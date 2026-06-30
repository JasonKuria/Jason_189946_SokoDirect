# Products/utils.py - add these lines

from .models import Product, Category
from django.db.models import Q # Import the Q object for complex queries
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProducts(request, products, results):

    page = 1  # Default to the first page
    #page = 2 # Get the 'page' parameter from the GET request. If it's not provided, default to 1. This allows users to navigate through different pages of products.
    page = request.GET.get('page', page) # Get the 'page' parameter from the GET request. If it's not provided, default to the value of the 'page' variable (which is 2 in this case). This allows users to navigate through different pages of products.
    results = 6 # Number of products to display per page
    paginator = Paginator(products, results) # Create a Paginator object with the filtered products and the number of results per page.

    products = paginator.page(page) # Get the products for the current page. This will return a subset of the products based on the pagination settings.

    try:
        products = paginator.page(page) # Try to get the products for the current page. This will return a subset of the products based on the pagination settings.
    except PageNotAnInteger:
        page = 1 # If the 'page' parameter is not an integer, default to the first page.
        products = paginator.page(page) # Get the products for the first page.
    except EmptyPage:
        page = paginator.num_pages # If the 'page' parameter is out of range (e.g., too high), default to the last page.
        products = paginator.page(page) # Get the products for the last page.

    leftIndex = int(page) - 4 # Calculate the left index for pagination links. This will determine how many page numbers to show before the current page.
    if leftIndex < 1:
        leftIndex = 1 # Ensure the left index does not go below 1.
    
    rightIndex = int(page) + 5 # Calculate the right index for pagination links. This will determine how many page numbers to show after the current page.
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1 # Ensure the right index does not go beyond the total number of pages.

    custom_range = range(leftIndex, rightIndex) # Create a custom range for pagination links. This can be used in the template to display page numbers for navigation.

    return products, custom_range

def searchProducts(request):
    search_query = ''

    if request.GET.get('search_query'): 
        search_query = request.GET.get('search_query')

    category = Category.objects.filter(name__icontains=search_query) # Perform a case-insensitive search on the 'name' field of the Category model to find categories that match the search query. The resulting queryset is stored in the 'category' variable, which is then used to filter products based on their associated categories.        

    products = Product.objects.distinct().filter(
        Q(title__icontains=search_query) | 
        Q(description__icontains=search_query) | 
        Q(owner__name__icontains=search_query) | # Allow searching by the owner's name as well, which is a common requirement in marketplace applications where users may want to find products by specific sellers. This enhances the search functionality by enabling users to find products not only by their title and description but also by the name of the seller, making it easier to discover products from preferred sellers or brands.
        Q(categories__in=category) # Filter products based on their associated categories that match the search query. This allows users to find products not only by title and description but also by the categories they belong to, making it easier to discover products within specific categories of interest.
    )

    return products, search_query






#  update your searchProducts function with this version
# This adds category_id support so clicking a parent shows ALL descendant products
def get_all_descendant_ids(category):
    """
    Recursively collects IDs of a category and ALL its children/grandchildren.
    e.g. clicking 'Crops' returns IDs for Crops + Vegetables + Tomatoes + Kales etc.
    """
    ids = [category.id]
    for child in category.children.all().prefetch_related('children'):
        ids.extend(get_all_descendant_ids(child))
    return ids

def searchProducts(request):
    search_query = request.GET.get('search_query', '')
    category_id  = request.GET.get('category_id', '')

    products = Product.objects.distinct()

    if category_id:
        # Clicking a parent category → show ALL products in that tree
        try:
            root_cat = Category.objects.prefetch_related(
                'children__children'
            ).get(id=category_id)
            all_ids = get_all_descendant_ids(root_cat)
            products = products.filter(categories__id__in=all_ids)
        except Category.DoesNotExist:
            pass

    elif search_query:
        # Normal text search across title, description, owner name, category name
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(categories__name__icontains=search_query)
        )

    return products, search_query

