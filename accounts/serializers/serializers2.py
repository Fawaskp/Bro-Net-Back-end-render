from rest_framework.serializers import ModelSerializer, Serializer
from ..models.models2 import (
    Project,
    Skill,
    SocialMedia,
    UserSocialMediaAccounts,
    EducationCategory,
    UserEducation,
    WorkExperience,
    Follow,
)

"""
Serializers: 

UserSocialMediaAccounts
Project
Skill
SocialMedia
EducationCategory
UserEducation
WorkExperience
Message
"""

# class ProjectSerializer(ModelSerializer):
#     skills_used = SkillSerializer(many=True)
#     class Meta:
#         model = SocialMedia
#         fields = '__all__'


class SocialMediaSerializer(ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


class UserSocialMediaAccountsSerializer(ModelSerializer):
    social_media = SocialMediaSerializer()

    class Meta:
        model = UserSocialMediaAccounts
        fields = "__all__"


class UserSocialMediaAccountsUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserSocialMediaAccounts
        fields = "__all__"


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProjectSerializer(ModelSerializer):
    skills_used = SkillSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"


class WorkExperienceSerializer(ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = "__all__"


class EducationCategorySerializer(ModelSerializer):
    class Meta:
        model = EducationCategory
        fields = "__all__"


class UserEducationSerializer(ModelSerializer):
    category = EducationCategorySerializer()

    class Meta:
        model = UserEducation
        fields = "__all__"


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
