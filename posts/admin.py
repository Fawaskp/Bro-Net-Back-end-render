from django.contrib import admin
from .models import Post,VideoPost,ImagePost,ArticlePost,PostComment,PostLike,PollPost,PollPostRespond

admin.site.register(Post)
admin.site.register(VideoPost)
admin.site.register(ImagePost)
admin.site.register(ArticlePost)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(PollPost)
admin.site.register(PollPostRespond)
