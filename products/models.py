
# Create your models here.
# products/models.py
import uuid
from django.db import models
from users.models import Profile  

 #county model
class County(models.Model):
    name = models.CharField(max_length=200)  # e.g. Nairobi, Mombasa, Nakuru
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name_plural = 'Counties'  # Without this, admin shows 'Countys'
 
    def __str__(self):
        return self.name
    
    #category model
class Category(models.Model):
    name = models.CharField(max_length=200)
 
    # 'self' means this ForeignKey points back to the Category table itself.
    # null=True, blank=True means a category can have NO parent (a root category).
    # related_name='children' lets us write category.children.all() later.
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name_plural = 'Categories'
 
    def __str__(self):
        # Walk up the parent chain to build a readable path like:
        # 'Fruits & Vegetables > Vegetables > Tomatoes'
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

#speciality model
class Speciality(models.Model):
    name = models.CharField(max_length=200)  # e.g. Dairy, Tomatoes, Poultry
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
    
    #product model
class Product(models.Model):
    # Which farmer listed this produce. ForeignKey = many products, one owner.
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    county = models.ForeignKey(
        County, on_delete=models.SET_NULL, null=True, blank=True
    )
 
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                default=0.00, null=True, blank=True)
    quantity_available = models.IntegerField(default=0, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)  # kg, bunch, piece
 
    featured_image = models.ImageField(
        null=True, blank=True,
        default='default.jpg',
        upload_to='products/'  # saves to media/products/
    )
    contact_link = models.CharField(max_length=2000, null=True, blank=True)
    farm_link = models.CharField(max_length=2000, null=True, blank=True)
 
    # ManyToMany — one product, many category tags; one category, many products
    categories = models.ManyToManyField(Category, blank=True)
 
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
 
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
 
    def __str__(self):
        return self.title
 
    @property
    def imageURL(self):
        try:
            return self.featured_image.url
        except:
            return ''
        
        #Review model
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        # Enforces ONE review per owner per product at the database level —

        unique_together = [['owner', 'product']]
 
    def __str__(self):
        return self.value


 





