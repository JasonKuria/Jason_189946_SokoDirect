import os
import django
from decimal import Decimal

# =====================================================================
# STEP 1: Set up the Django Environment
# =====================================================================
# Tells Python where your settings file is. Change 'SokoDirect' if needed.
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
from products.models import County, Category, Product

# =====================================================================
# STEP 4: Define 15 Kenyan Sample Products Data
# =====================================================================
# Detailed, realistic market listings spanning different counties and units.
SAMPLE_PRODUCTS = [
    {
        "title": "Fresh Export-Grade Hass Avocados",
        "description": "Premium organic Hass avocados directly harvested from our farm in Kiambu. High oil content, perfect size, and excellent shelf-life. Sold per crate of approximately 15kg.",
        "price": Decimal("1500.00"),
        "quantity_available": 12,
        "unit": "crates",
        "county_name": "Kiambu",
        "category_names": ["Avocados", "Fruits"]
    },
    {
        "title": "Red Ripe Roma Tomatoes",
        "description": "Thick-skinned, fleshy Roma tomatoes perfect for cooking pastes and salads. Harvested daily under green-house conditions in Nakuru. Free from harmful pesticide residues.",
        "price": Decimal("80.00"),
        "quantity_available": 250,
        "unit": "kg",
        "county_name": "Nakuru",
        "category_names": ["Tomatoes", "Vegetables"]
    },
    {
        "title": "Pure Raw Forest Honey",
        "description": "100% natural, unpasteurized, and unfiltered organic honey sourced directly from our beehives in Baringo forest. Packed in food-grade bottles.",
        "price": Decimal("750.00"),
        "quantity_available": 40,
        "unit": "bottle (1kg)",
        "county_name": "Baringo",
        "category_names": ["Bee Keeping & Honey"]
    },
    {
        "title": "Fresh Whole Cow Milk",
        "description": "Creamy, fresh pasture-fed cow milk from our dairy farm in Nyeri. Chilled immediately post-milking to preserve nutrients and maintain premium freshness.",
        "price": Decimal("65.00"),
        "quantity_available": 100,
        "unit": "liters",
        "county_name": "Nyeri",
        "category_names": ["Fresh Cow Milk", "Dairy"]
    },
    {
        "title": "Crispy Sukuma Wiki (Kales)",
        "description": "Freshly cut, tender, and deeply green Sukuma Wiki leaves harvested early in the morning. Grown using organic compost in Kiambu.",
        "price": Decimal("30.00"),
        "quantity_available": 80,
        "unit": "bunches",
        "county_name": "Kiambu",
        "category_names": ["Kales (Sukuma Wiki)", "Vegetables"]
    },
    {
        "title": "Sweet Cavendish Bananas",
        "description": "Sweet, naturally ripened Cavendish bananas from Meru orchards. Perfect dessert fruit, sold in medium-sized bunches.",
        "price": Decimal("350.00"),
        "quantity_available": 30,
        "unit": "bunches",
        "county_name": "Meru",
        "category_names": ["Bananas", "Fruits"]
    },
    {
        "title": "Irish Potatoes (Shangi)",
        "description": "High-quality, freshly harvested Shangi potatoes from Nyandarua. Excellent for fries, mashing, or traditional stews. Sold in standard bags.",
        "price": Decimal("2800.00"),
        "quantity_available": 50,
        "unit": "50kg bags",
        "county_name": "Nyandarua",
        "category_names": ["Potatoes (Viazi)", "Tubers & Roots"]
    },
    {
        "title": "Fresh Kienyeji Eggs",
        "description": "Nutritious, organic eggs from deep-litter free-range Kienyeji chickens in Kiambu. Distinct golden yolks and excellent taste.",
        "price": Decimal("450.00"),
        "quantity_available": 25,
        "unit": "trays",
        "county_name": "Kiambu",
        "category_names": ["Chicken Eggs", "Poultry"]
    },
    {
        "title": "Organic Macadamia Nuts",
        "description": "De-shelled, raw macadamia nuts from Embu county. High in healthy fats, crunchy, and packed under vacuum for fresh storage.",
        "price": Decimal("900.00"),
        "quantity_available": 60,
        "unit": "kg",
        "county_name": "Embu",
        "category_names": ["Seeds & Seedlings"]
    },
    {
        "title": "Sweet Kent Mangoes",
        "description": "Large, fleshy, and fibreless Kent mangoes from the sunny orchards of Makueni. Extremely sweet and juicy.",
        "price": Decimal("40.00"),
        "quantity_available": 500,
        "unit": "pieces",
        "county_name": "Makueni",
        "category_names": ["Mangoes", "Fruits"]
    },
    {
        "title": "Fresh Lake Victoria Tilapia",
        "description": "Freshly caught Tilapia from Lake Victoria, Kisumu. Cleaned, scaled, and kept on ice. Average size is 400g - 500g per fish.",
        "price": Decimal("180.00"),
        "quantity_available": 150,
        "unit": "pieces",
        "county_name": "Kisumu",
        "category_names": ["Fish Farming (Aquaculture)"]
    },
    {
        "title": "Premium Purple Passion Fruits",
        "description": "Aromatic, sweet-tart purple passion fruits from Uasin Gishu. Excellent for making fresh home juices or direct consumption.",
        "price": Decimal("120.00"),
        "quantity_available": 120,
        "unit": "kg",
        "county_name": "Uasin Gishu",
        "category_names": ["Passion Fruits", "Fruits"]
    },
    {
        "title": "Dry White Maize (Premium Grade)",
        "description": "Clean, well-dried, and sorted premium white maize from the grain basket of Trans Nzoia. Moisture level below 13%, perfect for milling.",
        "price": Decimal("3200.00"),
        "quantity_available": 80,
        "unit": "90kg bags",
        "county_name": "Trans Nzoia",
        "category_names": ["Maize", "Cereals & Grains"]
    },
    {
        "title": "Fresh Spring Bulb Onions",
        "description": "Well-cured, medium-sized red bulb onions with deep purple skins. Great shelf life, harvested from semi-arid farms in Kajiado.",
        "price": Decimal("110.00"),
        "quantity_available": 400,
        "unit": "kg",
        "county_name": "Kajiado",
        "category_names": ["Onions", "Vegetables"]
    },
    {
        "title": "Fresh Farm Ginger (Tangawizi)",
        "description": "Pungent, highly aromatic ginger roots grown organically in Kakamega. Perfect for tea brewing, cooking spices, and commercial value addition.",
        "price": Decimal("160.00"),
        "quantity_available": 90,
        "unit": "kg",
        "county_name": "Kakamega",
        "category_names": ["Vegetables"]
    }
]

def get_or_create_default_farmer():
    """
    Ensures at least one Profile exists to own these sample listings.
    """
    existing_profile = Profile.objects.first()
    if existing_profile:
        return existing_profile

    # If no profile exists, create a default Django User first
    username = "default_farmer"
    user, user_created = User.objects.get_or_create(
        username=username,
        defaults={"email": "farmer@sokodirect.com", "first_name": "SokoDirect Farmer"}
    )
    if user_created:
        user.set_password("SokoPass123")
        user.save()

    # Retrieve or create corresponding Profile
    profile, profile_created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "name": "SokoDirect Verified Farmer",
            "username": username,
            "email": "farmer@sokodirect.com",
            "short_intro": "Verified organic producer supplying fresh harvests.",
            "bio": "Welcome to SokoDirect operations! We produce premium vegetables and fruits."
        }
    )
    return profile

def populate_products():
    print("🌾 Starting SokoDirect Product database population (15 Items)...")
    
    # Get a profile to own the new listings
    default_owner = get_or_create_default_farmer()
    print(f"👤 Products will be owned by: {default_owner.name} (@{default_owner.username})")

    created_count = 0
    skipped_count = 0

    for item in SAMPLE_PRODUCTS:
        # Check if product with the exact title already exists to prevent duplicates
        if Product.objects.filter(title=item["title"]).exists():
            print(f"🟡 Already exists (skipped): {item['title']}")
            skipped_count += 1
            continue

        # 1. Fetch or create the target County safely
        county, _ = County.objects.get_or_create(name=item["county_name"])

        # 2. Create the core Product instance
        product = Product.objects.create(
            owner=default_owner,
            county=county,
            title=item["title"],
            description=item["description"],
            price=item["price"],
            quantity_available=item["quantity_available"],
            unit=item["unit"],
            vote_total=0,
            vote_ratio=100
        )

        # 3. Handle categories linkage
        # Loop through each category name, fetch/create it, and link it to the product
        for cat_name in item["category_names"]:
            category, _ = Category.objects.get_or_create(name=cat_name)
            product.categories.add(category)

        print(f"✅ Created product: {product.title} (Location: {county.name})")
        created_count += 1

    print("\n==================================================")
    print(f"📊 Population Complete: {created_count} created, {skipped_count} skipped.")
    print("==================================================")

if __name__ == "__main__":
    populate_products()