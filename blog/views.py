from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from blog.forms import BlogEntryForm
from catalog.views import MyBaseFooter
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import BlogEntry


class BlogIndexView(MyBaseFooter, ListView):
    """Отображение главной страницы блога"""
    model = BlogEntry
    template_name = 'blog/index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publications=True)
        return queryset


class BlogDetailView(MyBaseFooter, DetailView):
    """Отображение одной записи блога"""
    model = BlogEntry
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save(update_fields=['views'])
        return self.object


class BlogCreateView(MyBaseFooter, CreateView):
    """Страничка с созданием записи блога"""
    model = BlogEntry
    form_class = BlogEntryForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(MyBaseFooter, UpdateView):
    """Старничка с редактированием блога """
    model = BlogEntry
    form_class = BlogEntryForm
    success_url = reverse_lazy('blog:detail')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', args=[self.object.slug])


class BlogDeleteView(MyBaseFooter, DeleteView):
    """Страничка с удалением блога"""
    model = BlogEntry
    success_url = reverse_lazy('blog:index')
# Create your views here.