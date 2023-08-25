from django.urls import path
from .views_github_proxy import get_access_token,get_user_data
from .views_login import (
    LoginWithSocialMedia,
    LoginWithEmail,
    token,
    check_username,
    is_user_auth,
    is_su_auth,
    get_user_id_by_username,
    send_otp_for_change_mail,
    verify_otp_for_change_mail,
)
from .views import (
    SearchUser,
    ViewUserProfile,
    UserProfileDetail,
    GetHubList,
    GetBatchList,
    GetStackList,
    UserDetail,
    DosView,
    DontsView,
    DosDetailView,
    DontsDetailView,
    PreviousMessagesView,
    ChatListView,
)
from .views2 import (
    SkillView,
    SocialMediaView,
    SkillDetail,
    ProjectViewSet,
    UserSocialMediaAccountsView,
    UserSocialMediaAccountsDetailView,
    UserEducationView,
    UserEducationDetail,
    WorkExperienceView,
    EducationCategoriesView,
    FollowView,
)


urlpatterns = [

    path('get_access_token/', get_access_token),
    path('get_user_data/', get_user_data),

    path("search/<int:user_id>/", SearchUser.as_view()),
    path("profile/", ViewUserProfile.as_view()),
    path("login/email/", LoginWithEmail.as_view()),
    path("login/social-media/", LoginWithSocialMedia.as_view()),
    path("user/<int:id>/", UserDetail.as_view()),
    path("user-profile/<int:id>/", UserProfileDetail.as_view()),

    path("hub", GetHubList.as_view()),
    path("batch", GetBatchList.as_view()),
    path("stack", GetStackList.as_view()),
    path("skill", SkillView.as_view()),
    
    path("user-skill-detail/<int:id>/", SkillDetail.as_view()),
    path("project/<int:user_id>/", ProjectViewSet.as_view({"get": "list"})),
    path("social-media", SocialMediaView.as_view()),
    path("user-work-experience", WorkExperienceView.as_view()),
    path("user-social-media", UserSocialMediaAccountsView.as_view()),
    path("user-social-media-detail/<int:id>/", UserSocialMediaAccountsDetailView.as_view()),
    path("education-categories", EducationCategoriesView.as_view()),
    path("user-education", UserEducationView.as_view()),
    path("user-education-detail/<int:id>/", UserEducationDetail.as_view()),

    path("dos/<int:user_id>/", DosView.as_view()),
    path("donts/<int:user_id>/", DontsView.as_view()),
    path("dos-detail/<int:id>/", DosDetailView.as_view()),
    path("donts-detail/<int:id>/", DontsDetailView.as_view()),
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),
    path("chat-list/<int:user_id>/", ChatListView.as_view()),

    path("token/", token),
    path("check-username/<str:username>/", check_username),
    path("get-user-id/<str:username>/", get_user_id_by_username),
    path("is-user-auth", is_user_auth),
    path("is-su-auth", is_su_auth),
    path("otp-for-change-email", send_otp_for_change_mail),
    path("verify-change-email-otp", verify_otp_for_change_mail),
    path("follow/<int:user1>/<int:user2>/", FollowView.as_view()),
]
