from django.contrib import admin
from .models import (
    SiteSettings, Profile, SocialLink, Service, InsideWorldCard, InsideWorldItem,
    SkillGroup, JourneyEntry, PortfolioCategory, Project, ProjectGalleryImage, Tag,
    BlogPost, Comment, ContactMessage, TeamMember, StudentCategory, Student, SiteStats,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order")
    list_editable = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)


class InsideWorldItemInline(admin.TabularInline):
    model = InsideWorldItem
    extra = 1


@admin.register(InsideWorldCard)
class InsideWorldCardAdmin(admin.ModelAdmin):
    list_display = ("title", "card_type", "order")
    list_editable = ("order",)
    inlines = [InsideWorldItemInline]


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ("label", "items", "level_percent", "order")
    list_editable = ("order",)


@admin.register(JourneyEntry)
class JourneyEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "order")
    list_editable = ("order",)


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}


class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "order", "created_at")
    list_editable = ("order", "is_published")
    list_filter = ("category", "is_published", "tags")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    inlines = [ProjectGalleryImageInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_at", "read_minutes", "display_views")
    list_filter = ("is_published", "tags")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    readonly_fields = ("view_count",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("order",)


@admin.register(StudentCategory)
class StudentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "role", "project_count", "order")
    list_editable = ("order",)
    list_filter = ("category",)


@admin.register(SiteStats)
class SiteStatsAdmin(admin.ModelAdmin):
    readonly_fields = ("total_visits",)

    def has_add_permission(self, request):
        return not SiteStats.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "post")
    search_fields = ("name", "email", "message")
    actions = ["approve_comments", "reject_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(status="approved")
    approve_comments.short_description = "Tanlangan izohlarni tasdiqlash"

    def reject_comments(self, request, queryset):
        queryset.update(status="rejected")
    reject_comments.short_description = "Tanlangan izohlarni rad etish"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "message")
