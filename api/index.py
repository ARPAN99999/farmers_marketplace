import os
import tempfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmers_marketplace.settings')

# Vercel's project directory is read-only. SQLite uses /tmp there, so initialize
# the schema in each fresh serverless instance before handling requests.
if os.environ.get('VERCEL'):
    os.environ.setdefault('SQLITE_DATABASE_PATH', os.path.join(tempfile.gettempdir(), 'farmers_marketplace.sqlite3'))

import django
django.setup()

if os.environ.get('VERCEL'):
    from django.core.management import call_command
    call_command('migrate', verbosity=0, interactive=False)

from farmers_marketplace.wsgi import application