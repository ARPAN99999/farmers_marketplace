# Deploying to Vercel with SQLite

This project can run on Vercel without PostgreSQL, but SQLite is not durable on Vercel. The database is stored in `/tmp` and may be reset whenever Vercel creates a new serverless instance. This is suitable for a demonstration, prototype, or read-only catalog, not a production marketplace that must preserve orders.

## Deploy

1. Push the project to GitHub and import it into Vercel.
2. Keep the framework preset as **Other**.
3. Add these environment variables for **Production**:

   - `DJANGO_SECRET_KEY`: a long random secret
   - `DJANGO_DEBUG`: `False`
   - `DJANGO_ALLOWED_HOSTS`: `.vercel.app,your-custom-domain.com`
   - `DJANGO_CSRF_TRUSTED_ORIGINS`: `https://your-project.vercel.app,https://your-custom-domain.com`

4. Deploy. Vercel uses `api/index.py` as the Django serverless entrypoint.

The first request on a fresh instance runs Django migrations automatically. Because `/tmp` is temporary, demo accounts, products, and orders can disappear after an instance is recycled.

## Local development

Run the normal local SQLite application with:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```