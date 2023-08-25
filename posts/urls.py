from django.urls import path
from .views import (
    PostImage,
    PostVideo,
    GetAllPost,
    PostCommentsView,
    PostLikeView,
    PostPoll,
    PostArticle,
    PollPostRespondView,
    BannerView,
    BannerDetailView,
    like_post,
    un_like_post,
    get_active_banner,
)

urlpatterns = [
    path("post-image/", PostImage.as_view()),
    path("post-video/", PostVideo.as_view()),
    path("post-poll/", PostPoll.as_view()),
    path("post-article/", PostArticle.as_view()),
    path("poll-post-respond/", PollPostRespondView.as_view()),
    path("banners/", BannerView.as_view()),
    path("banner-detail/<int:id>/", BannerDetailView.as_view()),
    path("get-posts/<int:user_id>/", GetAllPost.as_view()),
    path("comments/<int:post_id>/", PostCommentsView.as_view()),
    path("like-post/",PostLikeView.as_view()),
    path("un-like-post/",un_like_post),

    path("like-post/<int:id>/", like_post),
    path("get-active-banner/", get_active_banner),
]
