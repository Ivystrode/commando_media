from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin
import uuid

#==========MODELS==========

class Notice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(upload_to='notice_pictures', default='notice_pictures/notice_default.jpeg')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
    slug = models.SlugField()
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return str(self.title) + ": " + str(self.created_by)

class NoticeComment(models.Model):
    parent = models.ForeignKey(Notice, on_delete=models.CASCADE,related_name='noticecomments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noticecomments')
    body = models.TextField()
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f'Comment by {self.author}: {self.body}'

#==========MODEL ADMIN==========

class NoticeCommentAdmin(admin.ModelAdmin):
    search_fields = ['author', 'parent']
    list_display = ['author', 'time', 'parent']

# Show comments inline with Notices (see ref1)
class NoticeCommentInline(admin.TabularInline):
    model = NoticeComment
    
class NoticeAdmin(admin.ModelAdmin):
    search_fields = ['title', 'created_by']
    list_display = ['title', 'created_by', 'time']
    inlines = [NoticeCommentInline] #ref1