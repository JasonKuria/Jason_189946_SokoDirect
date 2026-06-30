import os
import django

# =====================================================================
# STEP 1: Set up the Django Environment
# =====================================================================
# This line tells Python where your project settings are located.
# Change 'SokoDirect' to match your actual Django project directory name
# if it is different.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SokoDirect.settings')

# =====================================================================
# STEP 2: Initialize Django
# =====================================================================
# This loads your models, database configurations, and app registry
# so you can interact with Django models outside of the running server.
django.setup()

# =====================================================================
# STEP 3: Import your Category model
# =====================================================================
from products.models import Category

# =====================================================================
# STEP 4: Define a nested dictionary of Kenyan agricultural categories
# =====================================================================
# This structured tree maps directly to your self-referential Category 
# model (Root -> Level 1 Subcategory -> Level 2 Specific Produce).
CATEGORIES_TREE = {
    "Crops": {
        "Fruits": [
            "Avocados", 
            "Mangoes", 
            "Oranges", 
            "Bananas", 
            "Passion Fruits", 
            "Watermelons"
        ],
        "Vegetables": [
            "Tomatoes", 
            "Onions", 
            "Kales (Sukuma Wiki)", 
            "Cabbages", 
            "Spinach", 
            "Capsicums (Pilipili Hoho)"
        ],
        "Cereals & Grains": [
            "Maize", 
            "Wheat", 
            "Rice", 
            "Beans", 
            "Peas", 
            "Sorghum"
        ],
        "Tubers & Roots": [
            "Potatoes (Viazi)", 
            "Sweet Potatoes", 
            "Cassava"
        ]
    },
    "Livestock & Poultry": {
        "Poultry": [
            "Kienyeji Chicken", 
            "Broilers", 
            "Layers", 
            "Chicken Eggs", 
            "Ducks & Turkeys"
        ],
        "Dairy": [
            "Fresh Cow Milk", 
            "Goat Milk", 
            "Yogurt", 
            "Cheese"
        ],
        "Live Animals": [
            "Goats", 
            "Sheep", 
            "Dairy Cows", 
            "Pigs"
        ]
    },
    "Farm Inputs & Equipment": {
        "Seeds & Seedlings": [
            "Fruit Seedlings", 
            "Vegetable Seeds", 
            "Tree Seedlings"
        ],
        "Fertilizers & Soil Care": [
            "Organic Compost", 
            "Animal Manure", 
            "Commercial Fertilizers"
        ],
        "Animal Feed": [
            "Poultry Feed (Mash/Pellets)", 
            "Dairy Meal", 
            "Hay & Silage"
        ]
    }
}

def seed_categories():
    print("🌾 Starting SokoDirect nested category database populator...")
    count_created = 0
    count_existed = 0

    # Loop through the root level categories (e.g., "Crops", "Livestock & Poultry")
    for root_name, subcategories in CATEGORIES_TREE.items():
        # Get or create the root category (parent is None)
        root_category, root_created = Category.objects.get_or_create(
            name=root_name, 
            parent=None
        )
        
        if root_created:
            print(f"📁 Created Root Category: {root_name}")
            count_created += 1
        else:
            count_existed += 1

        # Loop through Level 1 subcategories (e.g., "Fruits", "Vegetables")
        for sub_name, specific_items in subcategories.items():
            sub_category, sub_created = Category.objects.get_or_create(
                name=sub_name, 
                parent=root_category
            )
            
            if sub_created:
                print(f"  └── 📁 Created Subcategory: {sub_name}")
                count_created += 1
            else:
                count_existed += 1

            # Loop through Level 2 specific products (e.g., "Avocados", "Tomatoes")
            for item_name in specific_items:
                item_category, item_created = Category.objects.get_or_create(
                    name=item_name, 
                    parent=sub_category
                )
                
                if item_created:
                    print(f"      └── 🥑 Created Item: {item_name}")
                    count_created += 1
                else:
                    count_existed += 1

    # Print execution summary statistics
    print("\n🎉 Category hierarchy population complete!")
    print(f"Generated {count_created} new categories. {count_existed} already existed.")

# This block prevents the script from running automatically if imported elsewhere
if __name__ == '__main__':
    seed_categories()