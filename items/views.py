from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from bson.objectid import ObjectId
import datetime

from .forms import ItemForm
from .models import Item
from .db import get_collection_handle
from users.models import UserProfile

def items_list(request):
    collection, client = get_collection_handle('items')
    search_query = request.GET.get('search', '')
    
    # Build the query
    if search_query:
        query = {'name': {'$regex': search_query, '$options': 'i'}}
    else:
        query = {}
    
    # Get all items that match the query
    items_data = collection.find(query).sort('created_at', -1)
    items = [Item.from_mongo(item) for item in items_data]
    
    # Pagination
    paginator = Paginator(items, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'items/items_list.html', context)

@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            
            # Create new item
            item = Item(
                name=name,
                description=description,
                price=price,
                image=image,
                user_id=request.user.id,
                username=request.user.username,
                created_at=datetime.datetime.now()
            )
            
            # Save to MongoDB
            collection, client = get_collection_handle('items')
            collection.insert_one(item.to_mongo())
            client.close()
            
            # Update user's post count and badge level if they're a Google user
            try:
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                if profile.is_google_user:
                    profile.post_count += 1
                    profile.calculate_badge_level()
            except Exception as e:
                print(f"Error updating badge: {e}")
            
            return redirect('items_list')
    else:
        form = ItemForm()
    
    return render(request, 'items/item_form.html', {'form': form, 'action': 'Create'})

@login_required
def update_item(request, item_id):
    collection, client = get_collection_handle('items')
    item_data = collection.find_one({'_id': ObjectId(item_id)})
    
    if not item_data:
        return redirect('items_list')
    
    item = Item.from_mongo(item_data)
    
    # Ensure user can only edit their own items
    if str(item.user_id) != str(request.user.id):
        return redirect('items_list')
    
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # Update item
            item.name = form.cleaned_data['name']
            item.description = form.cleaned_data['description']
            item.price = form.cleaned_data['price']
            item.image = form.cleaned_data['image']
            
            # Save to MongoDB
            collection.update_one(
                {'_id': ObjectId(item_id)},
                {'$set': item.to_mongo()}
            )
            client.close()
            
            return redirect('items_list')
    else:
        form = ItemForm(initial={
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'image': item.image
        })
    
    return render(request, 'items/item_form.html', {'form': form, 'action': 'Update', 'item': item})

@login_required
def delete_item(request, item_id):
    collection, client = get_collection_handle('items')
    item_data = collection.find_one({'_id': ObjectId(item_id)})
    
    if not item_data:
        return redirect('items_list')
    
    item = Item.from_mongo(item_data)
    
    # Ensure user can only delete their own items
    if str(item.user_id) != str(request.user.id):
        return redirect('items_list')
    
    if request.method == 'POST':
        collection.delete_one({'_id': ObjectId(item_id)})
        client.close()
        return redirect('items_list')
    
    return render(request, 'items/confirm_delete.html', {'item': item})

def item_detail(request, item_id):
    collection, client = get_collection_handle('items')
    item_data = collection.find_one({'_id': ObjectId(item_id)})
    
    if not item_data:
        return redirect('items_list')
    
    item = Item.from_mongo(item_data)
    return render(request, 'items/item_detail.html', {'item': item})
