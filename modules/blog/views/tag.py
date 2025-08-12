from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.mixins import CompanyAdminRequiredMixin, SuccessMessageMixin
from ..domain.post import Tag
from ..forms import TagForm


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'blog/tag/list.html'
    context_object_name = 'tags'
    paginate_by = 20
    
    def get_queryset(self):
        return Tag.objects.all().order_by('name')


class TagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'blog/tag/detail.html'
    context_object_name = 'tag'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class TagCreateView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag/form.html'
    success_url = reverse_lazy('blog:tag_list')
    success_message = 'Tag criada com sucesso!'


class TagUpdateView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag/form.html'
    context_object_name = 'tag'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = 'Tag atualizada com sucesso!'
    
    def get_success_url(self):
        return reverse_lazy('blog:tag_detail', kwargs={'slug': self.object.slug})


class TagDeleteView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, DeleteView):
    model = Tag
    template_name = 'blog/tag/confirm_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('blog:tag_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    delete_success_message = 'Tag excluída com sucesso!'
