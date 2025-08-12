from django.utils.text import slugify
import unicodedata
import itertools


def custom_slugify(value):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    return slugify(value, allow_unicode=False)


class AutoSlugMixin:
    """
    A mixin that automatically generates a unique slug based on a source field.
    
    Usage:
        class MyModel(AutoSlugMixin, models.Model):
            name = models.CharField(max_length=100)
            slug = models.SlugField(unique=True, max_length=100)
            
            class Meta:
                abstract = True
                
            def __init__(self, *args, **kwargs):
                self.slug_source = 'name'  # Field to generate slug from
                self.slug_field = 'slug'   # Field to store the slug in
                super().__init__(*args, **kwargs)
    """
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        """
        Override save to automatically generate a unique slug if not provided.
        """
        if not getattr(self, self.slug_field):
            setattr(self, self.slug_field, self.generate_unique_slug())
        super().save(*args, **kwargs)
    
    def generate_unique_slug(self):
        """
        Generate a unique slug by appending a number if the slug already exists.
        """
        # Get the source text for the slug
        source_text = getattr(self, self.slug_source)
        slug = custom_slugify(source_text)
        
        # Get the model class
        model = self.__class__
        
        # If the slug is empty, use the model name
        if not slug:
            slug = model._meta.model_name
        
        # Make sure the slug is unique
        unique_slug = slug
        num = 1
        
        # Check if a model with this slug already exists
        while model._default_manager.filter(**{self.slug_field: unique_slug}).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
            
        return unique_slug
