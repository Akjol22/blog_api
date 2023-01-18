from django.contrib import admin
from .models import Category, Tag, Post, Rating
# Register your models here.


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Rating)