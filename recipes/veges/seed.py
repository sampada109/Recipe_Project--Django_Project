import os
import random
from faker import Faker
from django.conf import settings
from django.contrib.auth.models import User
from .models import tags, recp_category, recipes

fake = Faker()

# Generate fake users
def generate_fake_users(n):
    try:
        for i in range(n):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            password = fake.password()
            
            # Ensure the username is unique
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password
            )
    except Exception as e:
        print(e)

# Generate fake recipes
def generate_fake_recipes(n):
    try:
        user_obj = User.objects.all()
        tag_obj = tags.objects.all()
        category_obj = recp_category.objects.all()
        
        # List of food-related words for recipe names
        food_words = ['spaghetti', 'ice-cream', 'pancakes', 'pizza', 'lasagna', 'cheesecake', 'eggs', 'burger', 'sushi', 'taco', 'grilled cheese', 'curry', 'pasta', 'salad', 'cake', 'tacos']
        
        # Get list of default image files
        default_img_dir = os.path.join(settings.BASE_DIR, 'static/img/recp_def')
        default_img_files = os.listdir(default_img_dir)
        
        for i in range(n):
            user = random.choice(user_obj)
            recp_name = fake.random_element(food_words) + ' ' + ' '.join(fake.words(nb=random.randint(1, 5)))
            recp_desp = fake.text()
            category = random.choice(category_obj)
            ratings = random.randint(1, 5)
            views = random.randint(10, 100)
            favourites = random.randint(5, 20)
            # Generate a list of 3-4 random tags
            selected_tags = random.sample(list(tag_obj), k=random.randint(3, 4))
            
            # Choose a random image file
            random_img_file = random.choice(default_img_files)
            recp_img_path = os.path.join('img/recp_def', random_img_file)  # Path relative to STATIC_ROOT
            
            recipe = recipes.objects.create(
                user=user,
                recp_name=recp_name,
                recp_desp=recp_desp,
                recp_img=recp_img_path,
                category=category,
                ratings=ratings,
                views=views,
                favourites=favourites
            )

            recipe.tags.add(*selected_tags)
            recipe.save()

    except Exception as e:
        print(e)    



# generate_fake_users(10)  # Generate 10 fake users
# generate_fake_recipes(15)  # Generate 15 fake recipes


# go to django shell import all the models from app and run the functions to generate data