from rest_framework import serializers
from .models import (
    SiteSettings, Profile, SocialLink, Service, InsideWorldCard, InsideWorldItem,
    SkillGroup, JourneyEntry, PortfolioCategory, Project, ProjectGalleryImage, Tag,
    BlogPost, Comment, ContactMessage, TeamMember, StudentCategory, Student, SiteStats,
)


class SiteSettingsSerializer(serializers.ModelSerializer):
    favicon = serializers.ImageField(use_url=True, required=False)
    background_image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = SiteSettings
        fields = ["site_name", "favicon", "meta_description", "meta_keywords",
                  "background_image", "accent_color", "cube_rotation_seconds"]


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ["full_name", "display_name", "title", "avatar", "email", "phone",
                   "birthday", "location", "about_intro", "about_extra"]


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source="get_platform_display", read_only=True)

    class Meta:
        model = SocialLink
        fields = ["id", "platform", "platform_display", "url", "order"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "icon", "title", "description", "order"]


class InsideWorldItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsideWorldItem
        fields = ["id", "emoji", "bold_part", "rest_text", "order"]


class InsideWorldCardSerializer(serializers.ModelSerializer):
    items = InsideWorldItemSerializer(many=True, read_only=True)

    class Meta:
        model = InsideWorldCard
        fields = ["id", "icon", "title", "card_type", "body_text", "order", "items"]


class SkillGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillGroup
        fields = ["id", "label", "items", "level_percent", "order"]


class JourneyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyEntry
        fields = ["id", "title", "year", "description", "order"]


class PortfolioCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioCategory
        fields = ["id", "name", "slug", "order"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class ProjectGalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProjectGalleryImage
        fields = ["id", "image", "order"]


class ProjectListSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(use_url=True)
    category = PortfolioCategorySerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "slug", "category", "cover_image", "short_description", "order"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(use_url=True)
    category = PortfolioCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    gallery = ProjectGalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "slug", "category", "cover_image", "short_description",
                  "description", "project_url", "github_url", "tags", "gallery", "created_at"]


class BlogPostListSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(use_url=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    views = serializers.IntegerField(source="display_views", read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "cover_image", "excerpt", "read_minutes",
                  "tags", "published_at", "views", "comment_count"]

    def get_comment_count(self, obj):
        return obj.comments.filter(status="approved").count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(use_url=True, required=False)
    tags = TagSerializer(many=True, read_only=True)
    views = serializers.IntegerField(source="display_views", read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "cover_image", "excerpt", "body", "read_minutes",
                  "tags", "published_at", "views", "comment_count"]

    def get_comment_count(self, obj):
        return obj.comments.filter(status="approved").count()


class TeamMemberSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = TeamMember
        fields = ["id", "name", "role", "avatar", "icon", "accent_color", "skills",
                  "description", "github_url", "linkedin_url", "telegram_url", "portfolio_url", "order"]


class StudentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCategory
        fields = ["id", "name", "slug", "order"]


class StudentSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True, required=False)
    category = StudentCategorySerializer(read_only=True)

    class Meta:
        model = Student
        fields = ["id", "name", "photo", "role", "category", "skills", "start_date",
                  "end_date", "project_count", "portfolio_url", "order"]


class SiteStatsSerializer(serializers.Serializer):
    visits = serializers.IntegerField()
    contact_messages = serializers.IntegerField()
    comments = serializers.IntegerField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "name", "message", "created_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["name", "email", "message"]

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Ism kiritish majburiy.")
        return value


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
