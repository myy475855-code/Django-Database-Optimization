from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.test.utils import override_settings
from optimization.models import Post

class Command(BaseCommand):
    help = "Compare SQL query counts for a simple optimized and unoptimized access pattern."

    def handle(self, *args, **options):
        with override_settings(DEBUG=True):
            reset_queries()
            posts = list(Post.objects.filter(is_published=True)[:50])
            for post in posts:
                _ = post.author.username
                _ = post.comments.count()
            unoptimized_count = len(connection.queries)

            reset_queries()
            posts = list(
                Post.objects.filter(is_published=True)
                .select_related("author")
                .prefetch_related("comments")[:50]
            )
            for post in posts:
                _ = post.author.username
                _ = list(post.comments.all())
            optimized_count = len(connection.queries)

        self.stdout.write(f"Unoptimized query count: {unoptimized_count}")
        self.stdout.write(f"Optimized query count:   {optimized_count}")
        if unoptimized_count:
            reduction = (unoptimized_count - optimized_count) / unoptimized_count * 100
            self.stdout.write(f"Query-count reduction:   {reduction:.1f}%")
        self.stdout.write("Counts depend on available data and database backend.")
