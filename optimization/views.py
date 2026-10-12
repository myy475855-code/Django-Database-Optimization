from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from .models import Comment, Post

User = get_user_model()
POST_LIST_CACHE_KEY = "optimization:published-posts:v1"
CACHE_TIMEOUT = 300


def dashboard(request):
    stats = {
        "posts": Post.objects.filter(is_published=True).count(),
        "comments": Comment.objects.count(),
        "authors": User.objects.filter(optimization_posts__isnull=False).distinct().count(),
    }
    return render(request, "optimization/dashboard.html", {"stats": stats})


def post_list(request):
    """Optimized and cached listing: one cache lookup, then a bounded optimized query."""
    posts = cache.get(POST_LIST_CACHE_KEY)
    cache_hit = posts is not None

    if not cache_hit:
        posts = list(
            Post.objects.filter(is_published=True)
            .select_related("author")
            .annotate(comment_count=Count("comments"))
            .order_by("-created_at")[:50]
        )
        cache.set(POST_LIST_CACHE_KEY, posts, timeout=CACHE_TIMEOUT)

    return render(
        request,
        "optimization/post_list.html",
        {"posts": posts, "cache_hit": cache_hit, "optimized": True},
    )


def post_list_unoptimized(request):
    """Teaching comparison: deliberately avoids related-object optimization and caching."""
    posts = Post.objects.filter(is_published=True).order_by("-created_at")[:50]
    # The template accesses post.author and post.comments.count(), exposing N+1 patterns.
    return render(
        request,
        "optimization/post_list.html",
        {"posts": posts, "cache_hit": False, "optimized": False},
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related("comments__author"),
        pk=post_id,
        is_published=True,
    )
    comments = post.comments.all()
    return render(request, "optimization/post_detail.html", {"post": post, "comments": comments})
