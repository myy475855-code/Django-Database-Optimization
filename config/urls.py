from django.contrib import admin
from django.urls import include, path
from optimization import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("posts/", views.post_list, name="post_list"),
    path("posts/unoptimized/", views.post_list_unoptimized, name="post_list_unoptimized"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
]

# Debug Toolbar is strictly local-development tooling.
from django.conf import settings
if settings.DEBUG and "127.0.0.1" in settings.INTERNAL_IPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
