from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from optimization.models import Comment, Post

class Command(BaseCommand):
    help = "Create demo users, posts, and comments for testing optimization."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        users = []
        for i in range(1, 6):
            user, _ = User.objects.get_or_create(
                username=f"demo_user_{i}",
                defaults={"email": f"demo{i}@example.com"},
            )
            users.append(user)

        for i in range(1, 31):
            post, created = Post.objects.get_or_create(
                title=f"Performance demo post {i}",
                defaults={
                    "author": users[(i - 1) % len(users)],
                    "body": (
                        "This sample post is included to demonstrate ORM query optimization, "
                        "database indexes, caching, and Debug Toolbar analysis. " * 3
                    ),
                    "is_published": True,
                },
            )
            if created:
                for j in range(1, 4):
                    Comment.objects.create(
                        post=post,
                        author=users[(i + j) % len(users)],
                        body=f"Sample comment {j} on post {i}.",
                    )

        self.stdout.write(self.style.SUCCESS(
            "Demo data ready: 5 demo users, up to 30 posts, and sample comments."
        ))
