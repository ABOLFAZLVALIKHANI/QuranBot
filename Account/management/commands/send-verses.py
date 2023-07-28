import errno
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand , CommandError

from django_tgbot_vip.management import helpers


class Command(BaseCommand):
    help = 'send Verses to user'

    def handle(self, *args, **options):
        try:
                pass 
        except Exception as e :
            raise CommandError(f'error for check portfo = {e}')
        
