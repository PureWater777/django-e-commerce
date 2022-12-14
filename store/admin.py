from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Filters
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            queryset.filter(inventory__gte=10)


class CostFilter(admin.SimpleListFilter):
    title = 'cost'
    parameter_name = 'unit_price'

    def lookups(self, request, model_admin):
        return [
            ('<5', 'Very Low'),
            ('>=10', 'Medium')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<5':
           return queryset.filter(unit_price__lt=5)
        if self.value() == '>=10':
           return queryset.filter(unit_price__gte=10)


# Models registration
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['product']
    exclude = ['promotions']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter, CostFilter]
    list_per_page = 20
    list_select_related = ['collection']


    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'OK'

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description='Clear inventory items')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were updated.',
            messages.INFO
        )

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
                reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
            'collection__id': str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
# Inlines child augmentation

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 5

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']
    ordering = ['customer']
    list_select_related = ['customer']



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    autocomplete_fields = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 20
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
            'customer__id': str(customer.id)
        }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order'))




