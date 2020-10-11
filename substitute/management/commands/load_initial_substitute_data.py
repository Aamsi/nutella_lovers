from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

import requests
import json

from substitute.models import Categories, PurchaseStores, Products


class Command(BaseCommand):
    help = "Load initial data"

    def add_arguments(self, parser):
        parser.add_argument('-d', '--delete', action='store_true', help='Delete all rows in database')
        parser.add_argument('count', type=int, help='Indicates the number of instances to be created')

    def handle(self, *args, **options):
        delete = options['delete']
        count = options['count']
        opf = Openfoodfacts()
        if delete:
            return opf.delete_all()
        opf.insert_categories(count)
        opf.insert_stores(count)
        opf.insert_products()



class Openfoodfacts():
    # Pour tester: Faire des fichiers json avec une ou 2 cat par ex 
    def __init__(self):
        self.categories_url = "https://fr.openfoodfacts.org/categories&json=1"
        self.stores_url = "https://fr.openfoodfacts.org/stores&json=1"

    def insert_categories(self, count):
        res = requests.get(self.categories_url)
        categories = res.json()['tags'][:count]
        for category in categories:
            Categories.objects.get_or_create(
                name=category['name'],
                en_id=category['id']
            )

    def insert_stores(self, count):
        res = requests.get(self.stores_url)
        stores = res.json()['tags'][:count]
        for store in stores:
            PurchaseStores.objects.get_or_create(name=store['name'])

    def insert_products(self):
        stores = PurchaseStores.objects.all()
        categories = Categories.objects.all()

        store_names = [store.name for store in stores]

        products_to_ignore = []

        for category in Categories.objects.all():
            url = f"https://fr.openfoodfacts.org/categorie/{category.name}.json"
            res = requests.get(url)
            products = res.json()
            for product in products['products']:
                store = self.filter_store(product)
                if product['product_name'] in products_to_ignore:
                    continue
                if store not in store_names:
                    continue
                store_instance = PurchaseStores.objects.get(name=store)
                product_added = Products.objects.update_or_create(
                    name=product['product_name'],
                    nutriscore=product['nutrition_grades_tags'][0],
                    barcode=product['code'],
                    details=self.generic_name(product),
                    purchase_store=store_instance,
                    thumbnail=self.get_thumbnail(product)
                )
                self.add_categories(product, product_added[0])

                products_to_ignore.append(product['product_name'])

    def add_categories(self, product, product_added):
        for en_id in product['categories_tags']:
            try:
                cat = Categories.objects.get(en_id=en_id)
            except ObjectDoesNotExist:
                continue
            product_added.categories.add(cat)

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
    
    def get_thumbnail(self, product):
        try:
            return product['image_thumb_url']
        except KeyError:
            return None

    def delete_all(self):
        stores = PurchaseStores.objects.all()
        categories = Categories.objects.all()
        products = Products.objects.all()
        stores.delete()
        categories.delete()
        products.delete()
