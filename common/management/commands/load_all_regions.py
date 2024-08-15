import json
from pathlib import Path

from django.core.management.base import BaseCommand
from common.models import Region, Country
from core.settings.base import BASE_DIR


class Command(BaseCommand):
    help = "Load all countries from the countries.json file"

    def handle(self, *args, **kwargs):
        try:
            file_path = Path(BASE_DIR) / "data" / "regions.json"
            with file_path.open(encoding='utf-8') as file:

                regions = json.load(file)
                country = Country.objects.get(name="O'zbekiston", code="UZ")
                for region in regions:
                    Region.objects.create(name=region["name_uz"], country=country)
            self.stdout.write(self.style.SUCCESS("Regions loaded successfully!"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("regions.json file not found."))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON. Please check the regions.json file."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))