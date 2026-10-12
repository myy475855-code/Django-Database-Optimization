from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Comment, Post

POST_LIST_CACHE_KEY = "optimization:published-posts:v1"


@receiver([post_save, post_delete], sender=Post)
@receiver([post_save, post_delete], sender=Comment)
def clear_post_list_cache(sender, **kwargs):
    # Comments affect the displayed comment count, so they invalidate the listing too.
    cache.delete(POST_LIST_CACHE_KEY)
