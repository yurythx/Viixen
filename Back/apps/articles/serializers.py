from rest_framework import serializers
from .models import Article, Comment
from django.shortcuts import get_object_or_404

class RecursiveCommentSerializer(serializers.Serializer):
    """Para serializar recursivamente respostas dos comentários"""
    def to_representation(self, value):
        serializer = CommentSerializer(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveCommentSerializer(many=True, read_only=True)
    article_slug = serializers.CharField(write_only=True)
    parent_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'name', 'text', 'created_at', 'replies', 'parent', 'article_slug', 'parent_id']
        read_only_fields = ['id', 'created_at', 'parent']
        ref_name = "ArticlesCommentSerializer"
    
    def validate(self, data):
        article_slug = data.get('article_slug')
        parent_id = data.get('parent_id')
        
        # Validar que o artigo existe
        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise serializers.ValidationError({'article_slug': 'Artigo não encontrado.'})
        
        # Validar que o parent existe e pertence ao mesmo artigo
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
                if parent.article.slug != article_slug:
                    raise serializers.ValidationError({'parent_id': 'O comentário pai deve pertencer ao mesmo artigo.'})
            except Comment.DoesNotExist:
                raise serializers.ValidationError({'parent_id': 'Comentário pai não encontrado.'})
        
        return data
    
    def create(self, validated_data):
        article_slug = validated_data.pop('article_slug')
        parent_id = validated_data.pop('parent_id', None)
        
        article = Article.objects.get(slug=article_slug)
        validated_data['article'] = article
        
        if parent_id:
            validated_data['parent'] = Comment.objects.get(id=parent_id)
        
        return super().create(validated_data)

class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'created_at', 'comments', 'comments_count']
        read_only_fields = ['id', 'slug', 'created_at', 'comments_count']
    
    def get_comments(self, obj):
        # Retornar apenas comentários de alto nível (sem parent)
        top_level_comments = obj.comments.filter(parent=None)
        return CommentSerializer(top_level_comments, many=True, context=self.context).data
    
    def get_comments_count(self, obj):
        return obj.comments.count()