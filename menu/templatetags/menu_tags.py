from django import template
from django.db import models
from menu.models import MenuItem, Menu

register = template.Library()

def get_parents(item):
    parents = []
    while item.parent:
        parents.insert(0, item.parent)
        item = item.parent
    return parents

def get_children(item, parent_items):
    return parent_items.get(item.id, [])

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path

    menu = Menu.objects.prefetch_related(
        models.Prefetch('items',
                        queryset=MenuItem.objects.select_related('parent').order_by('id'))
    ).filter(name=menu_name).first()

    if not menu:
        return []

    active_item = None
    items_by_parent = {}
    for item in menu.items.all():
        if item.get_url() == current_url:
            active_item = item
        parent_id = item.parent_id if item.parent else None
        if parent_id not in items_by_parent:
            items_by_parent[parent_id] = []
        items_by_parent[parent_id].append(item)

    if not active_item:
        return []

    parents = get_parents(active_item)

    tree = [{'child': parent, 'is_active': True, 'children': []} for parent in parents]

    tree.append({
        'child': active_item,
        'is_active': True,
        'children': get_children(active_item, items_by_parent)
    })

    return tree
