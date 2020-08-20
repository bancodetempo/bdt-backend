from model_bakery import baker
from model_bakery.recipe import Recipe

from .models import CustomUser


user_recipe = Recipe(
    CustomUser,
    password='12345',
    is_active=True,
    is_staff=False,
    is_superuser=False,
)
