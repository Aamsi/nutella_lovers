from django.core.management import call_command
from django.core.management.base import BaseCommand

import requests
import json

from substitute.models import Categories, PurchaseStores, Products


class Command(BaseCommand):
    help = "Load initial data"

    def handle(self, *args, **options):
        opf = Openfoodfacts()
        opf.insert_categories()
        opf.insert_stores()
        opf.insert_products()


class Openfoodfacts():
    def __init__(self):
        self.categories_url = "https://fr.openfoodfacts.org/categories&json=1"
        self.stores_url = "https://fr.openfoodfacts.org/stores&json=1"
        self.categories = []
        self.stores = []
        self.products = []

    def insert_categories(self):
        res = requests.get(self.categories_url)
        categories = res.json()['tags'][:200]
        for category in categories:
            cat_to_add = Categories(category_name=category['name'])
            cat_to_add.save()

    def insert_stores(self):
        res = requests.get(self.stores_url)
        stores = res.json()['tags'][:200]
        for store in stores:
            store_to_add = PurchaseStores(store_name=store['name'])
            store_to_add.save()

    def insert_products(self):
        stores = PurchaseStores.objects.all()
        categories = Categories.objects.all()

        store_names = [store.store_name for store in stores]
        categories_name = [category.category_name for category in categories]

        products_to_ignore = []

        for category in categories_name:
            url = f"https://fr.openfoodfacts.org/categorie/{category}.json"
            res = requests.get(url)
            products = res.json()
            for product in products['products']:
                store = self.filter_store(product)
                if not store or product['product_name'] in products_to_ignore:
                    continue
                if store in store_names:
                    store_instance = PurchaseStores.objects.get(store_name=store)
                    category_instance = Categories.objects.get(category_name=category)
                    prod_to_add = Products(
                        product_name=product['product_name'],
                        nutriscore=product['nutrition_grades_tags'][0],
                        barcode=product['code'],
                        details=self.generic_name(product),
                        category=category_instance,
                        purchase_store=store_instance
                    )
                    prod_to_add.save()
                    products_to_ignore.append(product['product_name'])

    def filter_store(self, product):
        try:
            return product['stores_tags'][0].strip().capitalize()
        except (IndexError, KeyError):
            return None

    def generic_name(self, product):
        try:
            return product['generic_name_fr']
        except KeyError:
            return None
