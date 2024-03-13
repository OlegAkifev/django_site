from django import template
import women.views as views
from women.models import Category

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_categories(category_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'category_selected': category_selected}


