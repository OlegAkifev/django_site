from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, TagPost, UploadedFiles
from women.utils import DataMixin


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    category_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('category')


# def about(request):
#     contact_list = Women.published.all()
#     paginator = Paginator(contact_list, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#
#     return render(request, 'women/about.html',
#                   {'title': 'О сайте', 'page_obj': page_obj, 'menu': menu})

class AboutPage(DataMixin, ListView):
    template_name = 'women/about.html'
    title_page = 'О сайте'

    def get_queryset(self):
        return Women.published.all()


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ('title', 'content', 'photo', 'is_published', 'category')
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context,
                                      title='Категория - ' + category.name,
                                      category_selected=category.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тэг: ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')

