import os
import sys
import dotenv
import django

from django.test.utils import get_runner
from django.conf import settings

def runtests():
    dotenv.load_dotenv()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()

