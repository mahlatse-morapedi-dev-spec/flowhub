
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from apps.posts.models import Post

User = get_user_model()


class Command(BaseCommand):
    help = "Create sample users and posts for FlowHub"

    def handle(self, *args, **options):
        sample_users = [
            ("alice", "alice@example.com"),
            ("bob", "bob@example.com"),
            ("charlie", "charlie@example.com"),
            ("diana", "diana@example.com"),
            ("ethan", "ethan@example.com"),
            ("fatima", "fatima@example.com"),
            ("grace", "grace@example.com"),
        ]

        users = {}

        for username, email in sample_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )

            if created:
                user.set_password("FlowHubDemo123!")
                user.save(update_fields=["password"])

            users[username] = user

        sample_posts = [
            {
                "title": "Welcome to FlowHub",
                "body": "Our API is now backed by PostgreSQL.",
                "author": "alice",
            },
            {
                "title": "Learning system design",
                "body": "We are building the fundamentals step by step.",
                "author": "bob",
            },
            {
                "title": "Why APIs need pagination",
                "body": "Pagination helps clients retrieve large collections in manageable pages.",
                "author": "charlie",
            },
            {
                "title": "Understanding database indexes",
                "body": "Indexes can help PostgreSQL find records without scanning an entire table.",
                "author": "diana",
            },
            {
                "title": "Authentication versus authorization",
                "body": "Authentication establishes identity; authorization determines what that identity can do.",
                "author": "ethan",
            },
            {
                "title": "Building reliable backend tests",
                "body": "Automated tests help us catch regressions when the API changes.",
                "author": "fatima",
            },
            {
                "title": "Scaling beyond a monolith",
                "body": "We should identify real bottlenecks before introducing queues, caches, or separate services.",
                "author": "grace",
            },
        ]

        for data in sample_posts:
            Post.objects.get_or_create(
                title=data["title"],
                author=users[data["author"]],
                defaults={"body": data["body"]},
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed data ready: {len(users)} users and "
                f"{len(sample_posts)} sample posts checked."
            )
        )
