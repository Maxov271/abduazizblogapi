from rest_framework import viewsets, generics, permissions
from rest_framework.authentication import TokenAuthentication

from .models import (
    SiteSettings, Profile, SocialLink, Service, InsideWorldCard, InsideWorldItem,
    SkillGroup, JourneyEntry, PortfolioCategory, Project, ProjectGalleryImage, Tag,
    BlogPost, Comment, ContactMessage, TeamMember, StudentCategory, Student, SiteStats,
)
from .admin_serializers import (
    SiteSettingsAdminSerializer, ProfileAdminSerializer, SocialLinkAdminSerializer,
    ServiceAdminSerializer, InsideWorldCardAdminSerializer, InsideWorldItemAdminSerializer,
    SkillGroupAdminSerializer, JourneyEntryAdminSerializer, PortfolioCategoryAdminSerializer,
    TagAdminSerializer, ProjectAdminSerializer, ProjectGalleryImageAdminSerializer,
    BlogPostAdminSerializer, CommentAdminSerializer, ContactMessageAdminSerializer,
    TeamMemberAdminSerializer, StudentCategoryAdminSerializer, StudentAdminSerializer,
    SiteStatsAdminSerializer,
)


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class BaseAdminViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffUser]


# ---- Singletons ----
class SiteSettingsAdminView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffUser]
    serializer_class = SiteSettingsAdminSerializer

    def get_object(self):
        return SiteSettings.load()


class ProfileAdminView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffUser]
    serializer_class = ProfileAdminSerializer

    def get_object(self):
        return Profile.load()


# ---- Standard CRUD ----
class SocialLinkAdminViewSet(BaseAdminViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkAdminSerializer


class ServiceAdminViewSet(BaseAdminViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceAdminSerializer


class InsideWorldCardAdminViewSet(BaseAdminViewSet):
    queryset = InsideWorldCard.objects.all()
    serializer_class = InsideWorldCardAdminSerializer


class InsideWorldItemAdminViewSet(BaseAdminViewSet):
    queryset = InsideWorldItem.objects.all()
    serializer_class = InsideWorldItemAdminSerializer


class SkillGroupAdminViewSet(BaseAdminViewSet):
    queryset = SkillGroup.objects.all()
    serializer_class = SkillGroupAdminSerializer


class JourneyEntryAdminViewSet(BaseAdminViewSet):
    queryset = JourneyEntry.objects.all()
    serializer_class = JourneyEntryAdminSerializer


class PortfolioCategoryAdminViewSet(BaseAdminViewSet):
    queryset = PortfolioCategory.objects.all()
    serializer_class = PortfolioCategoryAdminSerializer


class TagAdminViewSet(BaseAdminViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagAdminSerializer


class ProjectAdminViewSet(BaseAdminViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectAdminSerializer


class ProjectGalleryImageAdminViewSet(BaseAdminViewSet):
    queryset = ProjectGalleryImage.objects.all()
    serializer_class = ProjectGalleryImageAdminSerializer


class BlogPostAdminViewSet(BaseAdminViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostAdminSerializer


class CommentAdminViewSet(BaseAdminViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentAdminSerializer
    http_method_names = ["get", "patch", "delete", "head", "options"]


class ContactMessageAdminViewSet(BaseAdminViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageAdminSerializer
    http_method_names = ["get", "patch", "delete", "head", "options"]


class TeamMemberAdminViewSet(BaseAdminViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberAdminSerializer


class StudentCategoryAdminViewSet(BaseAdminViewSet):
    queryset = StudentCategory.objects.all()
    serializer_class = StudentCategoryAdminSerializer


class StudentAdminViewSet(BaseAdminViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentAdminSerializer


class SiteStatsAdminView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffUser]
    serializer_class = SiteStatsAdminSerializer

    def get_object(self):
        return SiteStats.load()
