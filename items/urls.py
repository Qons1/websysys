from django.urls import path
from . import views

urlpatterns = [
    path('', views.items_list, name='items_list'),
    path('create/', views.create_item, name='create_item'),
    path('detail/<str:item_id>/', views.item_detail, name='item_detail'),
    path('update/<str:item_id>/', views.update_item, name='update_item'),
    path('delete/<str:item_id>/', views.delete_item, name='delete_item'),
] 