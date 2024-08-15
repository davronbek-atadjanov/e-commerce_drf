import json
from pathlib import Path

from django.core.management.base import BaseCommand
from common.models import Country
from core.settings.base import BASE_DIR


class Command(BaseCommand):
    help = "Load all countries from the countries.json file"

    def handle(self, *args, **kwargs):
        try:
            file_path = Path(BASE_DIR) / "data" / "countries.json"
            with file_path.open(encoding='utf-8') as file:

                countries = json.load(file)
                for country in countries:
                    Country.objects.create(name=country["name_uz"], code=country["code"])
            self.stdout.write(self.style.SUCCESS("Countries loaded successfully!"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("countries.json file not found."))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding JSON. Please check the countries.json file."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))