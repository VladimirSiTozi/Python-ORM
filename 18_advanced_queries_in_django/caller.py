import os
from pprint import pprint

import django
from django.db import connection
from django.db.models import Count, Avg, Sum, Value, CharField, Q, F
from django.db.models.functions import Concat

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


# Create and run queries
def add_records_to_database():
    # Categories
    food_category = Category.objects.create(name='Food')
    drinks_category = (Category.objects.create(name='Drinks'))

    # Food
    product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99, category=food_category, is_available=False)
    product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99, category=food_category, is_available=False)
    product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99, category=food_category, is_available=True)
    product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49, category=food_category, is_available=True)
    product5 = Product.objects.create(name='Pasta and Sauce Bundle', description='Package containing pasta and a jar of pasta sauce', price=6.99, category=food_category, is_available=False)
    product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99, category=food_category, is_available=True)
    product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs', price=3.49, category=food_category, is_available=True)
    product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99, category=food_category, is_available=False)
    product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49, category=food_category, is_available=True)

    # Drinks
    product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99, category=drinks_category, is_available=True)
    product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49, category=drinks_category, is_available=False)
    product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water', price=4.99, category=drinks_category, is_available=True)
    product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49, category=drinks_category, is_available=True)
    product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99, category=drinks_category, is_available=False)
    product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49, category=drinks_category, is_available=True)

    # Customers
    customer1 = Customer.objects.create(username='john_doe')
    customer2 = Customer.objects.create(username='alex_alex')
    customer3 = Customer.objects.create(username='peter132')
    customer4 = Customer.objects.create(username='k.k.')
    customer5 = Customer.objects.create(username='peter_smith')

    # Orders
    order1 = Order.objects.create(customer=customer1)
    order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
    order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
    order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
    order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)

    order2 = Order.objects.create(customer=customer3)
    order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
    order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)

    order3 = Order.objects.create(customer=customer1)
    order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
    order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
    return "All data entered!"


# Run and print your queries
# print(add_records_to_database())


# Available Products

# print('All Products:')
# print(Product.objects.all())
# print()
# print('All Available Products:')
# print(Product.objects.available_products())
# print()
# print('All Available Food Products:')
# print(Product.objects.available_products_in_category("Food"))


# **************************************************start
# ONLY / VALUES

# # normal
def normal_products():
    products = Product.objects.all()[:3]
    for p in products:
        print(p.name, p.price)
    pprint(connection.queries)

# normal_products()


# # only
def only_products():
    products = Product.objects.all().only('name', 'price')[:3]
    for p in products:
        print(p.name, p.price)
    pprint(connection.queries)

# only_products()


# # values
def values_products():
    products = Product.objects.all().values('name', 'price')[:3]
    pprint(products)
    pprint(connection.queries)

# values_products()


# AGGREGATE / ANNOTATE

# aggregate

def aggregate_products():
    all_products = Product.objects.aggregate(employees_count=Count('id'))
    print(all_products)

    all_foods = Product.objects.filter(category__name='Food').aggregate(all_foods_count=Count('id'))
    print(all_foods)

    avg_drink_price = Product.objects.filter(category__name='Drinks').aggregate(average_drink_price=Avg('price'))
    print(avg_drink_price)

    avg_food_price = Product.objects.filter(category__name='Food').aggregate(average_food_price=Avg('price'))
    print(avg_food_price)

# aggregate_products()


# annotate
def annotate_products():
    products = Product.objects.values('category__name').annotate(Avg('price'))
    pprint(products)

    all_products = (Product.objects.values('category__name', 'name', 'price')
                    .annotate(full_info=Concat('category__name', Value(' - '), 'name',
                                               Value(' -> '), 'price', output_field=CharField(max_length=100))))

    for p in all_products:
        print(p)
# **************************************************end


# Product Quantity Ordered

def product_quantity_ordered():
    orders = (OrderProduct.objects
              .values('product__name')
              .annotate(total=Sum('quantity'))
              .order_by('-total'))
    result = []

    for product in orders:
        result.append(f'Quantity ordered of {product["product__name"]}: {product["total"]}')

    return '\n'.join(result)

# print(product_quantity_ordered())


# **************************************************start
# SELECT RELATED, PREFETCH RELATED

def select_related():
    all_products = Product.objects.all().select_related('category')
    for p in all_products:
        print(p.name, p.price, p.category.name)

    pprint(connection.queries)


def prefetch_related_products():
    all_categories = Category.objects.prefetch_related('product_set')
    for category in all_categories:
        for product in category.product_set.all():
            print(product.name, product.price, category.name)

    pprint(connection.queries)


# select_related()
# prefetch_related_products()
# **************************************************end


# Ordered Products Per Customer
def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')
    result = []

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for product in order.orderproduct_set.all():
            result.append(f'- Product: {product.product.name}, Category: {product.product.category.name}')

    return '\n'.join(result)

# print(ordered_products_per_customer())

# **************************************************start
# Q and F Objects

# AND = &
# OR = |
# NOT = ~


# Q
def all_product_or():
    all_products = Product.objects.filter(Q(category__product__name__icontains='F') | Q(price__gte=5))
    for p in all_products:
        print(p.name, p.price, p.category.name)


def all_product_not():
    all_products = Product.objects.filter(~Q(category__product__name__icontains='F') & Q(price__gte=5))
    for p in all_products:
        print(p.name, p.price, p.category.name)


# all_product_or()
# all_product_not()


# F
def all_product_update_with_f():
    Product.objects.all().update(price=F('price') + 10)
    for p in Product.objects.all():
        print(p.name, p.price)


all_product_update_with_f()


# **************************************************end

# Available Products Prices
def filter_products():
    query = Q(is_available=True) & Q(price__gt=3)
    all_product = Product.objects.filter(query).order_by('-price', 'name')
    result = []

    for product in all_product:
        result.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(result)


# print(filter_products())


# Give Discounts
def give_discount():
    query = Q(is_available=True) & Q(price__gt=3)
    Product.objects.filter(query).update(price=F('price') * 0.70)

    available_products = Product.objects.filter(is_available=True).order_by('-price', 'name')
    result = []

    for product in available_products:
        result.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(result)


# print(give_discount())

