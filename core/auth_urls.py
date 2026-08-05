from django.urls import path
from . import auth_views as v

urlpatterns = [
    path("login/", v.login_view, name="auth_login"),
    path("me/", v.me_view, name="auth_me"),
    path("logout/", v.logout_view, name="auth_logout"),
]
