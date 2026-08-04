from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    SiteSettings, Profile, SocialLink, Service, InsideWorldCard,
    SkillGroup, JourneyEntry, PortfolioCategory, Project, BlogPost,
)
from .serializers import (
    SiteSettingsSerializer, ProfileSerializer, SocialLinkSerializer, ServiceSerializer,
    InsideWorldCardSerializer, SkillGroupSerializer, JourneyEntrySerializer,
    PortfolioCategorySerializer, ProjectListSerializer, ProjectDetailSerializer,
    BlogPostListSerializer, BlogPostDetailSerializer, CommentSerializer,
    CommentCreateSerializer, ContactMessageSerializer,
)
from .telegram import notify_new_comment, notify_new_contact_message


@api_view(["GET"])
def site_settings_view(request):
    return Response(SiteSettingsSerializer(SiteSettings.load(), context={"request": request}).data)


@api_view(["GET"])
def profile_view(request):
    return Response(ProfileSerializer(Profile.load(), context={"request": request}).data)


class SocialLinkListView(generics.ListAPIView):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class InsideWorldListView(generics.ListAPIView):
    queryset = InsideWorldCard.objects.prefetch_related("items").all()
    serializer_class = InsideWorldCardSerializer


class SkillGroupListView(generics.ListAPIView):
    queryset = SkillGroup.objects.all()
    serializer_class = SkillGroupSerializer


class JourneyEntryListView(generics.ListAPIView):
    queryset = JourneyEntry.objects.all()
    serializer_class = JourneyEntrySerializer


class PortfolioCategoryListView(generics.ListAPIView):
    queryset = PortfolioCategory.objects.all()
    serializer_class = PortfolioCategorySerializer


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        qs = Project.objects.filter(is_published=True).select_related("category")
        category = self.request.query_params.get("category")
        if category and category != "all":
            qs = qs.filter(category__slug=category)
        return qs


class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectDetailSerializer
    lookup_field = "slug"


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_published=True).prefetch_related("tags")
    serializer_class = BlogPostListSerializer


class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"


@api_view(["GET"])
def blog_comments_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    comments = post.comments.filter(status="approved")
    return Response(CommentSerializer(comments, many=True).data)


@api_view(["POST"])
def blog_comment_create_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        comment = serializer.save(post=post, status="pending")
        notify_new_comment(comment)
        return Response(
            {"detail": "Izohingiz yuborildi! Tasdiqlangach saytda ko'rinadi."},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def contact_create_view(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        msg = serializer.save()
        notify_new_contact_message(msg)
        return Response(
            {"detail": "Xabaringiz yuborildi! Tez orada javob beraman."},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
