import os
import tempfile
import mimetypes
from pathlib import Path
from urllib.parse import unquote

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


class StaticAssetMiddleware:
    def __init__(self, app):
        self.app = app
        self.static_root = (Path(__file__).resolve().parent.parent / 'static').resolve()

    def __call__(self, environ, start_response):
        request_path = environ.get('PATH_INFO', '')
        if request_path.startswith('/static/'):
            relative_path = Path(unquote(request_path.removeprefix('/static/')))
            asset_path = (self.static_root / relative_path).resolve()
            if asset_path.is_relative_to(self.static_root) and asset_path.is_file():
                content = asset_path.read_bytes()
                content_type = mimetypes.guess_type(asset_path.name)[0] or 'application/octet-stream'
                start_response('200 OK', [('Content-Type', content_type), ('Content-Length', str(len(content))), ('Cache-Control', 'public, max-age=31536000')])
                return [content]
        return self.app(environ, start_response)


application = StaticAssetMiddleware(application)