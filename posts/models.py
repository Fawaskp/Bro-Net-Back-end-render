from django.db import models
from accounts.models.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Banner(models.Model):
    heading = models.CharField(max_length=60, blank=True)
    content = models.CharField(max_length=250, blank=True)
    status = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Post(models.Model):
    """
    field "poll_subject" is only for model "PollPost"
    like count will be considered as the total response for PollPost (temp)
    """

    TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
        ("poll", "Poll"),
        ("article", "Article"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    description = models.TextField(null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    poll_subject = models.CharField(max_length=60, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.type} post of {self.user} ({self.id})"

class ImagePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image-post")

class VideoPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to="post-video")

class ArticlePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    heading = models.CharField(max_length=50,null=True)
    body = models.TextField()

class PollPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    option = models.CharField(max_length=50)
    respond_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return f"option '{self.option}' of {self.post}"

class PollPostRespond(models.Model):
    post_poll = models.ForeignKey(PollPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post_poll'], name='unique_user_poll_response')
        ]

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        unique_together = ["post", "comment", "user"]

    def __str__(self) -> str:
        return f"{self.user} commented on {self.post}"


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["post", "user"]

    def __str__(self) -> str:
        return f"{self.user} liked on {self.post}"


@receiver(post_save, sender=PollPostRespond)
def update_poll_post_respond_count(sender, instance, **kwargs):
    poll_post = instance.post_poll
    poll_post.respond_count = PollPostRespond.objects.filter(post_poll=poll_post).count()
    poll_post.save()

@receiver(post_save, sender=PostLike)
def update_post_like_count(sender, instance, **kwargs):
    post = instance.post
    post.like_count = PostLike.objects.filter(post=post).count()
    post.save()

@receiver(post_save, sender=PostComment)
def update_post_comments_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = PostComment.objects.filter(post=post).count()
    post.save()

@receiver(post_delete, sender=PollPostRespond)
def update_poll_post_respond_count_on_delete(sender, instance, **kwargs):
    poll_post = instance.post_poll
    poll_post.respond_count = PollPostRespond.objects.filter(post_poll=poll_post).count()
    poll_post.save()

@receiver(post_delete, sender=PostLike)
def update_post_like_count_on_delete(sender, instance, **kwargs):
    post = instance.post
    post.like_count = PostLike.objects.filter(post=post).count()
    post.save()

@receiver(post_delete, sender=PostComment)
def update_post_comments_count_on_delete(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = PostComment.objects.filter(post=post).count()
    post.save()