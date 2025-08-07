from django.db.models import QuerySet
from ..domain.post import BlogPost

class PostRepository:
    def get_all(self) -> QuerySet[BlogPost]:
        return BlogPost.objects.all()
    
    def get_published(self) -> QuerySet[BlogPost]:
        return BlogPost.objects.filter(status='published')
    
    def get_by_id(self, post_id: int) -> BlogPost:
        return BlogPost.objects.get(id=post_id)
    
    def get_by_slug(self, slug: str) -> BlogPost:
        return BlogPost.objects.get(slug=slug)
    
    def get_by_company(self, company) -> QuerySet[BlogPost]:
        return BlogPost.objects.filter(company=company)
    
    def create(self, **kwargs) -> BlogPost:
        return BlogPost.objects.create(**kwargs)
    
    def update(self, post_id: int, **kwargs) -> BlogPost:
        post = self.get_by_id(post_id)
        for key, value in kwargs.items():
            setattr(post, key, value)
        post.save()
        return post
    
    def delete(self, post_id: int) -> bool:
        try:
            post = self.get_by_id(post_id)
            post.delete()
            return True
        except BlogPost.DoesNotExist:
            return False