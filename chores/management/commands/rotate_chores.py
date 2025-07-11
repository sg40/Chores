from django.core.management.base import BaseCommand
from django.utils import timezone
from chores.models import Person, Chore, ChoreGroup, RotationLog
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Rotates chore groups between two persons and resets chore completion status'

    def handle(self, *args, **kwargs):
        # Ensure exactly two persons and two chore groups
        persons = Person.objects.all()
        chore_groups = ChoreGroup.objects.all()

        if persons.count() != 2 or chore_groups.count() != 2:
            logger.error(f"Rotation requires exactly 2 persons and 2 chore groups. Found {persons.count()} persons and {chore_groups.count()} groups.")
            self.stdout.write(self.style.ERROR("Rotation failed: Exactly 2 persons and 2 chore groups required."))
            return

        # Get the two persons and groups
        person1, person2 = persons
        group1, group2 = chore_groups

        # Swap chore groups
        person1_group = person1.chore_group
        person2_group = person2.chore_group

        person1.chore_group = person2_group
        person2.chore_group = person1_group
        person1.save()
        person2.save()

        # Reset chore completion status
        Chore.objects.update(completed=False)

        # Log rotation
        rotation_time = timezone.now()
        RotationLog.objects.create(rotation_time=rotation_time)
        logger.info(f"Chore groups rotated at {rotation_time}: {person1.name} to {person1.chore_group}, {person2.name} to {person2.chore_group}")

        self.stdout.write(self.style.SUCCESS(f"Successfully rotated chore groups at {rotation_time}"))