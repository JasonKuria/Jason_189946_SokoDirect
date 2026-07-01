import os
import django

# =====================================================================
# STEP 1: Set up the Django Environment
# =====================================================================
# Tells Python where your settings file is. Matches 'SokoDirectProducts.settings'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SokoDirect.settings')

# =====================================================================
# STEP 2: Initialize Django
# =====================================================================
# Loads your configuration so you can interact with your models.
django.setup()

# =====================================================================
# STEP 3: Import your Models
# =====================================================================
from django.contrib.auth.models import User
from users.models import Profile
from products.models import Product, Review

# =====================================================================
# STEP 4: Define Sample Buyer Users
# =====================================================================
# We need different buyers because of the unique_together constraint.
# One buyer profile can only review a specific product once.
SAMPLE_BUYERS = [
    {
        "username": "buyer_makena",
        "email": "makena@sokodirect.com",
        "name": "Makena Ndwiga"
    },
    {
        "username": "buyer_jason",
        "email": "jason@sokodirect.com",
        "name": "Jason Mwenda"
    },
    {
        "username": "buyer_mwangi",
        "email": "mwangi@sokodirect.com",
        "name": "Mwangi Kamau"
    }
]

# =====================================================================
# STEP 5: Define 15 Realistic Product Reviews
# =====================================================================
# We map each review to a target product title and assign it to one of
# our three sample buyers to keep things clean and varied.
SAMPLE_REVIEWS = [
    {
        "product_title": "Fresh Export-Grade Hass Avocados",
        "buyer_username": "buyer_makena",
        "body": "These avocados arrived perfectly green and ripened beautifully within three days! Extremely creamy and large.",
        "value": "up"
    },
    {
        "product_title": "Red Ripe Roma Tomatoes",
        "buyer_username": "buyer_jason",
        "body": "Great quality tomatoes for my restaurant. Very thick skins and minimal water content, which makes excellent paste.",
        "value": "up"
    },
    {
        "product_title": "Pure Raw Forest Honey",
        "buyer_username": "buyer_mwangi",
        "body": "This honey has a deep, rich forest flavor. Truly unfiltered and authentic. Will definitely buy again.",
        "value": "up"
    },
    {
        "product_title": "Fresh Whole Cow Milk",
        "buyer_username": "buyer_makena",
        "body": "Extremely fresh and creamy. Reminds me of the milk we used to get directly from the village when growing up.",
        "value": "up"
    },
    {
        "product_title": "Crispy Sukuma Wiki (Kales)",
        "buyer_username": "buyer_jason",
        "body": "Clean, crisp, and ready to cook. Very fresh and saved me a lot of prep time.",
        "value": "up"
    },
    {
        "product_title": "Sweet Cavendish Bananas",
        "buyer_username": "buyer_mwangi",
        "body": "A bit bruised on arrival due to transport, but they are incredibly sweet and naturally ripened.",
        "value": "up"
    },
    {
        "product_title": "Irish Potatoes (Shangi)",
        "buyer_username": "buyer_makena",
        "body": "The absolute best Shangi potatoes! Made the crispiest home fries. No rotten ones in the bag.",
        "value": "up"
    },
    {
        "product_title": "Fresh Kienyeji Eggs",
        "buyer_username": "buyer_jason",
        "body": "Excellent eggs with deep yellow yolks. Customers at my diner have noticed the quality improvement!",
        "value": "up"
    },
    {
        "product_title": "Organic Macadamia Nuts",
        "buyer_username": "buyer_mwangi",
        "body": "Very fresh, crunchy, and well-packaged. Perfect healthy snack to keep at the office desk.",
        "value": "up"
    },
    {
        "product_title": "Sweet Kent Mangoes",
        "buyer_username": "buyer_makena",
        "body": "Gigantic, sweet, and juice-filled Kent mangoes! Not stringy at all. My kids loved them.",
        "value": "up"
    },
    {
        "product_title": "Fresh Lake Victoria Tilapia",
        "buyer_username": "buyer_jason",
        "body": "Fish was fresh and clean. Docked a star because delivery was delayed by an hour, but fish quality is excellent.",
        "value": "up"
    },
    {
        "product_title": "Premium Purple Passion Fruits",
        "buyer_username": "buyer_mwangi",
        "body": "Super aromatic and packed with seeds and juice. Made a wonderful passion fruit concentrate.",
        "value": "up"
    },
    {
        "product_title": "Dry White Maize (Premium Grade)",
        "buyer_username": "buyer_makena",
        "body": "Beautifully dried grains with zero moisture smell. Ground them into premium flour for sweet ugali.",
        "value": "up"
    },
    {
        "product_title": "Fresh Spring Bulb Onions",
        "buyer_username": "buyer_jason",
        "body": "Great size, dry skins, and sweet sharp taste. Very good value for bulk purchases.",
        "value": "up"
    },
    {
        "product_title": "Fresh Farm Ginger (Tangawizi)",
        "buyer_username": "buyer_mwangi",
        "body": "Extremely strong and pungent ginger. Perfect for tea brewing and home remedy concoctions.",
        "value": "up"
    }
]

def get_or_create_buyers():
    """
    Creates and returns our distinct buyer profiles so that each product 
    gets reviewed by an active buyer profile.
    """
    profiles = {}
    for buyer in SAMPLE_BUYERS:
        # Create or fetch the basic Auth User (email is safely saved here on User model)
        user, created = User.objects.get_or_create(
            username=buyer["username"],
            defaults={"email": buyer["email"]}
        )
        if created:
            user.set_password("BuyerPass123")
            user.save()

        # Create or fetch corresponding profile
        # FIXED: Removed 'email' and 'short_intro' from defaults to prevent FieldError
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={
                "name": buyer["name"],
                "username": buyer["username"]
            }
        )
        profiles[buyer["username"]] = profile
    return profiles

def update_product_vote_metrics(product):
    """
    Helper function to dynamically calculate and update the target product's 
    overall voting total and positive ratio percentages.
    """
    reviews = product.review_set.all()
    upvotes = reviews.filter(value='up').count()
    total_votes = reviews.count()

    # Avoid divide-by-zero errors if no votes exist
    if total_votes > 0:
        ratio = (upvotes / total_votes) * 100
    else:
        ratio = 100

    product.vote_total = total_votes
    product.vote_ratio = int(ratio)
    product.save()

def populate_reviews():
    print("🌾 Starting SokoDirect Review database population...")
    
    # Ensure our buyer users exist in the database
    buyers = get_or_create_buyers()
    print(f"👥 Created/Verified {len(buyers)} sample buyer profiles.")

    created_count = 0
    skipped_count = 0

    for item in SAMPLE_REVIEWS:
        # 1. Safely locate the target product in the database
        try:
            product = Product.objects.get(title=item["product_title"])
        except Product.DoesNotExist:
            print(f"❌ Product not found (skipping review): '{item['product_title']}'")
            skipped_count += 1
            continue

        # 2. Grab the corresponding buyer profile
        buyer_profile = buyers[item["buyer_username"]]

        # 3. Create the review safely, preventing duplicates on unique_together
        review, created = Review.objects.get_or_create(
            owner=buyer_profile,
            product=product,
            defaults={
                "body": item["body"],
                "value": item["value"]
            }
        )

        if created:
            print(f"✅ Added review to: '{product.title}' by @{buyer_profile.username}")
            # Automatically recalculate the vote ratios so they render on the UI
            update_product_vote_metrics(product)
            created_count += 1
        else:
            print(f"🟡 Review already exists (skipped): '{product.title}' by @{buyer_profile.username}")
            skipped_count += 1

    print("\n==================================================")
    print(f"📊 Population Complete: {created_count} created, {skipped_count} skipped.")
    print("==================================================")

if __name__ == "__main__":
    populate_reviews()