from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from core.mixins import CompanyFilterMixin, CompanyAdminRequiredMixin
from ..domain.page import Page
from ..forms import PageForm


class PageListView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, ListView):
    model = Page
    template_name = 'pages/list.html'
    context_object_name = 'pages'
    paginate_by = 12
    ordering = ['-created_at']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        context.update({
            'total_pages': queryset.count(),
            'published_pages': queryset.filter(is_published=True).count(),
            'draft_pages': queryset.filter(is_published=False).count(),
            'pages_this_month': queryset.filter(
                created_at__month=self.request.user.date_joined.month
            ).count(),
        })
        return context


class PageCreateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/form.html'
    success_url = reverse_lazy('pages:page_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.company = self.request.company
        messages.success(self.request, 'Página criada com sucesso!')
        return super().form_valid(form)


class PageUpdateView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, UpdateView):
    model = Page
    form_class = PageForm
    template_name = 'pages/form.html'
    context_object_name = 'page'
    
    def get_success_url(self):
        return reverse_lazy('pages:page_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        messages.success(self.request, 'Página atualizada com sucesso!')
        return super().form_valid(form)


class PageDeleteView(LoginRequiredMixin, CompanyAdminRequiredMixin, CompanyFilterMixin, DeleteView):
    model = Page
    template_name = 'pages/confirm_delete.html'
    context_object_name = 'page'
    success_url = reverse_lazy('pages:page_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Página excluída com sucesso!')
        return super().delete(request, *args, **kwargs)
