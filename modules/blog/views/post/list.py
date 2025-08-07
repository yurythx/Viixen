from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from ...domain.post import BlogPost
from ...services.post_service import PostService

class PostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = PostService()  # ✅ Já implementado corretamente
    
    def get_queryset(self):
        queryset = self.service.get_published_posts(self.request.company)
        
        # Busca
        search = self.request.GET.get('search')
        if search:
            queryset = self.service.search_posts(search, self.request.company)
        
        # Filtro por categoria
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = self.service.get_featured_posts(self.request.company, 3)
        context['recent_posts'] = self.service.get_recent_posts(self.request.company, 5)
        return context