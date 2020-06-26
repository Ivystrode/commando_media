from django.contrib import admin
from .models import Idea, IdeaAdmin, IdeaComment, IdeaCommentAdmin, IdeaCommentInline

# Register your models here.
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaComment, IdeaCommentAdmin)