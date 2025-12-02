from django.shortcuts import render, get_object_or_404
from .models import Item

def item_list(request):
    # Fetch all items
    items = Item.objects.all()
    
    # SENIOR TIP: Context Dictionary
    # This is how we pass data from Python to HTML.
    # We label the data 'items' so the HTML can find it.
    context = {
        'items': items
    }
    return render(request, 'inventory/item_list.html', context)

def item_detail(request, slug):
    # SENIOR PATTERN: get_object_or_404
    # We search for the item where the slug column matches the slug from the URL.
    # If not found, Django automatically raises a 404 "Page Not Found" error.
    # This prevents your site from crashing with a 500 error on bad links.
    item = get_object_or_404(Item, slug=slug)

    print("Item",item)
    
    context = {
        'item': item
    }
    return render(request, 'inventory/item_detail.html', context)