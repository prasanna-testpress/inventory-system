from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Review
from .forms import ItemForm, ReviewForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required


def item_list(request):
    # Fetch all items
    items = Item.objects.all()

    # SENIOR TIP: Context Dictionary
    # This is how we pass data from Python to HTML.
    # We label the data 'items' so the HTML can find it.
    context = {"items": items}
    return render(request, "inventory/item_list.html", context)


def item_detail(request, slug):
    # SENIOR PATTERN: get_object_or_404
    # We search for the item where the slug column matches the slug from the URL.
    # If not found, Django automatically raises a 404 "Page Not Found" error.
    # This prevents your site from crashing with a 500 error on bad links.
    item = get_object_or_404(Item, slug=slug)
    # 1. Fetch existing reviews to display
    reviews = item.reviews.all().order_by("-created")  # Newest first

    # 2. Handle the Form Submission (POST)
    if request.method == "POST":
        # Security Check: Only logged-in users can post
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                # COMMIT=FALSE PATTERN
                # Create the object but don't save to DB yet
                review = form.save(commit=False)

                # Assign the missing data
                review.item = item
                review.user = request.user

                # Now save!
                review.save()

                # Refresh the page to show the new review
                return redirect("inventory:item_detail", slug=slug)
        else:
            # If a guest tries to hack a POST request, just redirect them
            return redirect("login")

    else:
        # 3. Handle the Page Load (GET)
        form = ReviewForm()

    context = {
        "item": item,
        "reviews": reviews,
        "form": form,
    }
    return render(request, "inventory/item_detail.html", context)


@login_required
def item_create(request):
    if request.method == "POST":
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
            return redirect("inventory:item_detail", slug=item.slug)
    else:
        # 2. User just visited the page (GET). Show empty form.
        form = ItemForm()

    return render(request, "inventory/item_form.html", {"form": form})


@login_required
def item_update(request, slug):

    item = get_object_or_404(Item, slug=slug)

    if request.method == "POST":
        # 1. User submitted data. Pass it to the form.
        form = ItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()

            # Success! Send them to the detail page of the new item.
            return redirect("inventory:item_detail", slug=item.slug)
    else:
        # 2. User just visited the page (GET). Show empty form.
        form = ItemForm(instance=item)

    return render(request, "inventory/item_form.html", {"form": form})


@login_required
def item_delete(request, slug):

    item = get_object_or_404(Item, slug=slug)

    if request.method == "POST":

        item.delete()
        return redirect("inventory:item_list")

    return render(request, "inventory/item_confirm_delete.html", {"item": item})


@login_required
def review_list(request):

    reviews = request.user.review_set.all()

    return render(request, "inventory/review/list.html", {"reviews": reviews})


@login_required
def review_update(request, id):

    review = get_object_or_404(Review, id=id,user=request.user)
    if request.method == "POST":

        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()

            # Success! Send them to the detail page of the new item.
            return redirect("inventory:reviews")

    else:
        form = ReviewForm(instance=review)

    return render(
        request, "inventory/review/form.html", {"form": form, "review": review}
    )


@login_required
def review_delete(request, id,):
    review = get_object_or_404(Review, id=id,user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("inventory:reviews")

    return render(
        request, "inventory/review/confirm_delete.html",{ "review": review}   )
