# type:ignore

from django.contrib.staticfiles import finders




import datetime

from django.test import TestCase
from django.utils import timezone
# from django.urls import reverse

# from polls.models import Question

class StaticFilesTest(TestCase):

    def test_static_files_served(self):
        """
        Static files are being served correctly.
        """
        EXPECTED_ROOT = '/home/app/web/'
        # EXPECTED_ROOT = 'https://d337ewj4ohwll8.cloudfront.net'

        searched_locations = finders.searched_locations
        root_in_searched_locations = [EXPECTED_ROOT in loc for loc in searched_locations]
        all_in_root = all(root_in_searched_locations )
        self.assertTrue(all_in_root)
        # self.assertEquals(searched_locations, [
        #     '/home/app/web/static', 
        #     '/home/app/web/.[123 chars]tic',
        #     '/home/app/web/.venv/lib/python3.10/site-packages/django/contrib/admin/static',
        #     '/home/app/web/.venv/lib/python3.10/site-packages/polls/static'
        # ])