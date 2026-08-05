from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.api_urls")),
    path("api/auth/", include("core.auth_urls")),
    path("api/admin/", include("core.admin_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Frontend (static HTML/CSS/JS) — bitta index.html, ichki navigatsiya JS orqali.
# /admin/, /api/, /static/, /media/ dan boshqa har qanday yo'l shu SPA shell'ni qaytaradi.
urlpatterns += [
    re_path(r"^(?!admin|api|static|media).*$", TemplateView.as_view(template_name="index.html"), name="spa"),
]
