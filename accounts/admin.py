from django.contrib import admin
from .models.models import User, Badges, Hub, UserProfile, Batch, LoginWithEmailData, Stack
from .models.models2 import (
    Skill,
    Project,
    SocialMedia,
    Follow,
    UserSocialMediaAccounts,
    EducationCategory,
    UserEducation,
    WorkExperience,
    Dos,
    Donts,
    Message,
)

admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(SocialMedia)
admin.site.register(Follow)

admin.site.register(User)
admin.site.register(Hub)
admin.site.register(UserProfile)
admin.site.register(Badges)
admin.site.register(Batch)
admin.site.register(LoginWithEmailData)
admin.site.register(Stack)
admin.site.register(UserSocialMediaAccounts)
admin.site.register(EducationCategory)
admin.site.register(UserEducation)
admin.site.register(WorkExperience)
admin.site.register(Dos)
admin.site.register(Donts)
admin.site.register(Message)

