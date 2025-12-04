from django.shortcuts import render, get_object_or_404,redirect
from .models import Item
from .forms import ItemForm
from django.utils.text import slugify
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



def item_create(request):
    if request.method == 'POST':
        # 1. User submitted data. Pass it to the form.
        form = ItemForm(request.POST)
        
        if form.is_valid():
            # SENIOR LOGIC: "commit=False"
            # We pause saving because we need to add data the user didn't provide.
            item = form.save(commit=False)
            
            # Auto-generate the SKU and Slug
            # (In a real app, you'd use a better random generator for SKU)
            item.sku = slugify(item.name).upper() + "-001" 
            item.slug = slugify(item.name)
            
            # Now we save to DB
            item.save()
            
            # Success! Send them to the detail page of the new item.
            return redirect('inventory:item_detail', slug=item.slug)
    else:
        # 2. User just visited the page (GET). Show empty form.
        form = ItemForm()

    return render(request, 'inventory/item_form.html', {'form': form})




def item_update(request,slug):
    print("slug -------------------------",slug)

    item=get_object_or_404(Item,slug=slug)

    if request.method == 'POST':
        # 1. User submitted data. Pass it to the form.
        form = ItemForm(request.POST,instance=item)
        
        if form.is_valid():            
            form.save()

            # Success! Send them to the detail page of the new item.
            return redirect('inventory:item_detail', slug=item.slug)
    else:
        # 2. User just visited the page (GET). Show empty form.
        form = ItemForm(instance=item)

    return render(request, 'inventory/item_form.html', {'form': form})
