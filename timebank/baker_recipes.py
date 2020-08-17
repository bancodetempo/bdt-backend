
from model_bakery import baker
from model_bakery.recipe import Recipe, foreign_key

from .models import Account, AccountTransaction
from authentication.baker_recipes import user_recipe


account_recipe = Recipe(
    Account,
    balance=0,
    owner=foreign_key(user_recipe)
)
