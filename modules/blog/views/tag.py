from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from core.mixins import CompanyAdminRequiredMixin
from ..domain.post import Tag
from ..forms import TagForm


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'blog/tag/list.html'
    context_object_name = 'tags'
    paginate_by = 24
    ordering = ['name']


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'blog/tag/detail.html'
    context_object_name = 'tag'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class TagCreateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag/form.html'
    success_url = reverse_lazy('blog:tag_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tag criada com sucesso!')
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, CompanyAdminRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag/form.html'
    context_object_name = 'tag'
    
    def get_success_url(self):
        return reverse_lazy('blog:tag_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        messages.success(self.request, 'Tag atualizada com sucesso!')
        return super().form_valid(form)


class TagDeleteView(LoginRequiredMixin, CompanyAdminRequiredMixin, DeleteView):
    model = Tag
    template_name = 'blog/tag/confirm_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('blog:tag_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tag excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
