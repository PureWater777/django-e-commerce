
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db import transaction
from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem

# Create your views here.
from tags.models import TaggedItem

def say_hello(request):

    #product_query = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    #product_query = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # result_1 = Order.objects.aggregate(count=Count('id'))
    # result_2 = OrderItem.objects.filter(product__id=1).aggregate(units_sold = Sum('quantity'))
    # result_3 = Order.objects.filter(customer__id=1).aggregate(orders_by_customer = Count('id'))
    # result_4 = Product.objects.fileter(collection__id = 3).aggregate(min = Min('unit_price'), max = Max('unit_price'), average = Avg('unit_price'))
    # result_5 = OrderItem.objects.filter(product__collection_id=3)
    # result_6 = Product.objects.filter(id__in=OrderItem.objects.values(('product_id'))).distinct().order_by('title')
    # result_7 = Order.objects.aggregate(count=Count('id'))
    # result_8 = Product.objects.filter(collection_id=3).distinct().aggregate(count=Count('id'))
    result_9 = Product.objects.filter(collection_id='12').distinct().aggregate(count=Count('id'))
    # customers_orders_and_ids = Customer.objects.annotate(last_order_id=Max('order__id'))
    # collections_count = Collection.objects.annotate(product_count=Count('product'))
    # customers_more_than_5 = Customer.objects.annotate(order_count=Count('order')).filter(order_count_gt=5)

    #customers_amount_spent = Customer.objects.annotate(amount_spent=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity'))).order_by('-amount_spent')

    #custom_manager = TaggedItem.objects.get_tags_for(Product, 1)

    #shopping cart with products
    # cart = Cart()
    # cart.save()
    #
    # item_1 = CartItem()
    # item_1.cart = cart
    # item_1.product_id = 1
    # item_1.quantity = 1
    # item_1.save()
    #
    # item_2 = CartItem()
    # item_2.cart = cart
    # item_2.product_id = 2
    # item_2.quantity = 1
    # item_2.save()
    #
    # #update quantity
    # item_1 = CartItem.objects.get(pk=1)
    # item_1.quantity = 2
    # item_1.save()
    #
    # #delete cart
    # cart = Cart(pk=1)
    # cart.delete()

    #transactions

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 2
        item.unit_price = 70
        item.save()



    return render(request, 'hello.html', {'name': "wsad"})