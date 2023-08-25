from rest_framework import serializers
from accounts.models.models import UserProfile,User,Badges,Hub,Batch
from accounts.models.models2 import Skill,SocialMedia,Project,EducationCategory
from superuser.models import AdminMessages

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CombinedUserSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'fullname', 'username','email', 'role', 'is_verified', 'is_active', 'dob', 'is_profile_completed', 'user_profile')

    def get_user_profile(self, user):
        try:
            profile_instance = UserProfile.objects.get(user=user)
            return UserProfileSerializer(profile_instance).data
        except UserProfile.DoesNotExist:
            return None

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class EduCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationCategory
        fields = '__all__'

class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = '__all__'

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class AdminMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminMessages
        fields = '__all__'