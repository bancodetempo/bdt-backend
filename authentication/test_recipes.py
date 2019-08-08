from model_mommy.recipe import Recipe

from .models import CustomUser


user_recipe = Recipe(
    CustomUser,
    email='user@test.com',
    password='12345',
    is_active=True,
    is_staff=False,
    is_superuser=False,
)
