from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F

from core.mixins import CompanyFilterMixin
from ...domain.post import BlogPost


class PostDetailView(LoginRequiredMixin, CompanyFilterMixin, DetailView):
    """
    View for displaying a single blog post.
    Uses slug for URL pattern and increments the view count on each view.
    """
    model = BlogPost
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """
        Get the queryset, ensuring we only show posts for the current company.
        """
        return super().get_queryset().select_related('author', 'category')
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