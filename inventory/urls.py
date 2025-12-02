from django.urls import path
from . import views

app_name = 'inventory'  # Crucial for the {% url %} tag later

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('<slug:slug>/', views.item_detail, name='item_detail'),
]