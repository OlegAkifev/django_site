from django import template
import women.views as views

register = template.Library()


@register.simple_tag()
def get_categories():
    return views.categories_db


@register.inclusion_tag('women/list_categories.html')
def show_categories(category_selected=0):
    cats = views.categories_db
    return {'cats': cats, 'category_selected': category_selected}
