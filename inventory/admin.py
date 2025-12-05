from django.contrib.admin.decorators import display
from django.contrib import admin
from .models import Category, Item,Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    prepopulated_fields = {'slug':('name',)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'quantity', 'is_low_stock_display','slug')
    # FILTERS: Sidebar filters for quick sorting
    list_filter = ('category', 'created_at')

    # SEARCH: Adds a search bar
    search_fields = ('name', 'sku')

    # EDITING: Edit these fields without opening the item
    list_editable = ('price', 'quantity')

    prepopulated_fields = {'slug':('name',)}
    @admin.display(description='Low Stock?', boolean=True)
    def is_low_stock_display(self,obj):
        return obj.is_low_stock



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display=['item','user','rating','created']
    list_filter=['rating']