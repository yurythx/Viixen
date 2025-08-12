from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from core.mixins import CompanyAdminRequiredMixin, SuccessMessageMixin
from ..domain.post import Category
from ..forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blog/category/list.html'
    context_object_name = 'categories'
    paginate_by = 12
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('name')


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'blog/category/detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class CategoryCreateView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category/form.html'
    success_url = reverse_lazy('blog:category_list')
    success_message = 'Categoria criada com sucesso!'


class CategoryUpdateView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category/form.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_message = 'Categoria atualizada com sucesso!'
    
    def get_success_url(self):
        return reverse_lazy('blog:category_detail', kwargs={'slug': self.object.slug})


class CategoryDeleteView(SuccessMessageMixin, LoginRequiredMixin, CompanyAdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'blog/category/confirm_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('blog:category_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    delete_success_message = 'Categoria excluída com sucesso!'
