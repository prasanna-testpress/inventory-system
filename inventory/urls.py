from django.urls import path
from . import views

app_name = 'inventory'  # Crucial for the {% url %} tag later

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add/',views.item_create,name='item_create'),
    path('update/<slug:slug>',views.item_update,name='item_update'),
    path('delete/<slug:slug>',views.item_delete,name='item_delete'),

    path('<slug:slug>/', views.item_detail, name='item_detail'),
   
]