import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order
from django.db.models import Q, Count, F, Case, When, Value, BooleanField

# Create queries within functions

# print(Profile.objects.get_regular_customers())


def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    query = (Q(full_name__icontains=search_string) | Q(email__icontains=search_string) | Q(phone_number__icontains=search_string))

    profiles = Profile.objects.filter(query).order_by('full_name')

    if not profiles.exists():
        return ''

    result = []

    for p in profiles:
        result.append(f'Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, '
                      f'orders: {p.orders.count()}')

    return '\n'.join(result)


# print(get_profiles('+359'))


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ''

    result = []

    for p in profiles:
        result.append(f'Profile: {p.full_name}, orders: {p.orders.count()}')

    return '\n'.join(result)


# print(get_loyal_profiles())


def get_last_sold_products():
    last_order = Order.objects.prefetch_related('products').last()

    if last_order is None or not last_order.products.exists():
        return ''

    products = ', '.join(last_order.products.order_by('name').values_list('name', flat=True))

    return f"Last sold products: {products}"

#
# print(get_last_sold_products())


def get_top_products():
    products = (Product.objects
                .annotate(orders_count=Count('order'))
                .filter(orders_count__gt=0)
                .order_by('-orders_count', 'name'))[:5]

    if not products:
        return ''

    result = []

    for p in products:
        result.append(f'{p.name}, sold {p.orders_count} times')

    products_text_result = '\n'.join(result)

    return f'Top products:\n{products_text_result}'


print(get_top_products())


def apply_discounts():
    orders = (Order.objects.prefetch_related('products')
              .filter(is_completed=False, products__gt=2)
              ).update(total_price=F('total_price') * 0.90)

    return f'Discount applied to {orders} orders.'

#
# print(apply_discounts())


def complete_order():
    unfinished_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not unfinished_order:
        return ""

    # for product in unfinished_order.product.all():
    #     product.in_stock -= 1
    #
    #     if product.in_stock == 0:
    #         product.is_available = False
    #
    #     product.save()

    unfinished_order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    unfinished_order.is_completed = True
    unfinished_order.save()

    return "Order has been completed!"


