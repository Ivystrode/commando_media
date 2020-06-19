from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin
import uuid

#==========MODELS==========

class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(upload_to='idea_pictures', default='idea_pictures/idea_default.jpeg')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    slug = models.SlugField()
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.title) + ": " + str(self.created_by)

class IdeaComment(models.Model):
    parent = models.ForeignKey(Idea, on_delete=models.CASCADE,related_name='ideacomments')
    author = models.CharField(max_length=150)
    body = models.TextField()
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f'Comment by {self.author}: {self.body}'

#==========MODEL ADMIN==========

class IdeaCommentAdmin(admin.ModelAdmin):
    search_fields = ['author', 'parent']
    list_display = ['author', 'time', 'parent']

# Show comments inline with ideas (see ref1)
class IdeaCommentInline(admin.TabularInline):
    model = IdeaComment
    
class IdeaAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_by']
    list_display = ['title', 'created_by', 'time']
    inlines = [IdeaCommentInline] #ref1
