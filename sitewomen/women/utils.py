menu = [{'title': "О сайте", 'url_name': 'about'}, {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}, {'title': "Войти", 'url_name': 'login'}]


class DataMixin:
    paginate_by = 4

    title_page = None
    category_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.category_selected is not None:
            self.extra_context['category_selected'] = self.category_selected

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['category_selected'] = None
        context.update(kwargs)
        return context
