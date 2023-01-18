from rest_framework import serializers

from .models import Post, Category, Tag, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Post
        fields = '__all__'
    
    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('Такой заголовок уже существует')
        return title

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            Comment.objects.filter(post=instance.pk),
            many=True
        ).data
        return representation


class PostListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment

    class Meta:
        model = Comment
        fields = '__all__'