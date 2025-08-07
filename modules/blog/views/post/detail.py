from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ...domain.post import BlogPost
from ...services.post_service import PostService

class PostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'blog/post/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = PostService()
    
    def get_object(self, queryset=None):
        post = get_object_or_404(
            BlogPost,
            slug=self.kwargs['slug'],
            status='published',
            company=self.request.company
        )
        
        # Incrementar visualizações
        self.service.increment_post_views(post.id)
        
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = self.service.get_related_posts(self.object, 4)
        return context