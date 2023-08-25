from django.urls import path
from .views.userViews import (
    StudetsView,
    CouncellorsView,
    AdminsView,
    CoOrdinatorsView,
    EduCategoriesView,
    SkillsView,
    HubsView,
    BatchesView,
    SocialMediaView,
    EduCategoryDetailView,
    SkillsViewDetail,
    HubViewDetail,
    BatchViewDetail,
    SocialMediaDetail,
    BadgesView,
    ProjectView,
    AdminMessageView,
    admin_login,
    block_user,
    unblock_user,
)

urlpatterns = [

    path("login", admin_login),
    path("students/", StudetsView.as_view()),
    path("councellors/", CouncellorsView.as_view()),
    path("admins/", AdminsView.as_view()),
    path("block-user/<int:id>/", block_user),
    path("unblock-user/<int:id>/", unblock_user),
    path("co-ordinator/", CoOrdinatorsView.as_view()),

    path("skills/", SkillsView.as_view()),
    path("hubs/", HubsView.as_view()),
    path("education-categories/", EduCategoriesView.as_view()),
    path("batches/", BatchesView.as_view()),
    path("social-media/", SocialMediaView.as_view()),
    path("badges/", BadgesView.as_view()),
    path("projects/", ProjectView.as_view()),
    path("admin-messages/", AdminMessageView.as_view()),

    path("education-categories/<int:id>/", EduCategoryDetailView.as_view()),
    path("skill/<int:id>/", SkillsViewDetail.as_view()),
    path("hub/<int:id>/", HubViewDetail.as_view()),
    path("batch/<int:id>/", BatchViewDetail.as_view()),
    path("social-media/<int:id>/", SocialMediaDetail.as_view()),
    
]
