from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import admin_api_views as v

router = DefaultRouter()
router.register("social-links", v.SocialLinkAdminViewSet, basename="admin-social-links")
router.register("services", v.ServiceAdminViewSet, basename="admin-services")
router.register("inside-world", v.InsideWorldCardAdminViewSet, basename="admin-inside-world")
router.register("inside-world-items", v.InsideWorldItemAdminViewSet, basename="admin-inside-world-items")
router.register("skills", v.SkillGroupAdminViewSet, basename="admin-skills")
router.register("journey", v.JourneyEntryAdminViewSet, basename="admin-journey")
router.register("portfolio-categories", v.PortfolioCategoryAdminViewSet, basename="admin-portfolio-categories")
router.register("tags", v.TagAdminViewSet, basename="admin-tags")
router.register("portfolio", v.ProjectAdminViewSet, basename="admin-portfolio")
router.register("portfolio-gallery", v.ProjectGalleryImageAdminViewSet, basename="admin-portfolio-gallery")
router.register("thread", v.BlogPostAdminViewSet, basename="admin-thread")
router.register("comments", v.CommentAdminViewSet, basename="admin-comments")
router.register("contact-messages", v.ContactMessageAdminViewSet, basename="admin-contact-messages")

urlpatterns = [
    path("site-settings/", v.SiteSettingsAdminView.as_view(), name="admin_site_settings"),
    path("profile/", v.ProfileAdminView.as_view(), name="admin_profile"),
    path("", include(router.urls)),
]
