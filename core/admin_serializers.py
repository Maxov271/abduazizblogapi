from rest_framework import serializers
from .models import (
    SiteSettings, Profile, SocialLink, Service, InsideWorldCard, InsideWorldItem,
    SkillGroup, JourneyEntry, PortfolioCategory, Project, ProjectGalleryImage, Tag,
    BlogPost, Comment, ContactMessage, TeamMember, StudentCategory, Student, SiteStats,
)


class SiteSettingsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"


class ProfileAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class SocialLinkAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = "__all__"


class ServiceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class InsideWorldCardAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsideWorldCard
        fields = "__all__"


class InsideWorldItemAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsideWorldItem
        fields = "__all__"


class SkillGroupAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillGroup
        fields = "__all__"


class JourneyEntryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyEntry
        fields = "__all__"


class PortfolioCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioCategory
        fields = "__all__"
        read_only_fields = ["slug"]


class TagAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["slug"]


class ProjectAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["slug", "created_at"]


class ProjectGalleryImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGalleryImage
        fields = "__all__"


class BlogPostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = "__all__"
        read_only_fields = ["slug", "created_at", "view_count"]


class TeamMemberAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class StudentCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCategory
        fields = "__all__"
        read_only_fields = ["slug"]


class StudentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class SiteStatsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStats
        fields = "__all__"
        read_only_fields = ["total_visits"]


class CommentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["post", "name", "email", "message", "created_at"]


class ContactMessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
        read_only_fields = ["name", "email", "message", "created_at"]
