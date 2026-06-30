import os
import django

# =====================================================================
# STEP 1: Set up the Django Environment
# =====================================================================
# Tells Python where your settings file is located. 
# It uses 'SokoDirectProducts.settings' to match your folder structure.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SokoDirect.settings')

# =====================================================================
# STEP 2: Initialize Django
# =====================================================================
# Loads SokoDirect configurations, database connections, and registered apps.
django.setup()

# =====================================================================
# STEP 3: Import your Models
# =====================================================================
# We import Django's built-in User model and your custom Profile model
from django.contrib.auth.models import User
from users.models import Profile

# =====================================================================
# STEP 4: Define 15 Sample Kenyan Users and Profiles
# =====================================================================
# We define a list of 15 authentic Kenyan usernames, names, and passwords.
SAMPLE_PROFILES = [
    {
        "username": "wanjiku",
        "email": "wanjiku@sokodirect.com",
        "name": "Wanjiku Nafula",
        "password": "FarmerPassKiambu1"
    },
    {
        "username": "kiprop",
        "email": "kiprop@sokodirect.com",
        "name": "Juma Kiprop",
        "password": "FarmerPassUasin2"
    },
    {
        "username": "anyango",
        "email": "anyango@sokodirect.com",
        "name": "Anyango Mwajuma",
        "password": "BuyerPassMombasa3"
    },
    {
        "username": "kamau",
        "email": "kamau@sokodirect.com",
        "name": "Kamau Njoroge",
        "password": "FarmerPassNakuru4"
    },
    {
        "username": "fatuma",
        "email": "fatuma@sokodirect.com",
        "name": "Fatuma Omar",
        "password": "BuyerPassGarissa5"
    },
    {
        "username": "kipkorir",
        "email": "kipkorir@sokodirect.com",
        "name": "Chotara Kipkorir",
        "password": "FarmerPassKericho6"
    },
    {
        "username": "nekesa",
        "email": "nekesa@sokodirect.com",
        "name": "Nekesa Simiyu",
        "password": "FarmerPassBungoma7"
    },
    {
        "username": "mwende",
        "email": "mwende@sokodirect.com",
        "name": "Mwende Mutua",
        "password": "BuyerPassMachakos8"
    },
    {
        "username": "ochieng",
        "email": "ochieng@sokodirect.com",
        "name": "Ochieng Otieno",
        "password": "FarmerPassKisumu9"
    },
    {
        "username": "ndwiga",
        "email": "ndwiga@sokodirect.com",
        "name": "Ndwiga Njiru",
        "password": "FarmerPassEmbu10"
    },
    {
        "username": "waweru",
        "email": "waweru@sokodirect.com",
        "name": "Waweru Githinji",
        "password": "FarmerPassNyand11"
    },
    {
        "username": "moraa",
        "email": "moraa@sokodirect.com",
        "name": "Moraa Ongeri",
        "password": "BuyerPassKisii12"
    },
    {
        "username": "makori",
        "email": "makori@sokodirect.com",
        "name": "Makori Nyambane",
        "password": "FarmerPassNyamira13"
    },
    {
        "username": "gathoni",
        "email": "gathoni@sokodirect.com",
        "name": "Gathoni Kimani",
        "password": "BuyerPassNairobi14"
    },
    {
        "username": "sankan",
        "email": "sankan@sokodirect.com",
        "name": "Lolwande Ole Sankan",
        "password": "J@son123a"
    },
    {
        "username": "makena",
        "email": "makena@sokodirect.com",
        "name": "Makena James",
        "password": "J@son123a"
    },  
    {
        "username": "nicole",
        "email": "nicole@sokodirect.com",
        "name": "Nicole Strath",
        "password": "J@son123a"
    },      
]

def populate_profiles():
    print("🌾 Starting SokoDirect built-in User & Profile populator...")
    
    created_count = 0
    updated_count = 0

    for item in SAMPLE_PROFILES:
        # 1. First, create or retrieve the standard Django built-in User table entry
        # This is where the 'email' field is safely stored!
        user, user_created = User.objects.get_or_create(
            username=item["username"],
            defaults={"email": item["email"]}
        )

        if user_created:
            # Set password securely using Django's password hashing engine
            user.set_password(item["password"])
            user.save()
            print(f"👤 Created Django User: @{item['username']}")

        # 2. Next, handle SokoDirect's custom Profile creation
        # We only pass 'user', 'name', and 'username' since those are the fields 
        # actually present in your current custom Profile model definition.
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={
                "name": item["name"],
                "username": item["username"]
            }
        )

        # If the profile already existed, update its name and username fields
        if not profile_created:
            profile.name = item["name"]
            profile.username = item["username"]
            profile.save()
            print(f"🔄 Updated Profile details for: @{item['username']}")
            updated_count += 1
        else:
            print(f"✅ Created Profile entry for: @{item['username']}")
            created_count += 1

    print("\n==================================================")
    print(f"🎉 Population Complete: {created_count} created, {updated_count} updated.")
    print("==================================================")

if __name__ == "__main__":
    populate_profiles()