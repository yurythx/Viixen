from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..domain.page import Page

class PageDetailView(LoginRequiredMixin, DetailView):
    model = Page
    template_name = 'pages/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'page'
    
    def get_queryset(self):
        return Page.objects.filter(
            is_published=True,
            company=self.request.company
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.request.company
        return context