from django.core.management.base import BaseCommand
from django.utils import timezone
from chores.models import Chore
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clears the completed status of all chores to False'

    def handle(self, *args, **kwargs):
        # Reset all chores' completed status to False
        updated_count = Chore.objects.filter(completed=True).update(completed=False)
        clear_time = timezone.now()
        logger.info(f"Cleared {updated_count} chore(s) completed status at {clear_time}")
        self.stdout.write(self.style.SUCCESS(f"Successfully cleared {updated_count} chore(s) completed status at {clear_time}"))