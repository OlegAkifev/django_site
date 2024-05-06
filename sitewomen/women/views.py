from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from wheel.vendored.packaging.tags import Tag

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadedFiles

menu = [{'title': "О сайте", 'url_name': 'about'}, {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}, {'title': "Войти", 'url_name': 'login'}]


class WomenHome(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница',
                     'menu': menu,
                     'category_selected': 0,
                     }

    def get_queryset(self):
        return Women.published.all().select_related('category')


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadedFiles(file=form.cleaned_data['file'])
            fp.save()

    else:
        form = UploadFileForm()

    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {'menu': menu,
#                 'form': form,
#                 'title': 'Добавление статьи'}
#
#         return render(request, 'women/add_page.html', context=data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#
#         data = {'menu': menu,
#                 'form': form,
#                 'title': 'Добавление статьи'
#                 }
#
#         return render(request, 'women/add_page.html', context=data)

class AddPage(FormView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)




def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     posts = Women.published.filter(category_id=category.pk).select_related('category')
#     data = {'title': f'Рубрика: {category.name}',
#             'menu': menu,
#             'post': posts,
#             'category_selected': category.pk,
#             }
#
#     return render(request, 'women/index.html', context=data)


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        context['title'] = 'Категория - ' + category.name
        context['menu'] = menu
        context['post'] = Women.objects.all().select_related('category')
        context['category_selected'] = category.pk
        print(context['posts'][0].category)
        return context


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


class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тэг: ' + tag.tag
        context['menu'] = menu
        context['category_selected'] = None
        print(tag)
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')


