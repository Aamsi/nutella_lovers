from django.core.management import call_command
from django.core.management.base import BaseCommand

import requests
import json

from substitute.models import Categories, PurchaseStores


class Command(BaseCommand):
    help = "Load initial data"

    def handle(self, *args, **options):
        opf = Openfoodfacts()
        categories = opf.get_categories()
        stores = opf.get_stores()
        opf.write_category_store_data()
        call_command('loaddata', 'data_categories_stores.json')
        opf.get_products(categories, stores)
        opf.write_products_data()
        call_command('loaddata', 'data_products.json')


class Openfoodfacts():
    def __init__(self):
        self.categories_url = "https://fr.openfoodfacts.org/categories&json=1"
        self.stores_url = "https://fr.openfoodfacts.org/stores&json=1"
        self.data_categories_stores = []
        self.data_products = []

    def get_categories(self):
        res = requests.get(self.categories_url)
        categories = res.json()['tags'][:200]
        for i, category in enumerate(categories):
            self.data_categories_stores.append({
                'model': 'substitute.categories',
                'pk': i + 1,
                'fields': {
                    'category_name': category['name']
                }
            })
        
        return categories

    def get_stores(self):
        res = requests.get(self.stores_url)
        stores = res.json()['tags'][:200]
        for i, store in enumerate(stores):
            self.data_categories_stores.append({
                'model': 'substitute.purchasestores',
                'pk': i + 1,
                'fields': {
                    'store_name': store['name']
                }
            })
        
        return stores

    def get_products(self, categories, stores):
        store_names = [store['name'] for store in stores]
        products_to_ignore = []
        i = 0
        for category in categories:
            url = f"https://fr.openfoodfacts.org/categorie/{category['name']}.json"
            res = requests.get(url)
            products = res.json()
            for product in products['products']:
                store = self.filter_store(product)
                if not store or product['product_name'] in products_to_ignore:
                    continue
                if store in store_names:
                    store_name = PurchaseStores.objects.get(store_name=store)
                    category_name = Categories.objects.get(category_name=category['name'])
                    self.data_products.append({
                        'model': 'substitute.products',
                        'pk': i + 1,
                        'fields': {
                            'product_name': product['product_name'],
                            'nutriscore': product['nutrition_grades_tags'][0],
                            'link': f"https://world.openfoodfacts.org/product/{product['code']}",
                            'details': self.generic_name(product),
                            'category': category_name.pk,
                            'purchase_store': store_name.pk
                        }
                    })
                    products_to_ignore.append(product['product_name'])
                    i += 1

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

    def write_category_store_data(self):
        path = 'substitute/fixtures/'
        with open(path + 'data_categories_stores.json', 'w', encoding='utf-8') as f0:
            json.dump(self.data_categories_stores, f0, ensure_ascii=False, indent=4)
    
    def write_products_data(self):
        path = 'substitute/fixtures/'
        with open(path + 'data_products.json', 'w', encoding='utf-8') as f1:
            json.dump(self.data_products, f1, ensure_ascii=False, indent=4)
