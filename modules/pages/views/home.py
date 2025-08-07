from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...blog.domain.post import BlogPost
from ...blog.services.post_service import PostService

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if hasattr(self.request, 'company') and self.request.company:
            service = PostService()
            context['recent_posts'] = service.get_recent_posts(self.request.company, 4)
            context['featured_posts'] = service.get_featured_posts(self.request.company, 3)
        
        return context