from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from accounts.models.models import User, Badges, Hub, Batch
from accounts.models.models2 import Skill, SocialMedia, Project, EducationCategory
from ..serializers.userSerializer import (
    CombinedUserSerializer,
    SkillSerializer,
    SocialMediaSerializer,
    BadgeSerializer,
    ProjectSerializer,
    HubSerializer,
    BatchSerializer,
    EduCategorySerializer,
    AdminMessagesSerializer,
)
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from accounts.helpers import email_validator, create_jwt_pair_tokens
from django.contrib.auth import authenticate
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from superuser.models import AdminMessages


class DefaultPagination(PageNumberPagination):
    page_size = 3


class StudetsView(ListCreateAPIView):
    queryset = User.objects.filter(role="student")
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]  
    ordering_fields = ['fullname', 'username', 'email', 'dob']
    search_fields = ['fullname', 'username', 'email']
    pagination_class = DefaultPagination


class CouncellorsView(ListCreateAPIView):
    queryset = User.objects.filter(role="academic_counselor")
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['fullname', 'username', 'email']
    ordering_fields = ['fullname', 'username', 'email', 'dob']
    pagination_class = DefaultPagination


class AdminsView(ListCreateAPIView):
    queryset = User.objects.filter(role="brototype_admin")
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = DefaultPagination


class CoOrdinatorsView(ListCreateAPIView):
    queryset = User.objects.filter(role="review_coordinator")
    serializer_class = CombinedUserSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = DefaultPagination


class SkillsView(ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = DefaultPagination

class HubsView(ListCreateAPIView):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer
    pagination_class = DefaultPagination

class EduCategoriesView(ListCreateAPIView):
    queryset = EducationCategory.objects.all()
    serializer_class = EduCategorySerializer
    pagination_class = DefaultPagination

class BatchesView(ListCreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    pagination_class = DefaultPagination


class SocialMediaView(ListCreateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer


class EduCategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = EducationCategory.objects.all()
    serializer_class = EduCategorySerializer
    pagination_class = DefaultPagination
    lookup_field = 'id'


class SkillsViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = "id"


class HubViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer
    lookup_field = "id"


class BatchViewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    lookup_field = "id"


class SocialMediaDetail(RetrieveUpdateDestroyAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    lookup_field = "id"


class BadgesView(ListCreateAPIView):
    queryset = Badges.objects.all()
    serializer_class = BadgeSerializer
    pagination_class = DefaultPagination


class ProjectView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = DefaultPagination

class AdminMessageView(ListCreateAPIView):
    queryset = AdminMessages.objects.all()
    serializer_class = AdminMessagesSerializer


@api_view(["PUT"])
def block_user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return Response(data={"message": "User not found"}, status=404)
    if not user.is_active:
        return Response(data={"message": "User is already blocked"})
    else:
        user.is_active = False
        user.save()
    return Response(data={"message": "Blocked User successfully"})


@api_view(["PUT"])
def unblock_user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return Response(data={"message": "User not found"}, status=404)
    if user.is_active:
        return Response(data={"message": "User is not blocked"})
    else:
        user.is_active = True
        user.save()
    return Response(data={"message": "un Blocked User successfully"})


@api_view(["POST"])
@csrf_exempt
def admin_login(request):
    if request.method == "POST":
        email = request.data.get("email")
        password = request.data.get("password")
        if email and password:
            if not email_validator(email):
                return Response(
                    data={"message": "Invalid E-mail format", "status": 400}
                )
            else:
                username = authenticate(email=email, password=password)
                if username:
                    try:
                        user = User.objects.get(username=username)
                    except:
                        return JsonResponse(
                            data={"message": "Enter valid data", "status": 400}
                        )
                    if user.is_superuser:
                        token = create_jwt_pair_tokens(user)
                        return JsonResponse(data={"token": token}, status=202)
                    else:
                        return JsonResponse(
                            data={"message": "Credential is missing", "status": 400}
                        )
                else:
                    return JsonResponse(
                        data={"message": "Enter valid data", "status": 400}
                    )
        else:
            return JsonResponse(
                data={"message": "Credential is missing", "status": 400}
            )
    else:
        return JsonResponse(data={"detail": "is not allowed"}, status=405)
