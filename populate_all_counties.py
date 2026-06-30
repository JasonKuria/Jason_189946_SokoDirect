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
# This loads your models, database connections, and configurations 
# so you can use Django code outside of a running web server.
django.setup()

# =====================================================================
# STEP 3: Import your County model
# =====================================================================
from products.models import County

# =====================================================================
# STEP 4: Define the list of all 47 Kenyan counties
# =====================================================================
ALL_KENYAN_COUNTIES = [
    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita/Taveta",
    "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru",
    "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua",
    "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot",
    "Samburu", "Trans Nzoia", "Uasin Gishu", "Elgeyo/Marakwet", "Nandi", "Baringo",
    "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet",
    "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu",
    "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi City"
]

def seed_all_counties():
    print("🌾 Starting SokoDirect county database populator (47 Counties)...")
    
    # Track the progress of inserted entries
    count_created = 0
    count_existed = 0

    # Loop through each county name in our list
    for county_name in ALL_KENYAN_COUNTIES:
        # get_or_create checks if a county with the same name already exists.
        # - If it exists: It retrieves the object and sets 'created' to False.
        # - If it doesn't: It inserts it into the database and sets 'created' to True.
        county, created = County.objects.get_or_create(name=county_name)
        
        if created:
            print(f"✅ Added: {county_name}")
            count_created += 1
        else:
            print(f"ℹ️ Already exists: {county_name}")
            count_existed += 1

    # Print a summary of the operation
    print("\n🎉 Population complete!")
    print(f"Added {count_created} new counties. {count_existed} were already in the database.")

# This block ensures the script only runs if executed directly, 
# not if imported into another Python file.
if __name__ == '__main__':
    seed_all_counties()