# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import BaseCommand

from restaurants.etl import run


class Command(BaseCommand):
    help = "Get restaurant inspection data from NYC OpenData and store the data in the database."

    def handle(self, *args, **options):
        run()
        self.stdout.write(self.style.SUCCESS("ETL Complete"))
