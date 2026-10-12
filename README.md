# Django Database Optimization & Performance Tuning

A complete starter application demonstrating:
- Query optimization with `select_related()` and `prefetch_related()`
- Database indexes and a composite index
- Django cache framework with local-memory development cache
- Cache invalidation when posts/comments change
- Django Debug Toolbar for local SQL query inspection
- A small blog-like demo with seeded sample data and a benchmark command

## Requirements
- Python 3.10+
- pip

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Demo pages
- `/` — dashboard and performance concepts
- `/posts/` — optimized, cached post list
- `/posts/<id>/` — post detail with prefetched comments
- `/admin/` — Django admin (create a superuser with `python manage.py createsuperuser`)
- `/__debug__/` — Debug Toolbar URLs (toolbar appears on eligible local HTML responses)

## Inspect performance
1. Open `/posts/` and look at the Debug Toolbar's SQL panel.
2. Refresh `/posts/` to observe cache behavior (the cache panel is not built in; inspect the view and logs).
3. Compare the optimized endpoint against the intentionally unoptimized `/posts/unoptimized/` route.
4. Run `python manage.py benchmark_queries` for a simple query-count comparison.

The exact query counts vary by Django version and data. The benchmark reports observed counts instead of promising fixed numbers.

## Production notes
- Debug Toolbar is enabled only when `DEBUG=True`; never expose it publicly.
- `LocMemCache` is for development/single-process use. Use Redis or another shared cache for multi-worker production deployments.
- Configure `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, database credentials, HTTPS, and logging appropriately before deployment.
- Review query plans (`QuerySet.explain()`) and real traffic before adding indexes. Indexes use storage and can slow writes.
