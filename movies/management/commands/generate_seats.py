from django.core.management.base import BaseCommand
from movies.models import Screen, Seat
import math
import string

seats_per_row = 10  # Define how many seats per row


def generate_row_labels(n):
    """Generate Excel-style row labels (A, B, ..., Z, AA, AB, ...)"""
    labels = []
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        labels.append(string.ascii_uppercase[remainder])
    return "".join(reversed(labels))


class Command(BaseCommand):
    help = "Generate or delete seats for a screen based on its capacity."

    def add_arguments(self, parser):
        parser.add_argument(
            "screen_name", type=str, help="Name of the screen to generate seats for"
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing seats before generating new ones",
        )
        parser.add_argument(
            "--delete-only",
            action="store_true",
            help="Delete all seats for the given screen without generating new ones",
        )

    def handle(self, *args, **kwargs):
        screen_name = kwargs["screen_name"]
        clear_existing = kwargs["clear"]
        delete_only = kwargs["delete_only"]

        # 1. Fetch the screen
        try:
            screen = Screen.objects.get(name=screen_name)
        except Screen.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Screen {screen_name} does not exist."))
            return

        if delete_only:
            deleted_count, _ = Seat.objects.filter(screen=screen).delete()
            self.stdout.write(
                self.style.WARNING(f"Deleted {deleted_count} seats for {screen_name}.")
            )
            return

        capacity = screen.capacity
        total_rows = math.ceil(capacity / seats_per_row)

        self.stdout.write(f"Found {screen_name} with capacity {capacity}.")
        self.stdout.write(
            f"Generating {total_rows} rows (standard {seats_per_row} seats each)."
        )

        # 2. Clear existing seats
        if clear_existing:
            deleted_count, _ = Seat.objects.filter(screen=screen).delete()
            self.stdout.write(
                self.style.WARNING(f"Deleted {deleted_count} existing seats.")
            )

        # 3. Generate seats
        seats_to_create = []
        seats_created_count = 0

        for row_index in range(total_rows):
            row_char = generate_row_labels(row_index + 1)  # Excel-style labels
            remaining_seats = capacity - seats_created_count
            seats_in_this_row = min(seats_per_row, remaining_seats)

            for number in range(1, seats_in_this_row + 1):
                if not Seat.objects.filter(
                    screen=screen, row=row_char, number=number
                ).exists():
                    seats_to_create.append(
                        Seat(
                            screen=screen,
                            row=row_char,
                            number=number,
                            seat_type="Regular",
                        )
                    )

            seats_created_count += seats_in_this_row

        # 4. Save to DB
        Seat.objects.bulk_create(seats_to_create)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(seats_to_create)} seats for "{screen_name}"!'
            )
        )
