from django.contrib import admin
from .models import Category, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    prepopulated_fields = {'slug':('name',)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'quantity', 'is_low_stock_display')
    # FILTERS: Sidebar filters for quick sorting
    list_filter = ('category', 'created_at')

    # SEARCH: Adds a search bar
    search_fields = ('name', 'sku')

    # EDITING: Edit these fields without opening the item
    list_editable = ('price', 'quantity')

    @admin.display(description='Low Stock?', boolean=True)
    def is_low_stock_display(self,obj):
        return obj.is_low_stock