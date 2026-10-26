
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Generate 5,000 demo posts for FlowHub"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=5000,
            help="Number of posts to generate",
        )

    def handle(self, *args, **options):
        count = options["count"]
        users = list(User.objects.all())

        if not users:
            self.stderr.write(
                self.style.ERROR(
                    "No users found. Run seed_flowhub first."
                )
            )
            return

        titles = [
            "Understanding System Design",
            "Building Better APIs",
            "Database Optimization",
            "Learning Django",
            "Exploring Redis",
            "Backend Engineering",
            "Scalable Applications",
            "Caching Fundamentals",
            "Reliable Software",
            "PostgreSQL Tips",
        ]

        posts = [
            Post(
                title=f"{random.choice(titles)} #{i + 1}",
                body=(
                    f"Demo post number {i + 1}. "
                    "This post was generated to help us "
                    "experiment with FlowHub performance."
                ),
                author=random.choice(users),
            )
            for i in range(count)
        ]

        with transaction.atomic():
            Post.objects.bulk_create(posts, batch_size=500)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {count} posts."
            )
        )
