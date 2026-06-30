import os
import django

# =====================================================================
# STEP 1: Set up the Django Environment
# =====================================================================
# This line tells Python where your project settings are located.
# It uses 'SokoDirectProducts.settings' to match your folder structure.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SokoDirect.settings')

# =====================================================================
# STEP 2: Initialize Django
# =====================================================================
# This loads your models, database connections, and registered apps
# so you can run Django commands outside the main web server.
django.setup()

# =====================================================================
# STEP 3: Import your Speciality model
# =====================================================================
# Corrected: Speciality belongs to the 'products' app models file!
from products.models import Speciality

# =====================================================================
# STEP 4: Define a list of common Kenyan farming specialities
# =====================================================================
# These represent the different agricultural categories farmers can 
# choose to showcase their expertise on SokoDirect.
FARMER_SPECIALITIES = [
    "Dairy Farming",
    "Poultry Rearing",
    "Tomato Cultivation",
    "Avocado Orchards",
    "Maize Farming",
    "Bee Keeping & Honey",
    "Pig Rearing",
    "Goat Farming",
    "Fish Farming (Aquaculture)",
    "Potato Farming",
    "Coffee Farming",
    "Horticulture & Floriculture",
]

def populate_specialities():
    print("🌱 Starting SokoDirect Speciality database population...")
    
    created_count = 0
    skipped_count = 0

    for name in FARMER_SPECIALITIES:
        # get_or_create checks if a record with this name already exists.
        # If it exists, it fetches it; if not, it creates it.
        # This prevents duplicate entry errors when running the script multiple times.
        speciality, created = Speciality.objects.get_or_create(name=name)
        
        if created:
            print(f"✅ Created speciality: {name}")
            created_count += 1
        else:
            print(f"🟡 Already exists (skipped): {name}")
            skipped_count += 1

    print("\n==================================================")
    print(f"📊 Population Complete: {created_count} created, {skipped_count} skipped.")
    print("==================================================")

if __name__ == "__main__":
    populate_specialities()