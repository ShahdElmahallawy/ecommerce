import time
import redis
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        redis_up = False

        while redis_up is False:
            try:
                redis.StrictRedis(host="redis", port=6379, db=0)
                redis_up = True
            except redis.exceptions.ConnectionError:
                self.stdout.write("Redis unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Redis available!"))
