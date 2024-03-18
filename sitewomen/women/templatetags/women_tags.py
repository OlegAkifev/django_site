from django import template
from wheel.vendored.packaging.tags import Tag

import women.views as views
from women.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(category_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'category_selected': category_selected}


@register.inclusion_tag('women/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all()}

