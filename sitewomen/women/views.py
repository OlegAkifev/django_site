from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from wheel.vendored.packaging.tags import Tag

from women.models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'}, {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}, {'title': "Войти", 'url_name': 'login'}]


def index(request):
    posts = Women.published.all().select_related('category')
    data = {'title': 'Главная страница',
            'menu': menu,
            'post': posts,
            'category_selected': 0,
            }

    return render(request, 'women/index.html', context=data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'category_selected': 1,
    }

    return render(request, 'women/post.html', data)


def add_page(request):
    data = {'menu': menu, 'title': 'Добавление статьи'}
    return render(request, 'women/add_page.html', context=data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Women.published.filter(category_id=category.pk).select_related('category')
    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'post': posts,
            'category_selected': category.pk,
            }

    return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('category')
    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'post': posts,
        'category_selected': None,
    }

    return render(request, 'women/index.html', data)

