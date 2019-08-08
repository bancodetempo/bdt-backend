from model_mommy.recipe import Recipe, foreign_key

from .models import Account, AccountTransaction
from authentication.test_recipes import user_recipe


account_recipe = Recipe(
    Account,
    balance=0,
    owner=foreign_key(user_recipe)
)
