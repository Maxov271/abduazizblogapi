from django.urls import path
from . import api_views as v

urlpatterns = [
    path("site-settings/", v.site_settings_view, name="api_site_settings"),
    path("profile/", v.profile_view, name="api_profile"),
    path("social-links/", v.SocialLinkListView.as_view(), name="api_social_links"),
    path("services/", v.ServiceListView.as_view(), name="api_services"),
    path("inside-world/", v.InsideWorldListView.as_view(), name="api_inside_world"),
    path("skills/", v.SkillGroupListView.as_view(), name="api_skills"),
    path("journey/", v.JourneyEntryListView.as_view(), name="api_journey"),
    path("portfolio-categories/", v.PortfolioCategoryListView.as_view(), name="api_portfolio_categories"),
    path("portfolio/", v.ProjectListView.as_view(), name="api_portfolio_list"),
    path("portfolio/<slug:slug>/", v.ProjectDetailView.as_view(), name="api_portfolio_detail"),
    path("thread/", v.BlogPostListView.as_view(), name="api_thread_list"),
    path("thread/<slug:slug>/", v.BlogPostDetailView.as_view(), name="api_thread_detail"),
    path("thread/<slug:slug>/comments/", v.blog_comments_view, name="api_thread_comments"),
    path("thread/<slug:slug>/comments/create/", v.blog_comment_create_view, name="api_thread_comment_create"),
    path("contact/", v.contact_create_view, name="api_contact"),
    path("team/", v.TeamMemberListView.as_view(), name="api_team"),
    path("student-categories/", v.StudentCategoryListView.as_view(), name="api_student_categories"),
    path("students/", v.StudentListView.as_view(), name="api_students"),
    path("stats/", v.site_stats_view, name="api_stats"),
    path("stats/track-visit/", v.track_visit_view, name="api_track_visit"),
]
